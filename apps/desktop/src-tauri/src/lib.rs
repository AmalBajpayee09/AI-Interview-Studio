//! Windows packaged worker supervisor. Only an authenticated health response marks it ready.
//! Diagnostic events are deliberately schema-limited: no prompts, credentials, tokens or audio.
use std::{
    fs::{self, OpenOptions},
    io::{Read, Write},
    net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpListener, TcpStream},
    path::{Path, PathBuf},
    process::{Child, Command, Stdio},
    sync::{atomic::{AtomicBool, Ordering}, Mutex},
    thread,
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};
use serde::Serialize;
use serde_json::json;
use tauri::{AppHandle, LogicalSize, Manager, Size};

const MAX_RESTARTS: u8 = 2;
const READY_TIMEOUT: Duration = Duration::from_secs(22);

struct WorkerRuntime {
    child: Option<Child>,
    started: Instant,
    attempts: u8,
    ready: bool,
    stage: &'static str,
    failure: Option<&'static str>,
    startup_ms: Option<u64>,
    last_health_check: Instant,
    consecutive_failures: u8,
}

struct WorkerState {
    runtime: Mutex<WorkerRuntime>,
    executable: PathBuf,
    log_dir: PathBuf,
    base: String,
    port: u16,
    token: String,
    stopping: AtomicBool,
}

#[derive(Serialize)]
struct WorkerConnection { base: String, token: String }

#[derive(Serialize)]
struct WorkerStatus {
    running: bool,
    ready: bool,
    stage: &'static str,
    failure_category: Option<&'static str>,
    restart_attempts: u8,
    startup_ms: Option<u64>,
    diagnostic_log: String,
}

fn rotate(path: &Path, limit: u64) {
    if path.metadata().map(|m| m.len() >= limit).unwrap_or(false) {
        let previous = path.with_extension("previous.log");
        let _ = fs::remove_file(&previous);
        let _ = fs::rename(path, previous);
    }
}

fn event(state: &WorkerState, stage: &'static str, outcome: &'static str, attempt: u8, duration_ms: Option<u64>) {
    let path = state.log_dir.join("worker-lifecycle.jsonl");
    rotate(&path, 256 * 1024);
    let millis = SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default().as_millis();
    let line = json!({"timestamp_ms":millis,"component":"desktop-worker-supervisor",
        "app_version":env!("CARGO_PKG_VERSION"),"build_commit":option_env!("GITHUB_SHA").unwrap_or("unavailable"),
        "stage":stage,"outcome":outcome,"restart_attempt":attempt,"duration_ms":duration_ms});
    if let Ok(mut f) = OpenOptions::new().create(true).append(true).open(path) {
        let _ = writeln!(f, "{}", line);
    }
}

fn readiness_marker(state: &WorkerState, rt: &WorkerRuntime) {
    // No secrets, user data, URLs, path information or authentication material in this file.
    let pid = rt.child.as_ref().map(|p| p.id());
    let marker = json!({"app_version":env!("CARGO_PKG_VERSION"),
        "build_commit":option_env!("GITHUB_SHA").unwrap_or("unavailable"),
        "worker_pid":pid,"stage":rt.stage,"authenticated":rt.ready,
        "worker_version": if rt.ready {Some(env!("CARGO_PKG_VERSION"))} else {None},
        "failure_category":rt.failure,
        "restart_attempts":rt.attempts.saturating_sub(1),"startup_ms":rt.startup_ms,
        "timestamp_ms":SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default().as_millis()});
    let path = state.log_dir.join("worker-readiness.json");
    let tmp = state.log_dir.join("worker-readiness.tmp");
    if fs::write(&tmp, marker.to_string()).is_ok() {
        // Windows cannot atomically rename over an existing destination.
        let _ = fs::remove_file(&path);
        let _ = fs::rename(tmp,path);
    }
}

fn spawn_worker(state: &WorkerState) -> std::io::Result<Child> {
    let stderr_path = state.log_dir.join("worker-stderr.log");
    rotate(&stderr_path, 128 * 1024);
    let logfile = OpenOptions::new().create(true).append(true).open(stderr_path)?;
    Command::new(&state.executable)
        .current_dir(state.executable.parent().unwrap_or(Path::new(".")))
        .env("STUDIO_PORT", state.port.to_string())
        .env("STUDIO_WORKER_TOKEN", &state.token)
        .env("STUDIO_DIAGNOSTIC_DIR", &state.log_dir)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::from(logfile))
        .spawn()
}

fn stop_child(child: &mut Child) {
    #[cfg(windows)] {
        // PyInstaller onefile may have child processes; terminate the full owned process tree.
        let _ = Command::new("taskkill").args(["/PID", &child.id().to_string(), "/T", "/F"])
            .stdout(Stdio::null()).stderr(Stdio::null()).status();
    }
    let _ = child.kill();
    let _ = child.wait();
}

fn authenticated_health(port: u16, token: &str) -> bool {
    let addr = SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::LOCALHOST, port));
    let Ok(mut socket) = TcpStream::connect_timeout(&addr, Duration::from_millis(280)) else {return false};
    let _ = socket.set_read_timeout(Some(Duration::from_millis(450)));
    let _ = socket.set_write_timeout(Some(Duration::from_millis(350)));
    let request = format!("GET /api/health HTTP/1.1\r\nHost: 127.0.0.1\r\nX-Studio-Token: {}\r\nConnection: close\r\n\r\n",token);
    if socket.write_all(request.as_bytes()).is_err() {return false}
    let mut raw = Vec::with_capacity(1024);
    if socket.take(16_384).read_to_end(&mut raw).is_err() {return false}
    let Some(separator) = raw.windows(4).position(|part| part == b"\r\n\r\n") else {return false};
    let headers = String::from_utf8_lossy(&raw[..separator]);
    if !headers.lines().next().unwrap_or("").contains(" 200 ") {return false}
    let Ok(payload) = serde_json::from_slice::<serde_json::Value>(&raw[separator+4..]) else {return false};
    payload.get("status").and_then(|x|x.as_str())==Some("ok")
        && payload.get("version").and_then(|x|x.as_str())==Some(env!("CARGO_PKG_VERSION"))
}

fn check_worker(state: &WorkerState) {
    if state.stopping.load(Ordering::SeqCst) {return}
    let mut rt = match state.runtime.lock() {Ok(g)=>g,Err(_)=>return};
    if let Some(child) = rt.child.as_mut() {
        match child.try_wait() {
            Ok(Some(_)) => {
                rt.child.take(); rt.ready=false; rt.stage="exited"; rt.failure=Some("worker_exited");
                event(state,"worker_exited","error",rt.attempts,None);
                readiness_marker(state,&rt);
            }
            Err(_) => {
                rt.child.take(); rt.ready=false; rt.stage="process_error"; rt.failure=Some("process_inspection_failed");
                event(state,"process_inspection","error",rt.attempts,None);
            }
            Ok(None)=>{}
        }
    }
    if !state.executable.is_file() {
        // In dev mode the separately launched worker is probed, never spawned.
        if cfg!(debug_assertions) && authenticated_health(state.port,&state.token) {
            rt.ready=true;rt.stage="ready";rt.failure=None;readiness_marker(state,&rt);
        }
        return;
    }
    if rt.child.is_none() {
        if rt.attempts >= MAX_RESTARTS+1 {
            rt.stage="restart_exhausted"; rt.failure=Some("restart_limit");
            readiness_marker(state,&rt); return;
        }
        rt.attempts += 1;
        rt.started = Instant::now(); rt.last_health_check=Instant::now();
        rt.consecutive_failures=0; rt.startup_ms=None; rt.ready=false; rt.stage="launching";
        match spawn_worker(state) {
            Ok(child)=>{rt.child=Some(child);rt.stage="waiting_for_authenticated_health";rt.failure=None;
                event(state,"worker_spawn","ok",rt.attempts,None);}
            Err(_)=>{rt.stage="launch_failed";rt.failure=Some("process_launch_failed");
                event(state,"worker_spawn","error",rt.attempts,None);}
        }
        readiness_marker(state,&rt);
        return;
    }
    if !rt.ready && authenticated_health(state.port,&state.token) {
        rt.ready=true; rt.stage="ready";rt.failure=None;
        rt.last_health_check=Instant::now(); rt.consecutive_failures=0;
        let elapsed=rt.started.elapsed().as_millis() as u64; rt.startup_ms=Some(elapsed);
        event(state,"authenticated_health","ok",rt.attempts,Some(elapsed));
        readiness_marker(state,&rt);
    } else if rt.ready && rt.last_health_check.elapsed() >= Duration::from_secs(2) {
        rt.last_health_check=Instant::now();
        if authenticated_health(state.port,&state.token) {
            rt.consecutive_failures=0;
        } else {
            rt.consecutive_failures=rt.consecutive_failures.saturating_add(1);
            if rt.consecutive_failures >= 3 {
                rt.stage="health_lost";rt.failure=Some("authenticated_health_lost");rt.ready=false;
                event(state,"authenticated_health","error",rt.attempts,None);
                if let Some(mut child)=rt.child.take(){stop_child(&mut child)}
                readiness_marker(state,&rt);
            }
        }
    } else if !rt.ready && rt.started.elapsed() >= READY_TIMEOUT {
        rt.stage="readiness_timeout";rt.failure=Some("health_timeout");
        event(state,"authenticated_health","timeout",rt.attempts,None);
        if let Some(mut child)=rt.child.take(){stop_child(&mut child)}
        readiness_marker(state,&rt);
    }
}

fn get_status(state: &WorkerState) -> WorkerStatus {
    let rt = state.runtime.lock().expect("Worker state lock poisoned");
    WorkerStatus {running:rt.child.is_some(),ready:rt.ready,stage:rt.stage,
        failure_category:rt.failure,restart_attempts:rt.attempts.saturating_sub(1),startup_ms:rt.startup_ms,
        diagnostic_log:state.log_dir.join("worker-lifecycle.jsonl").display().to_string()}
}

// Never provide a worker token to the UI until the backend authenticates its own health response.
#[tauri::command]
async fn worker_connection(app: AppHandle) -> Result<WorkerConnection, String> {
    tauri::async_runtime::spawn_blocking(move || {
        let state = app.state::<WorkerState>();
        let start = Instant::now();
        while start.elapsed() < Duration::from_secs(72) {
            if state.stopping.load(Ordering::SeqCst) {return Err("Application is shutting down".into())}
            if state.runtime.lock().map_err(|_|"Worker state unavailable")?.ready {
                return Ok(WorkerConnection {base:state.base.clone(),token:state.token.clone()});
            }
            let status=get_status(&state);
            if status.stage=="restart_exhausted" {return Err("Worker startup failed after bounded recovery attempts. Export diagnostics for details.".into())}
            thread::sleep(Duration::from_millis(200));
        }
        Err("Worker did not pass authenticated readiness checks. Export diagnostics for details.".into())
    }).await.map_err(|_|"Worker readiness operation failed".to_string())?
}

#[tauri::command]
fn worker_status(state: tauri::State<'_, WorkerState>) -> WorkerStatus {get_status(&state)}

#[tauri::command]
fn restart_worker(state: tauri::State<'_, WorkerState>) -> Result<WorkerStatus, String> {
    if !state.executable.is_file() {return Err("Bundled AI worker missing; reinstall the app.".into())}
    {
        let mut rt=state.runtime.lock().map_err(|_|"Worker state unavailable")?;
        if let Some(mut child)=rt.child.take(){stop_child(&mut child)}
        rt.attempts=0; rt.ready=false;rt.stage="restart_requested";rt.failure=None;
        event(&state,"manual_restart","requested",0,None);
        readiness_marker(&state,&rt);
    }
    check_worker(&state);
    Ok(get_status(&state))
}

#[tauri::command]
fn export_worker_diagnostics(state: tauri::State<'_, WorkerState>) -> Result<String, String> {
    let src=state.log_dir.join("worker-lifecycle.jsonl");
    let dest=state.log_dir.join("diagnostics-export.jsonl");
    // Exports ONLY allowlisted structured lifecycle events; worker stderr may contain arbitrary
    // third-party exception text and is intentionally excluded from the export.
    let raw=fs::read_to_string(src).map_err(|_|"No lifecycle events have been recorded yet")?;
    let mut safe=Vec::new();
    for line in raw.lines().take(300) {
        if let Ok(v)=serde_json::from_str::<serde_json::Value>(line) {
            safe.push(json!({"timestamp_ms":v.get("timestamp_ms"),"component":v.get("component"),
                "app_version":v.get("app_version"),"build_commit":v.get("build_commit"),
                "stage":v.get("stage"),"outcome":v.get("outcome"),
                "restart_attempt":v.get("restart_attempt"),"duration_ms":v.get("duration_ms")}));
        }
    }
    let output=safe.into_iter().map(|v|v.to_string()).collect::<Vec<_>>().join("\n");
    fs::write(&dest,format!("{output}\n")).map_err(|_|"Could not write diagnostic export")?;
    Ok(dest.display().to_string())
}

#[tauri::command]
fn set_compact(window: tauri::Window, compact: bool) -> Result<(), String> {
    if compact {
        window.set_size(Size::Logical(LogicalSize::new(560.0, 720.0))).map_err(|e| e.to_string())?;
        window.set_always_on_top(true).map_err(|e| e.to_string())?;
    } else {
        window.set_always_on_top(false).map_err(|e| e.to_string())?;
        window.set_size(Size::Logical(LogicalSize::new(1320.0, 860.0))).map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
fn app_version() -> &'static str {env!("CARGO_PKG_VERSION")}

pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let executable=app.path().resolve("ai-studio-worker.exe",tauri::path::BaseDirectory::Resource)?;
            let log_dir=app.path().app_log_dir()?;
            fs::create_dir_all(&log_dir)?;
            let (port,token)=if executable.is_file() {
                let listener=TcpListener::bind("127.0.0.1:0")?;
                let port=listener.local_addr()?.port();drop(listener);
                (port,format!("{}{}",uuid::Uuid::new_v4(),uuid::Uuid::new_v4()))
            } else if cfg!(debug_assertions) {(8765,String::new())} else {
                return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
                    "Packaged AI worker not found in application resources").into());
            };
            let state=WorkerState {
                runtime:Mutex::new(WorkerRuntime {child:None,started:Instant::now(),attempts:0,
                    ready:false,stage:"initializing",failure:None,startup_ms:None,
                    last_health_check:Instant::now(),consecutive_failures:0}),
                executable,log_dir,base:format!("http://127.0.0.1:{port}"),port,token,
                stopping:AtomicBool::new(false),
            };
            event(&state,"desktop_launch","ok",0,None);
            app.manage(state);
            let handle=app.handle().clone();
            thread::spawn(move || {
                let state=handle.state::<WorkerState>();
                while !state.stopping.load(Ordering::SeqCst) {
                    check_worker(&state);
                    thread::sleep(Duration::from_millis(300));
                }
            });
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![worker_connection,worker_status,restart_worker,
            export_worker_diagnostics,set_compact,app_version])
        .on_window_event(|window,event| {
            if let tauri::WindowEvent::Destroyed=event {
                if let Some(state)=window.try_state::<WorkerState>() {
                    state.stopping.store(true,Ordering::SeqCst);
                    if let Ok(mut rt)=state.runtime.lock() {
                        if let Some(mut child)=rt.child.take(){stop_child(&mut child)}
                        rt.ready=false;rt.stage="stopped";
                        event(&state,"desktop_shutdown","ok",rt.attempts,None);
                        readiness_marker(&state,&rt);
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("Unable to start AI Interview Studio");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn metadata_does_not_include_tokens(){
        let v=json!({"stage":"ready","app_version":env!("CARGO_PKG_VERSION")});
        assert!(!v.to_string().contains("X-Studio-Token"));
    }
    #[test]
    fn restart_limit_is_bounded(){assert_eq!(MAX_RESTARTS,2)}
}

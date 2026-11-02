use std::{
    fs::{self, OpenOptions},
    net::TcpListener,
    path::PathBuf,
    process::{Child, Command, Stdio},
    sync::Mutex,
};
use serde::Serialize;
use tauri::{LogicalSize, Manager, Size};

struct WorkerState {
    child: Mutex<Option<Child>>,
    executable: PathBuf,
    log_path: PathBuf,
    base: String,
    token: String,
}

#[derive(Serialize)]
struct WorkerConnection { base: String, token: String }

#[derive(Serialize)]
struct WorkerStatus { running: bool, diagnostic_log: String }

// stderr is preserved in the user's per-app log directory rather than silently discarded.
// Do not log tokens, credentials, response bodies, or full command-line arguments.
fn spawn_worker(executable: &PathBuf, base: &str, token: &str, log_path: &PathBuf) -> std::io::Result<Child> {
    let port = base.rsplit(':').next().unwrap_or("0");
    let logfile = OpenOptions::new().create(true).append(true).open(log_path)?;
    Command::new(executable)
        .env("STUDIO_PORT", port)
        .env("STUDIO_WORKER_TOKEN", token)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::from(logfile))
        .spawn()
}

/// The token is scoped to the desktop process and never persisted to a file.
#[tauri::command]
fn worker_connection(state: tauri::State<'_, WorkerState>) -> WorkerConnection {
    WorkerConnection { base: state.base.clone(), token: state.token.clone() }
}

#[tauri::command]
fn worker_status(state: tauri::State<'_, WorkerState>) -> Result<WorkerStatus, String> {
    let mut lock = state.child.lock().map_err(|_| "Worker lock poisoned".to_string())?;
    let running = match lock.as_mut() {
        Some(child) => child.try_wait().map_err(|_| "Worker process check failed".to_string())?.is_none(),
        None => false,
    };
    if !running { lock.take(); }
    Ok(WorkerStatus { running, diagnostic_log: state.log_path.display().to_string() })
}

/// Explicit recovery action. Does not start an unrestricted or unauthenticated server.
#[tauri::command]
fn restart_worker(state: tauri::State<'_, WorkerState>) -> Result<WorkerStatus, String> {
    if !state.executable.is_file() {
        return Err("Packaged AI worker is missing; reinstall AI Interview Studio.".into());
    }
    let mut lock = state.child.lock().map_err(|_| "Worker lock poisoned".to_string())?;
    if let Some(child) = lock.as_mut() {
        if child.try_wait().map_err(|_| "Could not check worker state".to_string())?.is_none() {
            return Ok(WorkerStatus { running: true, diagnostic_log: state.log_path.display().to_string() });
        }
    }
    lock.take();
    let child = spawn_worker(&state.executable, &state.base, &state.token, &state.log_path)
        .map_err(|_| "Unable to launch bundled AI worker. Review the worker diagnostic log.".to_string())?;
    *lock = Some(child);
    Ok(WorkerStatus { running: true, diagnostic_log: state.log_path.display().to_string() })
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
fn app_version() -> &'static str { env!("CARGO_PKG_VERSION") }

pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let executable = app.path().resolve("ai-studio-worker.exe", tauri::path::BaseDirectory::Resource)?;
            let log_dir = app.path().app_log_dir()?;
            fs::create_dir_all(&log_dir)?;
            let log_path = log_dir.join("worker-stderr.log");
            let (child, base, token) = if executable.is_file() {
                // Unique port/token per application instance, never hardcoded to 8765.
                let listener = TcpListener::bind("127.0.0.1:0")?;
                let port = listener.local_addr()?.port();
                drop(listener);
                let token = format!("{}{}", uuid::Uuid::new_v4(), uuid::Uuid::new_v4());
                let base = format!("http://127.0.0.1:{}", port);
                let child = spawn_worker(&executable, &base, &token, &log_path)?;
                (Some(child), base, token)
            } else if cfg!(debug_assertions) {
                (None, "http://127.0.0.1:8765".to_string(), String::new())
            } else {
                return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
                    "Packaged AI worker is missing from application resources").into());
            };
            app.manage(WorkerState { child: Mutex::new(child), executable, log_path, base, token });
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![worker_connection, worker_status, restart_worker, set_compact, app_version])
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::Destroyed = event {
                if let Some(state) = window.try_state::<WorkerState>() {
                    if let Ok(mut guard) = state.child.lock() {
                        if let Some(mut child) = guard.take() {
                            let _ = child.kill();
                            let _ = child.wait();
                        }
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("Unable to start AI Interview Studio");
}

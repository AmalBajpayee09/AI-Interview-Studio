use std::{
    net::TcpListener,
    process::{Child, Command, Stdio},
    sync::Mutex,
};
use serde::Serialize;
use tauri::{LogicalSize, Manager, Size};

struct WorkerState {
    child: Mutex<Option<Child>>,
    base: String,
    token: String,
}

#[derive(Serialize)]
struct WorkerConnection { base: String, token: String }

/// The token is scoped to the local user's desktop window and is never persisted to disk.
#[tauri::command]
fn worker_connection(state: tauri::State<'_, WorkerState>) -> WorkerConnection {
    WorkerConnection { base: state.base.clone(), token: state.token.clone() }
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
            let (child, base, token) = if executable.is_file() {
                // A fresh ephemeral port prevents accidental reuse of other local servers.
                let listener = TcpListener::bind("127.0.0.1:0")?;
                let port = listener.local_addr()?.port();
                drop(listener);
                let token = format!("{}{}", uuid::Uuid::new_v4(), uuid::Uuid::new_v4());
                let child = Command::new(&executable)
                    .env("STUDIO_PORT", port.to_string())
                    .env("STUDIO_WORKER_TOKEN", &token)
                    .stdin(Stdio::null())
                    .stdout(Stdio::null())
                    .stderr(Stdio::null())
                    .spawn()?;
                (Some(child), format!("http://127.0.0.1:{}", port), token)
            } else if cfg!(debug_assertions) {
                // Development can explicitly run the standalone local worker.
                (None, "http://127.0.0.1:8765".to_string(), String::new())
            } else {
                // Incomplete release: fail closed instead of trusting an unrelated local service.
                (None, "http://127.0.0.1:0".to_string(), String::new())
            };
            app.manage(WorkerState { child: Mutex::new(child), base, token });
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![worker_connection, set_compact, app_version])
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

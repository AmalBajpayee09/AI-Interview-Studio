# Optional isolated programming practice (v0.3)

The code workspace now supports syntax checking even without Docker. Actual execution is **disabled** unless Docker Desktop is installed and the Linux containers engine is running. The Docker runner does NOT run user programs in the main worker or on the host.

Opt in separately by installing Docker Desktop from https://www.docker.com/products/docker-desktop/ and pulling the language image you want:

```powershell
docker info
docker pull python:3.11-alpine
docker pull node:22-alpine
docker pull gcc:14
docker pull eclipse-temurin:21-jdk
```

Then use Coding & DSA > Run isolated test. Java requires `public class Main`; C++ requires `main`; Python/JS execute `Main.py`/`Main.js` respectively. `stdin` and optional exact expected stdout are supported. The response reports exit status and elapsed time; it does not claim access to unknown hidden tests. SQL has an independent read-only SQLite practice path.

Docker runs as a nonroot user with no network, all Linux capabilities dropped, no-new-privileges, read-only root, a read-only mounted temporary source directory, writable temporary in-container work directory, CPU/memory/pids limits, and short timeouts. A Docker engine/VM or container escape vulnerability could still defeat this isolation; do not describe the result as a formally proved sandbox. Client output buffers may fill under malicious output volume. A process killed by timeout triggers a `docker rm -f` attempt against its container ID. The Docker engine must be trusted and controlled by the local user. Without Docker or required images, code execution returns an explicit error instead of running unsandboxed.

No Docker engine or image was available in the build environment; unit tests mock the Docker invocation to check the command and fail-closed behavior. A real Windows container runner requires clean-VM testing.

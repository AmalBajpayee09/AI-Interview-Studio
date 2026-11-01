# LLD — contracts and data

## Session

`Session { id: UUID, title: string, created: UnixSeconds, updated: UnixSeconds }`. Database `sessions` references `turns` with `ON DELETE CASCADE`; `turns` stores input question, full response, mode, provider, elapsed_ms and created timestamp.

## Ask request and streaming response

`AskBody { session_id: UUID, question: string[1..10000], mode: hint|short|detailed|code|diagram|verify|follow-up, provider: ollama|cloud, model?: string }`.

`POST /api/ask/stream` sends `text/event-stream` with JSON lines of `meta`, `token`, `done`, and `error` events. `meta` includes classifier category and unverified marker. `done` includes measured latency. Partial results are not persisted unless generation completes.

## Assessment

`Question { id, stem, options:[{label,text}], correct:string|string[], explanation?, section?, points? }`; correct answers and explanations are **removed** from the list API until submission. Assessment durations 30..14400 seconds. Client uses Date.now deadline for display; API validates `started` range but is not tamper-resistant proctoring.

`Attempt { answers: id -> label|string[], started: unix seconds, negative_marking: number [0..1] }`. Score is sum(points for exact correct selections) minus `negative_marking * points` for wrong selections. Unanswered score zero. Percent clamps negative final scores to zero.

## Document

Uploaded content extracted with file byte caps and OCR fallibility warning. Only manually saved normalized text is inserted into `documents`. Lexical snippets are passed to selected AI model; no embeddings required. Keys are read from the process environment, never stored in DB.

## Audio

`POST /api/transcribe` accepts a single user-provided `.webm/.wav/.mp3/.ogg/.m4a` max 10MB. Lazy optional faster-whisper CPU int8 model (default tiny). Audio is kept in a temporary file only for processing and then deleted. No diarization or continuous loopback system audio in current implementation.

## Schema migration

`db.initialize()` creates sessions, turns, documents, assessments and attempts tables and indices in SQLite and sets `PRAGMA user_version=2`. Migrations are idempotent; fresh startup cleans old data based on configured retention.

# Cloud model setup

Default: `ALLOW_CLOUD=false`. Cloud requests are unavailable without user-supplied `OPENAI_API_KEY` and `ALLOW_CLOUD=true`; keys are loaded from environment, not stored in SQLite. Get keys and check current model entitlement at https://platform.openai.com/.

In your local project `.env` (never commit this file):

```ini
ALLOW_CLOUD=true
OPENAI_API_KEY=YOUR_PRIVATE_VALUE
CLOUD_MODEL=gpt-4.1-mini
```

Restart worker after editing. Select Cloud in practice UI. The adapter uses the provider's Chat Completions streaming endpoint over TLS. Only explicitly chosen cloud practice calls are sent; current question, recent session turns and selected document snippets are included. Check account quota, model access, and applicable usage prices. To stop cloud processing, change `ALLOW_CLOUD=false` and restart. No automatic cloud fallback is enabled.

**Warning:** `.env` is plaintext. Set restrictive OS file permissions; native Windows credential vault support is not yet implemented. Do not put sensitive personal data or third-party recordings into cloud requests without consent.

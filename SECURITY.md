# Security

## Current controls
- Secrets are read through environment variables; no provider key is bundled in frontend code.
- API input validation is used for query parameters and Copilot payloads.
- CORS is restricted to local frontend origin.
- Raw source data is preserved unchanged.

## Known implementation limits
- The current demonstration has no implemented password/user database or protected authenticated routes.
- Deployment authentication and production secret management remain integration tasks.
- Uploaded-file authentication and persistent audit storage require a production identity provider and database.

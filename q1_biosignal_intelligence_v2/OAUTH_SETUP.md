# Enable Google and GitHub sign-in

The local username/password sign-in and account creation work without OAuth setup. Google and GitHub sign-in require OAuth client credentials owned by you. Never send client secrets in chat or commit them to GitHub.

## 1. Create the secrets file

Inside the project folder create `.streamlit` and then create `.streamlit/secrets.toml` (keep it private; `.gitignore` excludes it):

```toml
[google]
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
redirect_uri = "http://localhost:8501"

[github]
client_id = "YOUR_GITHUB_CLIENT_ID"
client_secret = "YOUR_GITHUB_CLIENT_SECRET"
redirect_uri = "http://localhost:8501"
```

## 2. Google OAuth setup

1. Open Google Cloud Console: https://console.cloud.google.com/
2. Create/select a project and configure the OAuth consent screen.
3. Create an OAuth Client ID of type **Web application**.
4. Add `http://localhost:8501` to **Authorized redirect URIs**. Add the matching JavaScript origin if the console asks for it.
5. Copy the client ID and client secret into the `[google]` section above.
6. While the consent screen is in Testing, add your Google account as a test user.

## 3. GitHub OAuth setup

1. Open https://github.com/settings/developers and choose **OAuth Apps → New OAuth App**.
2. Set Homepage URL to `http://localhost:8501` and Authorization callback URL to `http://localhost:8501`.
3. Register the app, then copy its Client ID and generate a Client Secret.
4. Put those values in the `[github]` section above.

## 4. Install and run

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Use the exact redirect/callback URL configured in each provider. If you deploy the app, register the deployed HTTPS URL too and update `redirect_uri` in secrets. OAuth providers may reject callbacks that do not match exactly.

## Important security notes

- Keep `secrets.toml` private and do not upload it to public repositories.
- This file-based local account system is a student prototype, not production-grade authentication. Do not deploy it publicly with sensitive data.
- The current local password storage uses a basic SHA-256 hash and should be replaced with a proper password-hashing/session solution before production.
- OAuth login establishes a provider identity for this prototype; it does not provide medical-data authorization or production account management.
- Forgot-password recovery is not implemented for local accounts.

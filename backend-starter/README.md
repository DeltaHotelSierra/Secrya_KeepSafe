# Secrya KeepSafe Backend Service

Flask-based backend service that bridges the browser extension to Gmail API and the Secrya analysis engine.

## Features

- OAuth 2.0 authentication with Google
- Gmail API integration
- Email retrieval as .eml format (RFC 2822)
- Integration with Secrya analysis engine
- RESTful API for the browser extension
- CORS support for extension communication
- Comprehensive error handling and logging

## Setup

### Prerequisites

- Python 3.9+
- Google Cloud Project with Gmail API enabled
- OAuth 2.0 credentials

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google OAuth credentials
   ```

4. **Create required directories:**
   ```bash
   mkdir -p logs
   mkdir -p reports
   ```

## Google OAuth Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "Secrya KeepSafe"
3. Enable Gmail API (APIs & Services → Library → Gmail API)

### 2. Create OAuth Credentials

1. Go to APIs & Services → Credentials
2. Create OAuth 2.0 Client ID:
   - Application type: Desktop (for development)
   - Authorized redirect URIs:
     - `http://localhost:5000/auth/callback`
     - `urn:ietf:wg:oauth:2.0:oob` (for manual token entry if needed)
3. Download credentials as JSON

### 3. Add Email for Testing

Since the app is in development:
1. Go to OAuth consent screen
2. Add test users (your Gmail address)

## Running the Backend

### Development Mode

```bash
python app.py
```

The service will start on `http://localhost:5000`

### Test Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "ok", "service": "Secrya KeepSafe Backend"}
```

## API Endpoints

### Health Check
- **GET** `/health`
- Returns service status

### Get Emails List
- **GET** `/api/emails?query=&max_results=10`
- **Headers:** `Authorization: Bearer {token}`
- Returns list of emails from inbox

### Analyze Email
- **POST** `/api/analyze-email`
- **Headers:** `Authorization: Bearer {token}`
- **Body:** `{"email_id": "gmail_message_id"}`
- Returns analysis result with risk score and indicators

### Analyze URL
- **POST** `/api/analyze-url`
- **Headers:** `Authorization: Bearer {token}`
- **Body:** `{"url": "https://example.com"}`
- Returns URL security analysis

### Get User Info
- **GET** `/api/user`
- **Headers:** `Authorization: Bearer {token}`
- Returns user profile information

## Example Requests

### Get Emails
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/emails?max_results=5
```

### Analyze Email
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email_id": "12345"}' \
  http://localhost:5000/api/analyze-email
```

### Analyze URL
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-domain.com"}' \
  http://localhost:5000/api/analyze-url
```

## Response Format

### Successful Analysis Response
```json
{
  "success": true,
  "email_id": "12345",
  "risk_level": "MEDIUM",
  "risk_score": 6.5,
  "indicators": [
    "Urgency language",
    "Link mismatch"
  ],
  "explanations": [
    "Contains urgent keywords",
    "Sender domain doesn't match URL"
  ],
  "recommendations": [
    "Verify through official channel"
  ],
  "timestamp": "2026-05-13T10:30:00"
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## Architecture

```
Browser Extension (Frontend)
         ↓
  OAuth Token
         ↓
    ┌─────────────────────┐
    │  Flask Backend      │
    │  - OAuth handling   │
    │  - Gmail API client │
    │  - Token mgmt       │
    └─────────────────────┘
         ↓
    Gmail API (Google)
         ↓
    .eml File
         ↓
    Secrya Analysis
```

## Project Structure

```
backend-starter/
├── app.py              # Main Flask application
├── gmail_api.py        # Gmail API integration module
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # This file
└── logs/              # Application logs (created at runtime)
```

## Troubleshooting

### Token Expired
- The backend handles token refresh automatically
- If error persists, re-authenticate in the extension

### Gmail API Error
- Verify OAuth credentials in `.env`
- Check that Gmail API is enabled in Google Cloud Console
- Confirm test user email is added to OAuth consent screen

### CORS Issues
- Ensure extension ID is in `CORS_ALLOWED_ORIGINS`
- Check extension manifest.json has correct permissions

### Connection Refused
- Verify backend is running on `localhost:5000`
- Check firewall isn't blocking port 5000
- Review logs in `logs/` directory

## Security Notes

1. **Never commit** `.env` file with real credentials
2. **Use HTTPS** in production (implement SSL/TLS)
3. **Validate all** input from extension
4. **Implement** rate limiting for production
5. **Store tokens** securely in extension storage
6. **Audit logs** regularly for suspicious activity

## Logging

Logs are saved to `logs/secrya_backend.log`

View recent logs:
```bash
tail -f logs/secrya_backend.log
```

## Development Tips

### Enable Debug Mode
```python
app.run(debug=True)  # In app.py
```

### Test Gmail Integration
```python
from gmail_api import GmailAPIClient

client = GmailAPIClient(access_token='your_token')
profile = client.get_user_profile()
print(profile)
```

### Mock Responses for Testing
See `tests/` directory for example test files (to be created)

## Next Steps

1. Configure Google OAuth credentials
2. Install dependencies
3. Run backend service
4. Configure and test browser extension
5. Integrate with Secrya analysis engine
6. Deploy to production with security hardening

## License

Part of Secrya KeepSafe project

## Support

For issues or questions, refer to the main project documentation.

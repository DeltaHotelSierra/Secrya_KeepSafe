# Secrya KeepSafe Browser Extension Proposal
## Email Integration via Gmail API & .eml File Analysis

### Overview
This proposal outlines a browser extension that connects Secrya KeepSafe to Gmail (and potentially other email providers) to retrieve and analyze emails directly without manual file downloads.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   BROWSER EXTENSION (Frontend)               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Gmail Integration UI                                  │ │
│  │  - OAuth 2.0 Login                                     │ │
│  │  - Email Selection Interface                           │ │
│  │  - Real-time Analysis Display                          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    Chrome Extension APIs
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Gmail API / Local Backend Service              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - OAuth 2.0 Token Management                          │ │
│  │  - Gmail API Integration                               │ │
│  │  - .eml File Retrieval                                 │ │
│  │  - Message Parsing                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
                   RESTful API / IPC
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Secrya KeepSafe Analysis Engine                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Python Backend (Existing)                             │ │
│  │  - analysis.py (email parsing)                         │ │
│  │  - url_security.py (link analysis)                     │ │
│  │  - report.py (report generation)                       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Browser Extension (Chrome/Firefox/Edge)

#### Structure:
```
secrya-extension/
├── manifest.json          # Extension configuration
├── src/
│   ├── popup/
│   │   ├── popup.html     # Extension UI
│   │   ├── popup.js       # UI logic & Gmail integration
│   │   └── popup.css      # Styling
│   ├── background/
│   │   ├── background.js  # Service worker/background script
│   │   └── oauth.js       # OAuth 2.0 handling
│   ├── content/
│   │   └── content.js     # Content script (if needed)
│   └── icons/
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
└── dist/                  # Build output
```

#### Key Features:
- **OAuth 2.0 Login**: Users authenticate with their Google account securely
- **Email List View**: Display inbox with preview
- **One-Click Analysis**: Select and analyze emails
- **Result Display**: Show risk score, indicators, and recommendations
- **History**: Track analyzed emails

#### manifest.json example:
```json
{
  "manifest_version": 3,
  "name": "Secrya KeepSafe",
  "version": "1.0.0",
  "description": "Analyze phishing emails directly from Gmail",
  "permissions": [
    "identity",
    "identity.email"
  ],
  "host_permissions": [
    "https://www.googleapis.com/*"
  ],
  "action": {
    "default_popup": "src/popup/popup.html",
    "default_icons": {
      "16": "src/icons/icon16.png",
      "48": "src/icons/icon48.png",
      "128": "src/icons/icon128.png"
    }
  },
  "background": {
    "service_worker": "src/background/background.js"
  },
  "oauth2": {
    "client_id": "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
    "scopes": [
      "https://www.googleapis.com/auth/gmail.readonly"
    ]
  }
}
```

---

### 2. Local Backend Service (Python/Flask or FastAPI)

This service runs locally and acts as a bridge between the browser extension and Secrya KeepSafe.

#### Purpose:
- Handles OAuth 2.0 token management
- Calls Gmail API to retrieve emails
- Converts email to .eml format
- Communicates with Python analysis engine
- Returns results to the extension

#### Stack Options:

**Option A: Flask (Lightweight)**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from email_handler import EmailHandler
from phishing_tool import analysis

app = Flask(__name__)
CORS(app)

@app.route('/analyze-email', methods=['POST'])
def analyze_email():
    email_id = request.json.get('email_id')
    gmail_token = request.json.get('token')
    
    # Fetch email via Gmail API
    email_content = fetch_gmail_email(email_id, gmail_token)
    
    # Convert to .eml format
    eml_content = convert_to_eml(email_content)
    
    # Analyze using existing Secrya logic
    result = analysis.analyze_email(eml_content)
    
    return jsonify(result)

@app.route('/auth/callback', methods=['POST'])
def auth_callback():
    code = request.json.get('code')
    token = exchange_code_for_token(code)
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(localhost, 5000)
```

**Option B: FastAPI (Modern, Async)**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from phishing_tool import analysis

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["chrome-extension://..."])

@app.post("/analyze-email")
async def analyze_email(email_id: str, token: str):
    async with httpx.AsyncClient() as client:
        # Fetch from Gmail API
        email_content = await fetch_gmail_email(email_id, token, client)
    
    # Convert and analyze
    result = analysis.analyze_email(email_content)
    return result
```

---

### 3. Gmail API Integration

#### Required Setup:
1. Create Google Cloud Project
2. Enable Gmail API
3. Create OAuth 2.0 credentials (Desktop/Extension)
4. Configure authorized redirect URIs

#### Email Retrieval Flow:

```python
# get_email_as_eml.py
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.oauthlib.flow import InstalledAppFlow
from google.api_core import gapic_v1
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class GmailHandler:
    def __init__(self, token):
        self.service = build('gmail', 'v1', credentials=token)
    
    def get_email_as_eml(self, message_id):
        """Retrieve Gmail email and convert to .eml format"""
        try:
            # Get full message with headers
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='raw'
            ).execute()
            
            # raw format returns base64 encoded RFC 2822 format (.eml)
            raw_email = base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))
            return raw_email.decode('utf-8')
        
        except Exception as e:
            print(f"Error retrieving email: {e}")
            return None
    
    def list_emails(self, query='', max_results=10):
        """List emails from inbox"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            return results.get('messages', [])
        except Exception as e:
            print(f"Error listing emails: {e}")
            return []
```

---

### 4. Data Flow Diagram

```
User clicks on email in Gmail
        ↓
Extension UI displays email preview
        ↓
User clicks "Analyze" button
        ↓
Extension sends request to local backend with:
  - Gmail message ID
  - Access token
        ↓
Backend fetches email from Gmail API as .eml
        ↓
Backend passes .eml to Secrya analysis engine
  ├─ analysis.analyze_email(eml_content)
  ├─ url_security checks (if applicable)
  └─ report generation
        ↓
Backend returns JSON result:
  {
    "risk_level": "MEDIUM",
    "risk_score": 6.0,
    "indicators": [...],
    "recommendations": [...]
  }
        ↓
Extension UI displays risk badge & results
        ↓
User can save report or mark as spam
```

---

## Implementation Steps

### Phase 1: Backend Service (1-2 weeks)
- [ ] Create Flask/FastAPI service
- [ ] Implement OAuth 2.0 flow
- [ ] Implement Gmail API integration
- [ ] Create email retrieval functions
- [ ] Add error handling & logging

### Phase 2: Browser Extension (2-3 weeks)
- [ ] Set up extension project structure
- [ ] Create manifest.json
- [ ] Build popup UI (HTML/CSS)
- [ ] Implement OAuth flow in extension
- [ ] Create email list view
- [ ] Add analysis display

### Phase 3: Integration (1 week)
- [ ] Connect extension to backend
- [ ] Test end-to-end flow
- [ ] Add caching/optimization
- [ ] Security review

### Phase 4: Enhancement (Optional)
- [ ] Support Outlook, Apple Mail
- [ ] Add bulk analysis
- [ ] Implement machine learning scoring
- [ ] Create dashboard for analysis history
- [ ] Add phishing report submission

---

## Security Considerations

### 1. OAuth 2.0 Token Management
- Store tokens securely (not in localStorage)
- Use extension's secure storage API
- Implement token refresh logic
- Auto-logout after inactivity

### 2. Data Privacy
- .eml files processed locally only
- No data transmitted to external servers (except Gmail API)
- Clear user consent for OAuth scopes
- HTTPS only for all communications

### 3. API Key Protection
- Store Google Client ID/Secret securely
- Never expose in extension code
- Use backend service as middleware
- Implement rate limiting

### 4. Code Security
- Input validation on all email content
- Sanitize HTML rendering
- Content Security Policy (CSP) headers
- Regular security audits

---

## .eml File Format Explanation

The Gmail API `raw` format returns RFC 2822 compliant email format (.eml):

```
From: sender@example.com
To: recipient@example.com
Subject: Test Email
Date: May 13, 2026 10:30:00 GMT
Message-ID: <unique-id@example.com>
Content-Type: text/plain; charset="UTF-8"

This is the email body.
Links: https://example.com
```

**Why .eml?**
- Standard email format
- Compatible with Secrya's existing parser
- Preserves all headers and metadata
- Easy to extract sender, links, headers

---

## User Workflow Example

```
1. User installs extension from Chrome Web Store
   ↓
2. User clicks Secrya extension icon
   ↓
3. Extension shows login screen
   ↓
4. User clicks "Connect Gmail" → OAuth consent
   ↓
5. Gmail inbox loaded in popup
   ↓
6. User selects suspicious email
   ↓
7. Clicks "Analyze" button
   ↓
8. Risk assessment appears:
   ┌─────────────────────┐
   │ RISK: MEDIUM 6.5/10 │
   │ ⚠️ Urgent language  │
   │ ⚠️ Link mismatch    │
   │ ✅ Valid SPF        │
   └─────────────────────┘
   ↓
9. User can:
   - View detailed report
   - Mark as spam
   - Save analysis
   - Export report
```

---

## Technology Stack Summary

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | HTML/CSS/JavaScript | Native, no build tools needed |
| Backend | Flask/FastAPI | Lightweight, Python integration |
| Gmail API | Google Cloud | Official, reliable |
| Email Parsing | Python email lib | Already used in Secrya |
| Analysis | Existing Secrya code | Reuse current logic |
| Storage | Browser storage + local | Privacy-first |

---

## Alternatives Considered

### Option 1: Web-based Application
- ❌ Requires email forwarding (privacy risk)
- ❌ More server infrastructure
- ✅ Cross-platform support

### Option 2: Direct Gmail Integration (no backend)
- ❌ Can't run Python analysis in browser
- ❌ Security issues with exposing tokens
- ✅ Simpler deployment

### Option 3: Native Electron App
- ✅ More powerful
- ❌ Overkill for this use case
- ❌ Larger download size

---

## Next Steps

1. **Validate Requirements**: Confirm OAuth scope and Gmail API access level
2. **Set Up Google Cloud Project**: Create credentials for development
3. **Prototype Backend**: Create Flask service with basic email retrieval
4. **Test Gmail API**: Verify .eml retrieval and parsing
5. **Build Extension UI**: Create mockups and validate UX
6. **Integrate with Secrya**: Connect to existing analysis engine
7. **Security Review**: Audit OAuth flow and data handling
8. **Package & Deploy**: Prepare for Chrome Web Store / Firefox Add-ons

---

## Resources

- [Gmail API Docs](https://developers.google.com/gmail/api/guides)
- [Chrome Extension Docs](https://developer.chrome.com/docs/extensions/)
- [OAuth 2.0 Flow](https://developers.google.com/identity/protocols/oauth2)
- [RFC 2822 Email Format](https://tools.ietf.org/html/rfc2822)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

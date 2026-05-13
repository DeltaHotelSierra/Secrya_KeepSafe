# Secrya KeepSafe Browser Extension - Complete Setup Guide

A comprehensive guide to set up the browser extension, backend service, and Gmail integration for Secrya KeepSafe.

## Overview

```
BROWSER EXTENSION ←→ BACKEND SERVICE ←→ GMAIL API
   (Chrome)              (Flask)        (Google)
```

The extension communicates with your local Flask backend, which fetches emails from Gmail API and analyzes them using Secrya's engine.

---

## Prerequisites

- ✅ Python 3.9 or higher
- ✅ Google account with Gmail
- ✅ Chrome, Firefox, or Edge browser
- ✅ Secrya KeepSafe main project installed
- ✅ Basic command line knowledge

---

## Step 1: Google Cloud Setup (15 minutes)

### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a Project"** → **"New Project"**
3. Name: `Secrya KeepSafe`
4. Click **Create**
5. Wait for project to be created
6. Select the new project

### 1.2 Enable Gmail API

1. In the left menu, click **"APIs & Services"** → **"Library"**
2. Search for **"Gmail API"**
3. Click on it
4. Click **"ENABLE"**
5. Wait for enablement to complete

### 1.3 Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User type: **"External"**
   - Click **Create**
   - Fill in:
     - App name: `Secrya KeepSafe`
     - User support email: Your email
     - Developer contact info: Your email
   - Click **Save and Continue**
   - Click **Save and Continue** (on scopes page)
   - Add test user: Your Gmail address
   - Click **Save and Continue**
4. Back to credentials, click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
5. Application type: **"Desktop application"**
6. Name: `Secrya KeepSafe Backend`
7. Click **Create**
8. Click **Download JSON** (save as `credentials.json`)
9. Extract `client_id` and `client_secret` from the JSON file

**Important:** Keep your credentials secure! Never commit them to version control.

---

## Step 2: Backend Service Setup (20 minutes)

### 2.1 Create Backend Directory Structure

```bash
cd path/to/Secrya_KeepSafe
mkdir -p backend
cd backend
```

### 2.2 Set Up Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

- Flask (web framework)
- Flask-CORS (cross-origin support)
- google-auth (OAuth)
- google-api-python-client (Gmail API)
- python-dotenv (configuration)

### 2.4 Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add:

```
GOOGLE_CLIENT_ID=your_client_id_from_step_1
GOOGLE_CLIENT_SECRET=your_client_secret_from_step_1
FLASK_ENV=development
BACKEND_HOST=localhost
BACKEND_PORT=5000
```

### 2.5 Test Backend

```bash
python app.py
```

Expected output:

```
 * Running on http://localhost:5000
 * Press CTRL+C to quit
```

Test in another terminal:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{ "status": "ok", "service": "Secrya KeepSafe Backend" }
```

✅ Backend is working! Press `CTRL+C` to stop it.

---

## Step 3: Browser Extension Setup (25 minutes)

### 3.1 Prepare Extension Files

Files are in `extension-starter/` directory:

```
extension-starter/
├── manifest.json
├── src/popup/
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── src/background/
│   └── background.js
└── src/icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

### 3.2 Create Extension Icons (Optional)

If icons don't exist, create 16x16, 48x48, and 128x128 PNG files.

Or use these minimal icon URLs in manifest for testing:

```json
"icons": {
  "16": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text x='2' y='12' font-size='14' font-weight='bold' fill='%23667eea'>S</text></svg>",
  "48": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'><rect fill='%23667eea' width='48' height='48'/><text x='12' y='36' font-size='24' font-weight='bold' fill='white'>S</text></svg>",
  "128": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'><rect fill='%23667eea' width='128' height='128'/><text x='32' y='96' font-size='64' font-weight='bold' fill='white'>S</text></svg>"
}
```

### 3.3 Update Manifest with OAuth Credentials

Edit `extension-starter/manifest.json`:

Replace:

```json
"oauth2": {
  "client_id": "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
}
```

With your actual Client ID from Step 1.

### 3.4 Update Backend URL (if needed)

Edit `extension-starter/src/popup/popup.js`:

If backend is on different machine/port:

```javascript
const CONFIG = {
  BACKEND_URL: "http://your-backend-host:5000",
  // ...
};
```

### 3.5 Load Extension in Chrome

1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable **"Developer mode"** (top right toggle)
4. Click **"Load unpacked"**
5. Select `extension-starter/` folder
6. ✅ Extension installed! Look for 🔐 icon in toolbar

### 3.6 Load Extension in Firefox

1. Open Firefox
2. Go to `about:debugging`
3. Click **"This Firefox"**
4. Click **"Load Temporary Add-on..."**
5. Select `extension-starter/manifest.json`
6. ✅ Extension installed!

---

## Step 4: Integration Test (10 minutes)

### 4.1 Start Backend Service

Open a terminal in `backend-starter/`:

```bash
# Activate venv if not already
venv\Scripts\activate  # Windows or source venv/bin/activate

# Start backend
python app.py
```

Output:

```
Starting Secrya KeepSafe Backend Service
 * Running on http://localhost:5000
```

### 4.2 Test Extension

1. Click Secrya KeepSafe extension icon
2. Click **"Login with Google"**
3. Google OAuth consent screen appears
4. Approve permissions
5. Click **Refresh** in the extension popup
6. Your Gmail inbox should appear
7. ✅ Integration working!

### 4.3 Analyze a Test Email

1. From your Gmail inbox, select an email
2. Click **"Analyze"** button in extension
3. Wait for analysis (should show loading spinner)
4. Results appear with risk score and indicators
5. ✅ End-to-end flow working!

---

## Step 5: Configuration & Customization

### 5.1 Adjust Risk Thresholds

In `backend-starter/app.py`, modify analysis parameters:

```python
# Example: Adjust sensitivity
result = analysis.analyze_email(eml_content, sensitivity='high')
```

### 5.2 Enable Report Saving

In backend `.env`:

```
SECRYA_ENABLE_REPORT_SAVING=True
SECRYA_REPORTS_DIR=./reports
```

### 5.3 Add Custom Email Filters

Edit `extension-starter/src/popup/popup.js`:

```javascript
async function loadEmails() {
  // Add custom filter
  const query = "from:suspicious-sender@example.com";

  const response = await fetch(
    `${CONFIG.BACKEND_URL}/api/emails?query=${encodeURIComponent(query)}`,
  );
  // ...
}
```

### 5.4 Customize UI Theme

Edit `extension-starter/src/popup/popup.css`:

```css
/* Change primary color */
body {
  background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

---

## Step 6: Running in Production

### 6.1 Get OAuth Approval

Before deploying to Chrome Web Store:

1. OAuth consent screen must be set to "Production"
2. Privacy policy and terms required
3. Submit OAuth for verification

### 6.2 Set Up HTTPS

For production, Flask must use HTTPS:

```python
# In app.py
from flask_talisman import Talisman

Talisman(app)  # Enable HTTPS enforcement
```

Or use nginx/Apache as reverse proxy with SSL.

### 6.3 Deploy Backend

Options:

- **Heroku**: Easy, free tier available
- **AWS**: EC2 instance with proper scaling
- **DigitalOcean**: Simple droplet deployment
- **On-premise**: Your own server

Example Heroku deployment:

```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
git push heroku main
```

### 6.4 Update Extension for Production

Edit manifest.json:

```json
"oauth2": {
  "client_id": "YOUR_PRODUCTION_CLIENT_ID"
}
```

Edit popup.js:

```javascript
const CONFIG = {
  BACKEND_URL: "https://your-production-backend.com",
};
```

### 6.5 Publish to Chrome Web Store

1. Create developer account ($5 fee)
2. Upload extension ZIP
3. Add screenshots and description
4. Submit for review
5. Published in 24-48 hours

---

## Troubleshooting Guide

### Issue: "Extension failed to load"

**Solution:**

1. Check manifest.json syntax (validate JSON online)
2. Verify all file paths exist
3. Check console for errors (F12)
4. Reload extension (click reload icon)

### Issue: "Login failed" error

**Solution:**

1. Is backend running? (`python app.py`)
2. Is backend URL correct in popup.js?
3. Is `BACKEND_URL` pointing to `http://localhost:5000`?
4. Check backend console for error messages

### Issue: "No emails appear"

**Solution:**

1. Are you logged in? (Check user email displayed)
2. Is Gmail API enabled? (Check Google Cloud Console)
3. Do you have emails in your inbox?
4. Check extension console (F12) for API errors

### Issue: "Analysis not working"

**Solution:**

1. Backend running?
2. Token valid? (Try logging out and back in)
3. Is Secrya module imported? Check backend console
4. Check backend logs: `tail -f logs/secrya_backend.log`

### Issue: "CORS Error"

**Solution:**

1. In backend `.env`, verify CORS settings
2. Backend should have: `allow_origins=['chrome-extension://*']`
3. Restart backend after changing `.env`

### Issue: "Token expired"

**Solution:**

1. Click **Logout** in extension
2. Click **Login with Google** again
3. Backend handles refresh automatically

---

## File Structure Summary

```
Secrya_KeepSafe/
├── backend-starter/
│   ├── app.py                 # Flask main application
│   ├── gmail_api.py          # Gmail API client
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   ├── .env                  # Your configuration (don't commit)
│   ├── logs/                 # Application logs
│   └── README.md
│
├── extension-starter/
│   ├── manifest.json         # Extension config
│   ├── src/
│   │   ├── popup/
│   │   │   ├── popup.html
│   │   │   ├── popup.js
│   │   │   └── popup.css
│   │   ├── background/
│   │   │   └── background.js
│   │   └── icons/
│   │       ├── icon16.png
│   │       ├── icon48.png
│   │       └── icon128.png
│   └── README.md
│
├── phishing_tool/            # Existing Secrya code
│   ├── analysis.py
│   ├── url_security.py
│   └── ...
│
└── BROWSER_EXTENSION_PROPOSAL.md
```

---

## Environment Checklist

Before deploying, verify:

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth credentials generated (client_id, client_secret)
- [ ] Backend `.env` configured with credentials
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Backend tested locally (health check passes)
- [ ] Extension manifest.json has correct client_id
- [ ] Extension files in correct directory structure
- [ ] Extension loads without errors in browser
- [ ] OAuth login works
- [ ] Gmail inbox loads
- [ ] Email analysis works end-to-end

---

## Next Steps

1. ✅ Complete setup following this guide
2. Test thoroughly with various emails
3. Add custom email filtering/analysis
4. Deploy backend to production server
5. Prepare extension for Chrome Web Store
6. Submit for review and publication
7. Monitor for issues and user feedback
8. Plan additional features (bulk analysis, ML scoring, etc.)

---

## Support & Resources

- **Gmail API Docs**: https://developers.google.com/gmail/api
- **Chrome Extension Docs**: https://developer.chrome.com/docs/extensions/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Google OAuth Guide**: https://developers.google.com/identity/protocols/oauth2
- **Security Best Practices**: https://cheatsheetseries.owasp.org/

---

## FAQ

**Q: Can I use this with Outlook/Apple Mail?**
A: Yes! Extend the `gmail_api.py` module with Outlook/Mail APIs. See proposal document.

**Q: Is my email data safe?**
A: Yes. Emails are analyzed locally or through Gmail API only. No third-party storage.

**Q: How often should I refresh my token?**
A: Automatic. Backend handles token refresh. Manual re-login needed only if error persists.

**Q: Can I deploy backend on shared hosting?**
A: Not easily. Needs Python environment. Use cloud platforms (Heroku, AWS, etc.) instead.

**Q: Will this work offline?**
A: No. Requires internet for Gmail API and OAuth. Can cache some data locally.

---

**Congratulations! You now have Secrya KeepSafe integrated with your Gmail inbox.** 🎉

For questions or issues, refer to component READMEs or the proposal document.

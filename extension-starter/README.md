# Secrya KeepSafe Browser Extension

Chrome/Firefox extension that integrates Secrya KeepSafe with Gmail for real-time phishing analysis.

## Features

✨ **Easy Installation** - One-click setup from Chrome Web Store
🔐 **Secure OAuth** - Direct Gmail authentication
📧 **Email Analysis** - Analyze emails right from Gmail
⚡ **Real-time Results** - Instant phishing risk assessment
💾 **Report Saving** - Save analysis history
🎨 **Beautiful UI** - Modern, intuitive interface

## System Requirements

- Chrome 88+ / Firefox 89+ / Edge 88+
- Active internet connection
- Google/Gmail account
- Secrya KeepSafe backend service running locally

## Installation

### Option A: Load from Source (Development)

1. **Clone/Download** the extension source
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable **Developer Mode** (top right)
4. Click **Load unpacked**
5. Select the `extension-starter/` directory
6. Extension installed! Look for the 🔐 icon in your toolbar

### Option B: From Chrome Web Store (Coming Soon)

1. Open Chrome Web Store
2. Search for "Secrya KeepSafe"
3. Click **Add to Chrome**
4. Confirm permissions

## Configuration

### 1. Update Google OAuth Credentials

Edit `manifest.json` and replace:
```json
"oauth2": {
  "client_id": "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
}
```

Get your Client ID from [Google Cloud Console](https://console.cloud.google.com/)

### 2. Configure Backend URL

In `src/popup/popup.js`, update:
```javascript
const CONFIG = {
    BACKEND_URL: 'http://localhost:5000',
    // ...
};
```

### 3. Start Backend Service

Ensure the Flask backend is running:
```bash
cd ../backend-starter
python app.py
```

## Usage

### First Time Setup

1. Click the Secrya KeepSafe extension icon
2. Click **"Login with Google"**
3. Authenticate with your Gmail account
4. Grant permissions to read emails
5. Done! Extension is ready to use

### Analyze an Email

1. Open Gmail
2. Click Secrya KeepSafe extension icon
3. Your emails appear in the popup
4. Click any email to analyze
5. View risk assessment and recommendations
6. Optionally save the report

### Email Analysis Results

Results include:

- **Risk Level**: HIGH / MEDIUM / LOW
- **Risk Score**: 0-10 numerical score
- **Indicators**: Phishing signals detected
- **Recommendations**: Steps to take
- **Report**: Detailed analysis saved

## Project Structure

```
extension-starter/
├── manifest.json              # Extension configuration
├── src/
│   ├── popup/
│   │   ├── popup.html        # UI markup
│   │   ├── popup.js          # UI logic & Gmail integration
│   │   └── popup.css         # Styling
│   ├── background/
│   │   └── background.js     # Service worker & OAuth
│   ├── content/
│   │   └── content.js        # Content script (optional)
│   └── icons/
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
└── README.md
```

## API Integration

### Backend Communication

The extension communicates with the backend via HTTP requests:

```javascript
// Example: Analyze email
fetch('http://localhost:5000/api/analyze-email', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email_id: messageId })
});
```

### OAuth Flow

```
User clicks "Login"
    ↓
Extension calls chrome.identity.getAuthToken()
    ↓
Google OAuth consent screen
    ↓
Token stored in extension storage
    ↓
Sent to backend with each API request
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+K` | Toggle extension popup |
| `Cmd+Shift+K` | Toggle (Mac) |

(To be configured in manifest.json)

## Permissions Explained

The extension requests these permissions:

| Permission | Why |
|-----------|-----|
| `identity` | OAuth login to Gmail |
| `identity.email` | Get user's email address |
| `https://www.googleapis.com/*` | Gmail API access |
| `storage` | Store OAuth tokens securely |

## Troubleshooting

### Extension Won't Load

**Solution 1: Check manifest syntax**
```bash
# Look for JSON errors in manifest.json
```

**Solution 2: Verify file paths**
- Ensure all file paths in manifest.json exist
- Check icons directory has all required PNG files

### "Login Failed" Error

**Cause**: Backend service not running
```bash
cd backend-starter
python app.py
```

**Cause**: Invalid Google Client ID
- Verify in manifest.json matches your OAuth credentials
- Regenerate credentials in Google Cloud Console

### Emails Not Loading

**Cause**: Token expired
- Click "Logout" then "Login with Google" again

**Cause**: Gmail API not enabled
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Enable Gmail API for your project

### "CORS Error"

**Cause**: Backend not configured for extension
- In backend `.env`, set CORS origin to your extension ID:
```
chrome-extension://YOUR_EXTENSION_ID
```

### Analysis Not Working

1. Check backend service is running
2. Verify email has proper .eml format
3. Check browser console for errors (F12)
4. Review backend logs: `logs/secrya_backend.log`

## Development

### Enable Debug Mode

In Chrome:
1. `chrome://extensions/`
2. Find Secrya KeepSafe
3. Click "Details"
4. Enable "Allow access to file URLs"

In Firefox:
1. `about:debugging`
2. Check "Enable add-on debugging"

### View Console Logs

1. Open extension popup
2. Right-click → Inspect
3. View Console tab for logs

### Reload Extension

While developing, reload after changes:
- Chrome: Click reload icon on extension card
- Firefox: Click refresh on extension details page
- Both: `F5` in browser

## Testing

### Test with Sample Email

1. Load a test .eml file through the backend
2. Verify analysis results are correct
3. Check indicators match expected output

### Test OAuth Flow

1. Login with test Gmail account
2. Verify token is stored securely
3. Verify token refresh works
4. Test logout clears data

## Deployment to Chrome Web Store

### Prerequisites

1. Google account
2. $5 developer registration fee
3. Completed extension files

### Steps

1. Create Chrome Web Store developer account
2. Upload extension ZIP file
3. Add description, screenshots, permissions explanations
4. Submit for review
5. Wait for approval (usually 24-48 hours)

### Preparation Checklist

- [ ] manifest.json is valid
- [ ] All files included
- [ ] Icons are 128x128 PNG
- [ ] Privacy policy written
- [ ] Terms of service reviewed
- [ ] No security issues detected
- [ ] Test on multiple browsers

## Performance Optimization

- Token cached locally (not re-requested)
- Email list paginated for large inboxes
- Analysis results cached temporarily
- UI responsive under 200ms

## Security Best Practices

✅ **Do:**
- Store tokens in `chrome.storage.local` (encrypted)
- Use HTTPS for all backend communication
- Validate all user input
- Clear cache on logout
- Request minimal permissions

❌ **Don't:**
- Store tokens in localStorage
- Send tokens in URL
- Cache sensitive data indefinitely
- Hardcode credentials
- Log sensitive information

## Privacy

- Emails processed locally or by Gmail API only
- No third-party tracking
- No data sold or shared
- Complies with GDPR, CCPA

## Support & Feedback

Report issues or suggest features:
- GitHub Issues: [project link]
- Email: support@secrya.example.com
- Discord: [community link]

## License

Open source under MIT license

## Contributing

We welcome contributions! See CONTRIBUTING.md for guidelines.

## Changelog

### v1.0.0 (Initial Release)
- OAuth Gmail integration
- Email analysis
- Real-time risk scoring
- Report generation
- Beautiful UI

See CHANGELOG.md for more details

## Credits

Developed as part of Secrya KeepSafe project

---

**Need Help?** Check troubleshooting section above or contact support.

// Configuration
const CONFIG = {
    BACKEND_URL: 'http://localhost:5000',
    TOKEN_STORAGE_KEY: 'secrya_gmail_token',
    USER_EMAIL_KEY: 'secrya_user_email'
};

// DOM Elements
const authSection = document.getElementById('authSection');
const mainSection = document.getElementById('mainSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const refreshBtn = document.getElementById('refreshBtn');
const emailList = document.getElementById('emailList');
const userEmail = document.getElementById('userEmail');
const authError = document.getElementById('authError');
const analysisResult = document.getElementById('analysisResult');
const resultDetails = document.getElementById('resultDetails');
const closeResultBtn = document.getElementById('closeResultBtn');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    const token = await getStoredToken();
    if (token) {
        await showMainSection(token);
    } else {
        showAuthSection();
    }
});

// Event Listeners
loginBtn.addEventListener('click', handleLogin);
logoutBtn.addEventListener('click', handleLogout);
refreshBtn.addEventListener('click', () => loadEmails());
closeResultBtn.addEventListener('click', () => {
    analysisResult.classList.add('hidden');
});

// Auth Functions
async function handleLogin() {
    try {
        loginBtn.disabled = true;
        const token = await chrome.identity.getAuthToken({ interactive: true });
        
        if (token) {
            const email = await getUserEmail(token);
            await storeToken(token, email);
            await showMainSection(token);
            authError.classList.add('hidden');
        }
    } catch (error) {
        console.error('Login error:', error);
        authError.textContent = `Login failed: ${error.message}`;
        authError.classList.remove('hidden');
    } finally {
        loginBtn.disabled = false;
    }
}

async function handleLogout() {
    const token = await getStoredToken();
    if (token) {
        chrome.identity.removeCachedAuthToken({ token });
    }
    await chrome.storage.local.clear();
    showAuthSection();
    emailList.innerHTML = '';
}

async function getUserEmail(token) {
    try {
        const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        return data.email;
    } catch (error) {
        console.error('Error fetching user email:', error);
        return 'Unknown User';
    }
}

// Storage Functions
async function storeToken(token, email) {
    return new Promise((resolve) => {
        chrome.storage.local.set({
            [CONFIG.TOKEN_STORAGE_KEY]: token,
            [CONFIG.USER_EMAIL_KEY]: email
        }, resolve);
    });
}

async function getStoredToken() {
    return new Promise((resolve) => {
        chrome.storage.local.get(CONFIG.TOKEN_STORAGE_KEY, (result) => {
            resolve(result[CONFIG.TOKEN_STORAGE_KEY] || null);
        });
    });
}

async function getStoredEmail() {
    return new Promise((resolve) => {
        chrome.storage.local.get(CONFIG.USER_EMAIL_KEY, (result) => {
            resolve(result[CONFIG.USER_EMAIL_KEY] || 'User');
        });
    });
}

// UI Functions
function showAuthSection() {
    authSection.classList.remove('hidden');
    mainSection.classList.add('hidden');
}

async function showMainSection(token) {
    const email = await getStoredEmail();
    userEmail.textContent = email;
    authSection.classList.add('hidden');
    mainSection.classList.remove('hidden');
    await loadEmails();
}

// Email Functions
async function loadEmails() {
    try {
        const token = await getStoredToken();
        if (!token) return;

        emailList.innerHTML = '<div class="loading">Loading emails...</div>';
        
        const response = await fetch(`${CONFIG.BACKEND_URL}/api/emails`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayEmails(data.emails || []);
    } catch (error) {
        console.error('Error loading emails:', error);
        emailList.innerHTML = `<div class="loading" style="color: #c33;">Error: ${error.message}</div>`;
    }
}

function displayEmails(emails) {
    if (emails.length === 0) {
        emailList.innerHTML = '<div class="loading">No emails found</div>';
        return;
    }

    emailList.innerHTML = emails.map(email => `
        <div class="email-item" onclick="selectEmail('${email.id}', '${email.subject}')">
            <div class="email-subject">${email.subject}</div>
            <div class="email-from">From: ${email.from}</div>
            <div class="email-date">${email.date}</div>
        </div>
    `).join('');
}

// Analysis Functions
async function selectEmail(emailId, subject) {
    try {
        showLoadingSpinner(true);
        const token = await getStoredToken();

        const response = await fetch(`${CONFIG.BACKEND_URL}/api/analyze-email`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email_id: emailId })
        });

        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }

        const result = await response.json();
        displayAnalysisResult(result, subject);
    } catch (error) {
        console.error('Analysis error:', error);
        alert(`Analysis failed: ${error.message}`);
    } finally {
        showLoadingSpinner(false);
    }
}

function displayAnalysisResult(result, subject) {
    const riskLevel = result.risk_level || 'UNKNOWN';
    const riskScore = result.risk_score || 0;
    const indicators = result.indicators || [];
    const recommendations = result.recommendations || [];

    // Update risk badge
    const badge = document.getElementById('riskBadge');
    badge.className = `risk-badge risk-${riskLevel.toLowerCase()}`;
    badge.textContent = `${riskLevel} RISK - ${riskScore.toFixed(1)}/10`;

    // Build result details
    let html = `<div class="result-details">`;
    html += `<div class="result-section">
        <h4>📧 Email</h4>
        <p style="font-size: 12px; margin: 0;">${subject}</p>
    </div>`;

    if (indicators.length > 0) {
        html += `<div class="result-section">
            <h4>⚠️ Detected Indicators</h4>
            <ul class="result-list">
                ${indicators.map(ind => `<li class="indicator">${ind}</li>`).join('')}
            </ul>
        </div>`;
    }

    if (recommendations.length > 0) {
        html += `<div class="result-section">
            <h4>💡 Recommendations</h4>
            <ul class="result-list">
                ${recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>`;
    }

    html += `</div>`;
    resultDetails.innerHTML = html;
    analysisResult.classList.remove('hidden');
}

function showLoadingSpinner(show) {
    loadingSpinner.classList.toggle('hidden', !show);
}

// Error handling
window.addEventListener('error', (event) => {
    console.error('Extension error:', event.error);
});

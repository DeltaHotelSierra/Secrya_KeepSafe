/**
 * Background Service Worker for Secrya KeepSafe Extension
 * Handles OAuth token refresh and authentication
 */

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('Secrya KeepSafe extension installed');
        // You can open a setup page here if needed
    }
});

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getToken') {
        getAuthToken().then(token => {
            sendResponse({ token });
        });
        return true; // Keep the message channel open
    }
    
    if (request.action === 'removeToken') {
        chrome.identity.removeCachedAuthToken({ token: request.token });
        sendResponse({ success: true });
    }
});

// Get auth token
async function getAuthToken() {
    return new Promise((resolve, reject) => {
        chrome.identity.getAuthToken({ interactive: false }, (token) => {
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            } else {
                resolve(token);
            }
        });
    });
}

// Periodic token refresh (every 50 minutes)
setInterval(() => {
    chrome.identity.getAuthToken({ interactive: false }, (token) => {
        if (token) {
            // Token is refreshed automatically by calling getAuthToken
            console.log('Token refreshed');
        }
    });
}, 50 * 60 * 1000);

// Handle errors
chrome.runtime.onStartup.addListener(() => {
    console.log('Secrya KeepSafe service worker started');
});

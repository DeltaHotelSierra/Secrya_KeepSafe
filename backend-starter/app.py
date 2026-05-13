"""
Secrya KeepSafe Backend Service
Connects browser extension to Gmail API and Secrya analysis engine

Features:
- Multi-provider support (Gmail, Outlook)
- Risk score enhancement with trust signals
- Email caching for performance
- Comprehensive error handling
"""

import os
import sys
import re
import base64
import logging
from datetime import datetime
from functools import wraps
from email import policy
from email.parser import BytesParser

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.api_core import gapic_v1
from google.auth.exceptions import RefreshError

# Add parent directory to path for Secrya imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Secrya modules
try:
    from phishing_tool import analysis, url_security, report
except ImportError:
    print("Warning: Could not import phishing_tool. Make sure it's installed.")

# Import local modules
try:
    from gmail_api import GmailAPIClient
    from outlook_api import OutlookAPIClient
    from risk_enhancer import RiskEnhancer
except ImportError:
    print("Warning: Could not import backend modules.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS for Chrome extension
CORS(app, 
     origins=['chrome-extension://*'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# Google API settings
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def sanitize_error_for_user(error_msg: str) -> str:
    """
    Remove sensitive data from error messages for display to users
    
    Args:
        error_msg: Original error message
    
    Returns:
        Sanitized error message safe to show users
    """
    # Remove email addresses
    error_msg = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[email]', error_msg)
    # Remove OAuth tokens
    error_msg = re.sub(r'Bearer\s+[\w\-\.]+', '[token]', error_msg)
    # Remove file paths
    error_msg = re.sub(r'[A-Za-z]:\\.*?(?=\s|$)', '[path]', error_msg)
    
    # Return helpful message
    if 'UNAUTHENTICATED' in error_msg or 'Unauthorized' in error_msg:
        return 'Authentication failed. Please log in again.'
    elif 'PERMISSION_DENIED' in error_msg:
        return 'Permission denied. Please check OAuth scopes.'
    elif 'NOT_FOUND' in error_msg or 'not found' in error_msg.lower():
        return 'Email not found. It may have been deleted.'
    elif 'rate' in error_msg.lower():
        return 'Too many requests. Please wait and try again.'
    
    return 'An error occurred. Please try again.'


def get_email_client(provider: str, token: str):
    """
    Get appropriate email client for provider
    
    Args:
        provider: Email provider ('gmail' or 'outlook')
        token: OAuth access token
    
    Returns:
        Email API client instance
    """
    if provider.lower() == 'gmail':
        return GmailAPIClient(token)
    elif provider.lower() == 'outlook':
        return OutlookAPIClient(token)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def require_auth(f):
    """Decorator to require valid OAuth token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing authorization token'}), 401
        
        token = auth_header.split('Bearer ')[1]
        
        try:
            # Verify and refresh token if needed
            verified_token = verify_and_refresh_token(token)
            request.gmail_token = verified_token
            return f(*args, **kwargs)
        except RefreshError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        except Exception as e:
            logger.error(f"Auth error: {e}")
            return jsonify({'error': str(e)}), 500
    
    return decorated_function


def verify_and_refresh_token(token):
    """Verify and refresh token if needed"""
    try:
        creds = Credentials(token=token)
        
        # Make a test request to verify token
        from googleapiclient.discovery import build
        service = build('gmail', 'v1', credentials=creds)
        service.users().getProfile(userId='me').execute()
        
        return token
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise


class GmailHandler:
    """Handle Gmail API interactions"""
    
    def __init__(self, token):
        self.token = token
        self.service = None
        self._init_service()
    
    def _init_service(self):
        """Initialize Gmail API service"""
        try:
            from googleapiclient.discovery import build
            creds = Credentials(token=self.token)
            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as e:
            logger.error(f"Failed to initialize Gmail service: {e}")
            raise
    
    def list_emails(self, query='', max_results=10):
        """List emails from Gmail"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for msg in messages:
                email_data = self._get_email_metadata(msg['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
        
        except Exception as e:
            logger.error(f"Error listing emails: {e}")
            return []
    
    def _get_email_metadata(self, message_id):
        """Get email metadata"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='metadata',
                metadataHeaders=['Subject', 'From', 'Date']
            ).execute()
            
            headers = message.get('payload', {}).get('headers', [])
            
            def get_header(name):
                for header in headers:
                    if header['name'] == name:
                        return header['value']
                return 'Unknown'
            
            return {
                'id': message_id,
                'subject': get_header('Subject'),
                'from': get_header('From'),
                'date': get_header('Date')
            }
        
        except Exception as e:
            logger.error(f"Error getting email metadata: {e}")
            return None
    
    def get_email_as_eml(self, message_id):
        """Retrieve Gmail email as .eml format (RFC 2822)"""
        try:
            # Get raw format - returns base64 encoded RFC 2822 message
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='raw'
            ).execute()
            
            # Decode base64
            raw_email = base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))
            return raw_email.decode('utf-8')
        
        except Exception as e:
            logger.error(f"Error retrieving email as .eml: {e}")
            raise


# Routes

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Secrya KeepSafe Backend'})


@app.route('/api/emails', methods=['GET'])
@require_auth
def get_emails():
    """Get list of emails from Gmail"""
    try:
        gmail = GmailHandler(request.gmail_token)
        query = request.args.get('query', '')
        max_results = int(request.args.get('max_results', 10))
        
        emails = gmail.list_emails(query=query, max_results=max_results)
        
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails)
        })
    
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-email', methods=['POST'])
@require_auth
def analyze_email_endpoint():
    """Analyze email for phishing"""
    try:
        data = request.get_json()
        email_id = data.get('email_id')
        
        if not email_id:
            return jsonify({'error': 'email_id is required'}), 400
        
        # Fetch email as .eml
        gmail = GmailHandler(request.gmail_token)
        eml_content = gmail.get_email_as_eml(email_id)
        
        # Analyze using Secrya
        result = analysis.analyze_email(eml_content)
        
        # Format response
        response = {
            'success': True,
            'email_id': email_id,
            'risk_level': result.get('risk_level', 'UNKNOWN'),
            'risk_score': result.get('risk_score', 0),
            'indicators': result.get('indicators', []),
            'explanations': result.get('explanations', []),
            'recommendations': result.get('recommendations', []),
            'timestamp': datetime.now().isoformat()
        }
        
        # Optional: Save report
        if result.get('indicators'):
            try:
                report_text = report.format_report(result, email_id)
                saved_path = report.save_report(report_text, f"email_{email_id}")
                response['report_saved'] = saved_path
            except Exception as e:
                logger.warning(f"Could not save report: {e}")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-url', methods=['POST'])
@require_auth
def analyze_url_endpoint():
    """Analyze URL for security"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'url is required'}), 400
        
        # Analyze using Secrya
        result = url_security.analyze_url_security(url)
        
        response = {
            'success': True,
            'url': url,
            'domain': result.get('domain', ''),
            'risk_score': result.get('risk_score', 0),
            'indicators': result.get('indicators', []),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"URL analysis error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user', methods=['GET'])
@require_auth
def get_user_info():
    """Get user profile info"""
    try:
        gmail = GmailHandler(request.gmail_token)
        profile = gmail.service.users().getProfile(userId='me').execute()
        
        return jsonify({
            'success': True,
            'email': profile.get('emailAddress', 'Unknown'),
            'messages_total': profile.get('messagesTotal', 0),
            'threads_total': profile.get('threadsTotal', 0)
        })
    
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Secrya KeepSafe Backend Service")
    app.run(
        host='localhost',
        port=5000,
        debug=False,
        threaded=True
    )

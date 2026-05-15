"""
Gmail API Integration Module
Handles all Gmail API interactions for Secrya KeepSafe
"""

import base64
import logging
import time
from typing import List, Dict, Optional
from email import policy
from email.parser import BytesParser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class GmailAPIClient:
    """
    Client for interacting with Google Gmail API
    Handles authentication, email retrieval, and .eml conversion
    
    Features:
    - Email caching for performance
    - Batch metadata retrieval
    - RFC 2822 (.eml) format support
    """
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    CACHE_TTL = 3600  # 1 hour cache
    
    def __init__(self, access_token: str):
        """
        Initialize Gmail API client
        
        Args:
            access_token: OAuth 2.0 access token
        """
        self.access_token = access_token
        self.service = None
        self._initialize_service()
        self._email_cache = {}  # Cache for .eml files
        self._metadata_cache = {}  # Cache for metadata
        self._batch_callbacks = {}  # Store batch responses
    
    def _initialize_service(self):
        """Initialize Gmail API service"""
        try:
            creds = Credentials(token=self.access_token)
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gmail API: {e}")
            raise
    
    def refresh_access_token(self, refresh_token: str, client_id: str, client_secret: str) -> str:
        """
        Refresh expired access token
        
        Args:
            refresh_token: OAuth 2.0 refresh token
            client_id: Google Client ID
            client_secret: Google Client Secret
        
        Returns:
            New access token
        """
        try:
            from google.oauth2 import service_account
            from google.auth import oauthlib
            
            # This is a simplified version - implement full OAuth flow as needed
            logger.warning("Token refresh not fully implemented - use full OAuth flow")
            raise NotImplementedError("Use full OAuth 2.0 refresh flow")
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise
    
    def get_user_profile(self) -> Dict:
        """
        Get user profile information
        
        Returns:
            Dictionary containing user profile data
        """
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            return {
                'email': profile.get('emailAddress', ''),
                'messages_total': profile.get('messagesTotal', 0),
                'threads_total': profile.get('threadsTotal', 0)
            }
        except HttpError as e:
            logger.error(f"Failed to get user profile: {e}")
            raise
    
    def list_messages(self, 
                     query: str = '', 
                     max_results: int = 10,
                     page_token: Optional[str] = None,
                     use_batch: bool = True) -> Dict:
        """
        List messages from Gmail inbox with optional batch metadata retrieval
        
        Args:
            query: Gmail search query (e.g., 'from:sender@example.com')
            max_results: Maximum number of messages to return
            page_token: Token for pagination
            use_batch: Use batch API for faster metadata retrieval
        
        Returns:
            Dictionary with messages list and pagination info
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results,
                pageToken=page_token
            ).execute()
            
            messages = results.get('messages', [])
            
            # Batch retrieve metadata for faster loading
            if use_batch and messages:
                enriched_messages = self._batch_get_metadata(messages)
            else:
                enriched_messages = messages
            
            return {
                'messages': enriched_messages,
                'next_page_token': results.get('nextPageToken'),
                'result_size_estimate': results.get('resultSizeEstimate', 0)
            }
        
        except HttpError as e:
            logger.error(f"Failed to list messages: {e}")
            raise
    
    def _batch_get_metadata(self, messages: List[Dict]) -> List[Dict]:
        """
        Batch retrieve metadata for multiple messages (3x faster)
        
        Args:
            messages: List of message IDs
        
        Returns:
            List of messages with metadata enriched
        """
        try:
            batch = self.service.new_batch_http_request(callback=self._batch_callback)
            message_ids = [msg['id'] for msg in messages]
            
            for msg_id in message_ids:
                batch.add(
                    self.service.users().messages().get(
                        userId='me',
                        id=msg_id,
                        format='metadata',
                        metadataHeaders=['Subject', 'From', 'Date']
                    ),
                    request_id=msg_id
                )
            
            # Execute batch request
            batch.execute()
            
            # Process results
            enriched = []
            for msg in messages:
                msg_id = msg['id']
                if msg_id in self._batch_callbacks:
                    metadata = self._batch_callbacks[msg_id]
                    headers = metadata.get('payload', {}).get('headers', [])
                    enriched.append({
                        'id': msg_id,
                        'subject': self._get_header(headers, 'Subject'),
                        'from': self._get_header(headers, 'From'),
                        'date': self._get_header(headers, 'Date')
                    })
                else:
                    enriched.append(msg)
            
            logger.info(f"Batch retrieved metadata for {len(enriched)} messages")
            return enriched
        
        except Exception as e:
            logger.warning(f"Batch retrieval failed, falling back to standard: {e}")
            return messages
    
    def _batch_callback(self, request_id: str, response: Dict, exception: Exception) -> None:
        """Handle batch response callback"""
        if exception:
            logger.warning(f"Batch error for {request_id}: {exception}")
        else:
            self._batch_callbacks[request_id] = response
    
    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Extract header value from headers list"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''
    
    def get_message_metadata(self, message_id: str) -> Dict:
        """
        Get message metadata (headers only)
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Dictionary with message metadata
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='metadata',
                metadataHeaders=['Subject', 'From', 'To', 'Date', 'Message-ID', 'Content-Type']
            ).execute()
            
            headers = message.get('payload', {}).get('headers', [])
            
            def get_header_value(name: str) -> str:
                for header in headers:
                    if header['name'].lower() == name.lower():
                        return header['value']
                return ''
            
            return {
                'id': message_id,
                'subject': get_header_value('Subject'),
                'from': get_header_value('From'),
                'to': get_header_value('To'),
                'date': get_header_value('Date'),
                'message_id': get_header_value('Message-ID'),
                'content_type': get_header_value('Content-Type'),
                'size': message.get('sizeEstimate', 0)
            }
        
        except HttpError as e:
            logger.error(f"Failed to get message metadata: {e}")
            raise
    
    def get_message_as_eml(self, message_id: str, use_cache: bool = True) -> str:
        """
        Retrieve Gmail message in .eml format (RFC 2822) with caching
        
        This is the complete raw email including all headers and body.
        Caches results for 1 hour to speed up repeated analyses.
        
        Args:
            message_id: Gmail message ID
            use_cache: Use cached version if available
        
        Returns:
            Email content in .eml format (RFC 2822 string)
        
        Raises:
            HttpError: If Gmail API call fails
            ValueError: If message cannot be decoded
        """
        try:
            # Check cache first
            if use_cache and message_id in self._email_cache:
                cached_data = self._email_cache[message_id]
                if time.time() - cached_data['timestamp'] < self.CACHE_TTL:
                    logger.info(f"Cache hit for message {message_id}")
                    return cached_data['content']
                else:
                    del self._email_cache[message_id]
            
            # Request raw format - returns base64 encoded RFC 2822 format
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='raw'
            ).execute()
            
            # Decode from base64
            raw_email = base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))
            eml_content = raw_email.decode('utf-8', errors='replace')
            
            # Store in cache
            self._email_cache[message_id] = {
                'content': eml_content,
                'timestamp': time.time()
            }
            
            logger.info(f"Successfully retrieved message {message_id} as .eml (cached)")
            return eml_content
        
        except KeyError as e:
            logger.error(f"Invalid message format response: {e}")
            raise ValueError(f"Cannot extract raw email: {e}")
        except HttpError as e:
            logger.error(f"Gmail API error retrieving message: {e}")
            raise
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode message: {e}")
            raise ValueError(f"Cannot decode message: {e}")
            raise
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode message: {e}")
            raise ValueError(f"Cannot decode message: {e}")
    
    def get_message_full(self, message_id: str) -> Dict:
        """
        Get complete message with payload and full content
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Dictionary with complete message including headers and body
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            return message
        
        except HttpError as e:
            logger.error(f"Failed to get full message: {e}")
            raise
    
    def parse_eml_to_dict(self, eml_content: str) -> Dict:
        """
        Parse .eml content into dictionary structure
        
        Args:
            eml_content: Email content in .eml format
        
        Returns:
            Dictionary with parsed email components
        """
        try:
            raw_bytes = eml_content.encode('utf-8', errors='replace')
            message = BytesParser(policy=policy.default).parsebytes(raw_bytes)
            
            parsed = {
                'from': message.get('From', ''),
                'to': message.get('To', ''),
                'cc': message.get('Cc', ''),
                'subject': message.get('Subject', ''),
                'date': message.get('Date', ''),
                'message_id': message.get('Message-ID', ''),
                'in_reply_to': message.get('In-Reply-To', ''),
                'headers': dict(message.items())
            }
            
            # Extract body
            if message.is_multipart():
                parts = []
                for part in message.walk():
                    if part.get_content_maintype() == 'text':
                        parts.append(part.get_content())
                parsed['body'] = '\n'.join(parts)
            else:
                parsed['body'] = message.get_content()
            
            return parsed
        
        except Exception as e:
            logger.error(f"Failed to parse .eml: {e}")
            raise
    
    def search_emails(self, 
                     sender: Optional[str] = None,
                     subject: Optional[str] = None,
                     has_attachment: bool = False,
                     before_date: Optional[str] = None,
                     after_date: Optional[str] = None) -> List[Dict]:
        """
        Advanced email search
        
        Args:
            sender: Filter by sender email
            subject: Filter by subject keyword
            has_attachment: Only return emails with attachments
            before_date: Search before date (YYYY/MM/DD)
            after_date: Search after date (YYYY/MM/DD)
        
        Returns:
            List of message dictionaries
        """
        query_parts = []
        
        if sender:
            query_parts.append(f'from:{sender}')
        if subject:
            query_parts.append(f'subject:{subject}')
        if has_attachment:
            query_parts.append('has:attachment')
        if before_date:
            query_parts.append(f'before:{before_date}')
        if after_date:
            query_parts.append(f'after:{after_date}')
        
        query = ' '.join(query_parts)
        
        try:
            results = self.list_messages(query=query, max_results=10)
            
            # Enrich with metadata
            messages_with_meta = []
            for msg in results['messages']:
                try:
                    meta = self.get_message_metadata(msg['id'])
                    messages_with_meta.append(meta)
                except Exception as e:
                    logger.warning(f"Failed to get metadata for {msg['id']}: {e}")
            
            return messages_with_meta
        
        except HttpError as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def get_email_summary(self, message_id: str) -> Dict:
        """
        Get a summary of an email suitable for quick display
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Dictionary with email summary
        """
        try:
            metadata = self.get_message_metadata(message_id)
            
            return {
                'id': message_id,
                'subject': metadata['subject'],
                'from': metadata['from'],
                'to': metadata['to'],
                'date': metadata['date'],
                'size': metadata['size']
            }
        
        except Exception as e:
            logger.error(f"Failed to get email summary: {e}")
            raise


if __name__ == '__main__':
    # Example usage (requires valid token)
    print("Gmail API Integration Module")
    print("This module should be imported and used in the Flask backend")

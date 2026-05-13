"""
Outlook API Integration Module
Handles all Outlook API interactions for Secrya KeepSafe
"""

import logging
from typing import List, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class OutlookAPIClient:
    """
    Client for interacting with Microsoft Outlook/Office 365 API
    Handles email retrieval and .eml conversion
    """
    
    SCOPES = ['https://graph.microsoft.com/.default']
    BASE_URL = 'https://graph.microsoft.com/v1.0'
    
    def __init__(self, access_token: str):
        """
        Initialize Outlook API client
        
        Args:
            access_token: OAuth 2.0 access token
        """
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_user_profile(self) -> Dict:
        """
        Get user profile information
        
        Returns:
            Dictionary containing user profile data
        """
        try:
            url = f'{self.BASE_URL}/me'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return {
                'email': data.get('userPrincipalName', ''),
                'name': data.get('displayName', ''),
                'mailbox_size': data.get('mailboxQuota', 0)
            }
        except Exception as e:
            logger.error(f"Failed to get Outlook profile: {e}")
            raise
    
    def list_messages(self, 
                     max_results: int = 10,
                     page_token: Optional[str] = None) -> Dict:
        """
        List messages from Outlook inbox
        
        Args:
            max_results: Maximum number of messages to return
            page_token: Token for pagination (skip token)
        
        Returns:
            Dictionary with messages list and pagination info
        """
        try:
            url = f'{self.BASE_URL}/me/messages'
            
            params = {
                '$top': max_results,
                '$select': 'id,subject,from,receivedDateTime,isRead',
                '$orderby': 'receivedDateTime desc'
            }
            
            if page_token:
                params['$skip'] = page_token
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            messages = data.get('value', [])
            
            enriched = []
            for msg in messages:
                from_data = msg.get('from', {}).get('emailAddress', {})
                enriched.append({
                    'id': msg['id'],
                    'subject': msg.get('subject', '(No Subject)'),
                    'from': from_data.get('address', ''),
                    'from_name': from_data.get('name', ''),
                    'date': msg.get('receivedDateTime', ''),
                    'is_read': msg.get('isRead', False)
                })
            
            return {
                'messages': enriched,
                'next_page_token': page_token,
                'count': len(enriched)
            }
        
        except Exception as e:
            logger.error(f"Failed to list Outlook messages: {e}")
            raise
    
    def get_message_metadata(self, message_id: str) -> Dict:
        """
        Get message metadata (headers and basic info)
        
        Args:
            message_id: Outlook message ID
        
        Returns:
            Dictionary with message metadata
        """
        try:
            url = f'{self.BASE_URL}/me/messages/{message_id}'
            
            params = {
                '$select': 'id,subject,from,to,cc,receivedDateTime,bodyPreview,size'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            msg = response.json()
            from_data = msg.get('from', {}).get('emailAddress', {})
            
            return {
                'id': message_id,
                'subject': msg.get('subject', ''),
                'from': from_data.get('address', ''),
                'from_name': from_data.get('name', ''),
                'to': msg.get('to', []),
                'cc': msg.get('cc', []),
                'date': msg.get('receivedDateTime', ''),
                'preview': msg.get('bodyPreview', ''),
                'size': msg.get('size', 0)
            }
        
        except Exception as e:
            logger.error(f"Failed to get Outlook message metadata: {e}")
            raise
    
    def get_message_as_eml(self, message_id: str) -> str:
        """
        Retrieve Outlook message in RFC 2822 format (.eml)
        
        Microsoft Graph doesn't provide native .eml export,
        so we construct it from the message data.
        
        Args:
            message_id: Outlook message ID
        
        Returns:
            Email content in RFC 2822-compatible format
        
        Raises:
            Exception: If message cannot be retrieved
        """
        try:
            url = f'{self.BASE_URL}/me/messages/{message_id}'
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            msg = response.json()
            
            # Construct RFC 2822-like format
            eml = self._construct_eml(msg)
            
            logger.info(f"Successfully retrieved Outlook message {message_id} as RFC 2822")
            return eml
        
        except Exception as e:
            logger.error(f"Failed to get Outlook message as .eml: {e}")
            raise
    
    def _construct_eml(self, message: Dict) -> str:
        """
        Construct RFC 2822 format from Outlook message data
        
        Args:
            message: Message data from Outlook API
        
        Returns:
            RFC 2822 formatted email string
        """
        eml_lines = []
        
        # Headers
        from_data = message.get('from', {}).get('emailAddress', {})
        eml_lines.append(f"From: {from_data.get('name', '')} <{from_data.get('address', '')}>")
        
        # To recipients
        to_addrs = []
        for recipient in message.get('toRecipients', []):
            addr = recipient.get('emailAddress', {})
            to_addrs.append(f"{addr.get('name', '')} <{addr.get('address', '')}>")
        if to_addrs:
            eml_lines.append(f"To: {', '.join(to_addrs)}")
        
        # CC recipients
        cc_addrs = []
        for recipient in message.get('ccRecipients', []):
            addr = recipient.get('emailAddress', {})
            cc_addrs.append(f"{addr.get('name', '')} <{addr.get('address', '')}>")
        if cc_addrs:
            eml_lines.append(f"Cc: {', '.join(cc_addrs)}")
        
        # Subject
        eml_lines.append(f"Subject: {message.get('subject', '(No Subject)')}")
        
        # Date
        eml_lines.append(f"Date: {message.get('receivedDateTime', '')}")
        
        # Message ID (construct one)
        message_id = message.get('id', '')
        if message_id:
            eml_lines.append(f"Message-ID: <{message_id}@outlook.com>")
        
        # Content-Type
        body_type = message.get('bodyType', 'html')
        if body_type == 'html':
            eml_lines.append('Content-Type: text/html; charset="UTF-8"')
        else:
            eml_lines.append('Content-Type: text/plain; charset="UTF-8"')
        
        eml_lines.append('Content-Transfer-Encoding: 7bit')
        
        # Blank line before body
        eml_lines.append('')
        
        # Body
        body = message.get('body', {}).get('content', '')
        eml_lines.append(body)
        
        return '\r\n'.join(eml_lines)
    
    def search_messages(self, 
                       from_addr: Optional[str] = None,
                       subject: Optional[str] = None,
                       has_attachment: bool = False) -> List[Dict]:
        """
        Search messages in Outlook
        
        Args:
            from_addr: Filter by sender email
            subject: Filter by subject keyword
            has_attachment: Only return emails with attachments
        
        Returns:
            List of message dictionaries
        """
        try:
            url = f'{self.BASE_URL}/me/messages'
            
            filters = []
            if from_addr:
                filters.append(f"from/emailAddress/address eq '{from_addr}'")
            if subject:
                filters.append(f"contains(subject, '{subject}')")
            if has_attachment:
                filters.append("hasAttachments eq true")
            
            params = {
                '$top': 10,
                '$select': 'id,subject,from,receivedDateTime'
            }
            
            if filters:
                params['$filter'] = ' and '.join(filters)
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            messages = response.json().get('value', [])
            
            return [
                {
                    'id': msg['id'],
                    'subject': msg.get('subject', ''),
                    'from': msg.get('from', {}).get('emailAddress', {}).get('address', ''),
                    'date': msg.get('receivedDateTime', '')
                }
                for msg in messages
            ]
        
        except Exception as e:
            logger.error(f"Outlook search failed: {e}")
            raise


if __name__ == '__main__':
    print("Outlook API Integration Module")
    print("This module should be imported and used in the Flask backend")

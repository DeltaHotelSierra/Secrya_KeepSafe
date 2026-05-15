"""
Risk Score Enhancement Module
Enhances basic phishing risk scores with provider trust signals
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class RiskEnhancer:
    """
    Enhance risk scores with email provider analysis and trust signals
    
    Factors considered:
    - Sender domain reputation
    - Known spoofing indicators
    - Link consistency
    - Authentication headers (SPF, DKIM, DMARC)
    """
    
    # Trusted provider domains (verified legitimate)
    TRUSTED_DOMAINS = {
        'google.com', 'microsoft.com', 'apple.com', 'linkedin.com',
        'github.com', 'amazon.com', 'facebook.com', 'twitter.com',
        'atlassian.com', 'notion.so', 'slack.com', 'adobe.com',
        'oracle.com', 'salesforce.com', 'zendesk.com', 'stripe.com',
        'paypal.com', 'square.com', 'twilio.com', 'sendgrid.com'
    }
    
    # Known phishing domains (honeypot)
    KNOWN_PHISHING_DOMAINS = {
        'goog1e.com', 'microsof.com', 'appl3.com', 'amaz0n.com'
    }
    
    @staticmethod
    def enhance_risk_score(analysis_result: Dict, sender_email: str, headers: Dict = None) -> Dict:
        """
        Enhance risk score based on sender domain and email signals
        
        Args:
            analysis_result: Original Secrya analysis result
            sender_email: Sender's email address
            headers: Email headers dictionary (optional)
        
        Returns:
            Enhanced analysis with adjusted risk score and additional signals
        """
        try:
            original_score = analysis_result.get('risk_score', 5.0)
            indicators = list(analysis_result.get('indicators', []))
            
            # Extract domain
            if '@' not in sender_email:
                logger.warning(f"Invalid sender email: {sender_email}")
                return analysis_result
            
            domain = sender_email.split('@')[1].lower()
            
            # 1. Check for known phishing domains
            if domain in RiskEnhancer.KNOWN_PHISHING_DOMAINS:
                adjusted_score = 10.0
                indicators.append('🚨 Known phishing domain detected')
                logger.warning(f"Known phishing domain detected: {domain}")
            
            # 2. Check if from trusted provider
            elif domain in RiskEnhancer.TRUSTED_DOMAINS:
                adjusted_score = max(original_score - 1.5, 1.0)
                indicators.insert(0, '✅ Verified trusted provider')
            
            # 3. Check for homoglyph/spoofing
            elif RiskEnhancer._is_homoglyph_domain(domain):
                adjusted_score = min(original_score + 2.5, 10.0)
                indicators.append('⚠️ Domain looks similar to legitimate service (homoglyph)')
            
            # 4. Check domain age (new domains are riskier)
            elif RiskEnhancer._is_new_domain(domain):
                adjusted_score = min(original_score + 1.0, 10.0)
                indicators.append('⚠️ Recently registered domain')
            
            else:
                adjusted_score = original_score
            
            # 5. Enhance based on link mismatch
            if 'Link mismatch' in str(indicators) or 'link mismatch' in str(indicators).lower():
                adjusted_score = min(adjusted_score + 1.5, 10.0)
            
            # 6. Check authentication headers
            if headers:
                auth_score = RiskEnhancer._check_auth_headers(headers)
                adjusted_score = adjusted_score * 0.9 + auth_score * 0.1
            
            # Ensure score is in valid range
            adjusted_score = max(1.0, min(10.0, adjusted_score))
            
            # Determine confidence level
            if domain in RiskEnhancer.TRUSTED_DOMAINS or domain in RiskEnhancer.KNOWN_PHISHING_DOMAINS:
                confidence = 'Very High'
            elif len(indicators) >= 3:
                confidence = 'High'
            elif len(indicators) >= 1:
                confidence = 'Medium'
            else:
                confidence = 'Low'
            
            # Determine risk level
            if adjusted_score >= 7.5:
                risk_level = 'HIGH'
            elif adjusted_score >= 4.0:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            # Update result
            analysis_result['risk_score'] = round(adjusted_score, 1)
            analysis_result['original_risk_score'] = round(original_score, 1)
            analysis_result['risk_level'] = risk_level
            analysis_result['indicators'] = list(dict.fromkeys(indicators))  # Remove duplicates
            analysis_result['confidence'] = confidence
            analysis_result['enhanced'] = True
            
            logger.info(f"Risk enhanced: {original_score} → {adjusted_score} (domain: {domain})")
            
            return analysis_result
        
        except Exception as e:
            logger.error(f"Risk enhancement failed: {e}")
            # Return original result if enhancement fails
            return analysis_result
    
    @staticmethod
    def _is_homoglyph_domain(domain: str) -> bool:
        """
        Check if domain looks like a homoglyph of a legitimate domain
        
        Homoglyphs use characters that look similar:
        - 1 (one) vs l (lowercase L) vs I (uppercase i)
        - 0 (zero) vs O (uppercase O)
        - rn vs m
        """
        homoglyph_indicators = [
            # Number substitutions
            ('goog1e', ['google']),
            ('mic ros0ft', ['microsoft']),
            ('am4zon', ['amazon']),
            ('l1nked1n', ['linkedin']),
            # Letter substitutions
            ('qoogle', ['google']),
            ('rnycrοsoft', ['microsoft']),
        ]
        
        domain_lower = domain.lower()
        
        for homoglyph, legitimate in homoglyph_indicators:
            for legit_domain in legitimate:
                if homoglyph in domain_lower or legit_domain in domain_lower:
                    # Check if very similar
                    similarity = RiskEnhancer._string_similarity(domain_lower, legit_domain)
                    if similarity > 0.8:
                        return True
        
        return False
    
    @staticmethod
    def _is_new_domain(domain: str) -> bool:
        """
        Check if domain is newly registered
        
        Note: This is a placeholder. In production, you'd query WHOIS
        or use a domain age API.
        """
        # Common patterns for newly registered domains
        new_patterns = [
            'temporary', 'temp', 'test', 'new', 'dev',
            'demo', 'staging', 'verify', 'confirm'
        ]
        
        domain_lower = domain.lower()
        
        for pattern in new_patterns:
            if pattern in domain_lower:
                return True
        
        return False
    
    @staticmethod
    def _check_auth_headers(headers: Dict) -> float:
        """
        Check email authentication headers (SPF, DKIM, DMARC)
        
        Returns:
            Score 0.0-10.0 based on authentication strength
        """
        try:
            score = 5.0  # Start neutral
            
            # SPF check
            spf_header = headers.get('Received-SPF', '')
            if 'pass' in spf_header.lower():
                score += 1.5
            elif 'fail' in spf_header.lower():
                score -= 2.0
            
            # DKIM check
            dkim_header = headers.get('DKIM-Signature', '')
            if dkim_header:
                score += 1.5
            
            # DMARC check
            dmarc_header = headers.get('Authentication-Results', '')
            if 'dmarc=pass' in dmarc_header.lower():
                score += 1.5
            elif 'dmarc=fail' in dmarc_header.lower():
                score -= 2.0
            
            # Clamp score
            score = max(1.0, min(10.0, score))
            
            return score
        
        except Exception as e:
            logger.warning(f"Auth header check failed: {e}")
            return 5.0
    
    @staticmethod
    def _string_similarity(s1: str, s2: str) -> float:
        """
        Calculate string similarity (Levenshtein-like)
        
        Returns:
            Score 0.0-1.0 where 1.0 is identical
        """
        if not s1 or not s2:
            return 0.0
        
        # Simple similarity: matching characters / total characters
        matches = sum(1 for a, b in zip(s1, s2) if a == b)
        total = max(len(s1), len(s2))
        
        return matches / total if total > 0 else 0.0
    
    @staticmethod
    def generate_explanation(analysis_result: Dict, sender_email: str) -> str:
        """
        Generate human-readable explanation of risk score
        
        Args:
            analysis_result: Enhanced analysis result
            sender_email: Sender's email
        
        Returns:
            String explanation of the risk assessment
        """
        try:
            risk_level = analysis_result.get('risk_level', 'UNKNOWN')
            risk_score = analysis_result.get('risk_score', 0)
            indicators = analysis_result.get('indicators', [])
            domain = sender_email.split('@')[1].lower() if '@' in sender_email else ''
            
            explanation = f"**Risk Level: {risk_level} ({risk_score}/10)**\n\n"
            
            if risk_level == 'HIGH':
                explanation += "⚠️ **WARNING**: This email shows signs of phishing. Do not click links or download attachments.\n\n"
            elif risk_level == 'MEDIUM':
                explanation += "⚠️ **CAUTION**: This email has some suspicious characteristics. Verify before interacting.\n\n"
            else:
                explanation += "✅ This email appears to be legitimate, but always verify unexpected requests.\n\n"
            
            if indicators:
                explanation += "**Issues Detected:**\n"
                for indicator in indicators[:5]:  # Show top 5
                    explanation += f"- {indicator}\n"
            
            if domain in RiskEnhancer.TRUSTED_DOMAINS:
                explanation += f"\n✅ From trusted provider: {domain}"
            
            return explanation
        
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return "Unable to generate explanation."


if __name__ == '__main__':
    print("Risk Score Enhancement Module")
    print("Enhances phishing detection with trust signals")

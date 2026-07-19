"""
Utility module for Canva Monitor V2.
Contains helper functions like token extraction.
"""
from urllib.parse import urlparse, parse_qs

def extract_canva_token(url: str) -> str:
    """
    Extracts the invitation token from a Canva URL.
    Supports 'brandAccessToken', 'invitationToken', or 'token' parameters.
    
    Args:
        url: The Canva invitation URL.
        
    Returns:
        The extracted token string, or an empty string if not found/invalid.
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        # Check known token parameters
        for param in ("brandAccessToken", "invitationToken", "token"):
            if param in query_params and query_params[param]:
                return query_params[param][0]
                
        return ""
    except Exception:
        return ""

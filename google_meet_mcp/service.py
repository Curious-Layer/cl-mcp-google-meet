import logging

from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger("google-meet-mcp-server")


def get_service():
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    logger.info("Creating Google Meet API service with provided access token")
    creds = Credentials(token=cred.access_token, scopes=cred.scopes)
    service = build("meet", "v2", credentials=creds)
    logger.info("Google Meet API service created successfully")
    return service

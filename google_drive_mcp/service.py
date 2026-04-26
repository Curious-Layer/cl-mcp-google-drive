import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from fastmcp_credentials import ResolvedCredential

logger = logging.getLogger("google-drive-mcp-server")


def get_service(cred: ResolvedCredential):
    """Build and return an authenticated Google Drive API service."""
    logger.info("Creating Google Drive API service")
    google_cred = Credentials(
        token=cred.access_token,
        refresh_token=cred.refresh_token,
        token_uri=cred.token_uri or "https://oauth2.googleapis.com/token",
        client_id=cred.client_id,
        client_secret=cred.client_secret,
        scopes=cred.scopes,
    )
    service = build("drive", "v3", credentials=google_cred)
    logger.info("Google Drive API service created successfully")
    return service

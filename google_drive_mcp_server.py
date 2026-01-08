#!/usr/bin/env python3
"""
MCP Server for Google Drive API
Provides access to Google Drive operations through Model Context Protocol
"""

import json
import logging
import os
import argparse
import io
from typing import Any, Optional, Dict
from pathlib import Path

from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler('google_drive_mcp_server.log'),
        logging.StreamHandler()
    ],
)
logger = logging.getLogger("google-drive-mcp-server")

# Create FastMCP instance
mcp = FastMCP("CL Google Drive MCP Server")

# Global service instance
_service = None


def _get_token_data(token_data: str) -> Dict:
    """Decode access token JSON string to dictionary"""
    try:
        token_data = json.loads(token_data)
        auth_data = {
            "token": token_data.get("token"),
            "refresh_token": token_data.get("refresh_token"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": token_data.get("client_id"),
            "client_secret": token_data.get("client_secret"),
            "scopes": token_data.get("scopes"),
        }
        return auth_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode access token: {e}")
        return {}


def _get_service(token_data: str):
    """Create Google Drive API service with provided access token"""
    auth_data = _get_token_data(token_data)
    logger.info("Creating Google Drive API service with provided access token")
    # Don't pass scopes - the token already has its authorized scopes
    creds = Credentials(**auth_data)
    service = build("drive", "v3", credentials=creds)
    logger.info("Google Drive API service created successfully")
    return service


# Define MCP Tools


@mcp.tool(
    name="list_files",
    description="List files in Google Drive. Supports filtering by folder, name, and type.",
)
def list_files(
    oauth_token: str, folder_id: str = None, query: str = "", page_size: int = 10
) -> Dict:
    """List files in Google Drive"""
    logger.info("Executing list_files")
    try:
        service = _get_service(oauth_token)
        page_size = min(page_size, 1000)

        # Build query
        q_parts = []
        if folder_id:
            q_parts.append(f"'{folder_id}' in parents")
        if query:
            q_parts.append(query)
        q_parts.append("trashed=false")

        query_str = " and ".join(q_parts)

        results = (
            service.files()
            .list(
                q=query_str,
                pageSize=page_size,
                fields="files(id, name, mimeType, size, createdTime, modifiedTime, owners, webViewLink)",
            )
            .execute()
        )

        files = results.get("files", [])
        logger.info(f"Found {len(files)} files")

        return {"count": len(files), "files": files}
    except Exception as e:
        logger.error(f"Error in list_files: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="get_file_metadata", description="Get metadata for a specific file by ID"
)
def get_file_metadata(oauth_token: str, file_id: str) -> Dict:
    """Get metadata for a specific file"""
    logger.info("Executing get_file_metadata")
    logger.debug(f"File ID: {file_id}")
    try:
        service = _get_service(oauth_token)

        file = service.files().get(fileId=file_id, fields="*").execute()

        logger.info(f"Retrieved metadata for file: {file.get('name')}")
        return file
    except Exception as e:
        logger.error(f"Error in get_file_metadata: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="download_file", description="Download a file from Google Drive to local disk"
)
def download_file(oauth_token: str, file_id: str, destination_path: str) -> Dict:
    """Download a file from Google Drive"""
    logger.info("Executing download_file")
    logger.debug(f"Downloading file {file_id} to {destination_path}")
    try:
        service = _get_service(oauth_token)

        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(f"Download {int(status.progress() * 100)}%")

        # Write to file
        with open(destination_path, "wb") as f:
            f.write(fh.getvalue())

        logger.info(f"File downloaded successfully to: {destination_path}")
        return {"message": f"File downloaded successfully to: {destination_path}"}
    except Exception as e:
        logger.error(f"Error in download_file: {e}")
        return {"error": str(e)}


@mcp.tool(name="upload_file", description="Upload a file to Google Drive")
def upload_file(
    oauth_token: str,
    file_path: str,
    name: str = None,
    folder_id: str = None,
    mime_type: str = None,
) -> Dict:
    """Upload a file to Google Drive"""
    logger.info("Executing upload_file")
    try:
        service = _get_service(oauth_token)

        if name is None:
            name = os.path.basename(file_path)

        logger.debug(f"Uploading {file_path} as {name}")

        file_metadata = {"name": name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        file = (
            service.files()
            .create(
                body=file_metadata, media_body=media, fields="id, name, webViewLink"
            )
            .execute()
        )

        logger.info(f"File uploaded successfully: {file['name']} (ID: {file['id']})")
        return {"message": "File uploaded successfully", "file": file}
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        return {"error": str(e)}


@mcp.tool(name="create_folder", description="Create a new folder in Google Drive")
def create_folder(oauth_token: str, name: str, parent_folder_id: str = None) -> Dict:
    """Create a new folder in Google Drive"""
    logger.info("Executing create_folder")
    try:
        service = _get_service(oauth_token)

        file_metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_folder_id:
            file_metadata["parents"] = [parent_folder_id]

        folder = (
            service.files()
            .create(body=file_metadata, fields="id, name, webViewLink")
            .execute()
        )

        logger.info(
            f"Folder created successfully: {folder['name']} (ID: {folder['id']})"
        )
        return {"message": "Folder created successfully", "folder": folder}
    except Exception as e:
        logger.error(f"Error in create_folder: {e}")
        return {"error": str(e)}


@mcp.tool(name="delete_file", description="Delete a file or folder from Google Drive")
def delete_file(oauth_token: str, file_id: str) -> Dict:
    """Delete a file or folder from Google Drive"""
    logger.info("Executing delete_file")
    logger.debug(f"Deleting file/folder: {file_id}")
    try:
        service = _get_service(oauth_token)

        service.files().delete(fileId=file_id).execute()

        logger.info(f"File/folder deleted: {file_id}")
        return {"message": f"File/folder with ID {file_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error in delete_file: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="search_files",
    description="Search for files in Google Drive using advanced queries",
)
def search_files(oauth_token: str, query: str, page_size: int = 10) -> Dict:
    """Search for files in Google Drive"""
    logger.info("Executing search_files")
    logger.debug(f"Search query: {query}")
    try:
        service = _get_service(oauth_token)
        page_size = min(page_size, 1000)

        results = (
            service.files()
            .list(
                q=query + " and trashed=false",
                pageSize=page_size,
                fields="files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink)",
            )
            .execute()
        )

        files = results.get("files", [])
        logger.info(f"Search found {len(files)} files")

        return {"count": len(files), "files": files}
    except Exception as e:
        logger.error(f"Error in search_files: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="share_file",
    description="Share a file with a user or make it publicly accessible",
)
def share_file(
    oauth_token: str,
    file_id: str,
    email: str = None,
    role: str = "reader",
    share_type: str = None,
) -> Dict:
    """Share a file with a user or publicly"""
    logger.info("Executing share_file")
    try:
        service = _get_service(oauth_token)

        if share_type is None:
            share_type = "user" if email else "anyone"

        permission = {"type": share_type, "role": role}
        if email:
            permission["emailAddress"] = email

        logger.debug(f"Sharing file {file_id} with {email or 'anyone'} as {role}")
        result = (
            service.permissions()
            .create(fileId=file_id, body=permission, fields="id")
            .execute()
        )

        # Get file link
        file = (
            service.files()
            .get(fileId=file_id, fields="webViewLink, webContentLink")
            .execute()
        )

        logger.info(f"File shared successfully: {file_id}")
        return {
            "message": "File shared successfully",
            "permission_id": result.get("id"),
            "webViewLink": file.get("webViewLink"),
            "webContentLink": file.get("webContentLink"),
        }
    except Exception as e:
        logger.error(f"Error in share_file: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="get_file_content",
    description="Get the content of a text file from Google Drive",
)
def get_file_content(oauth_token: str, file_id: str) -> str:
    """Get the content of a text file"""
    logger.info("Executing get_file_content")
    try:
        service = _get_service(oauth_token)

        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        content = fh.getvalue().decode("utf-8")
        logger.info(f"Retrieved content for file {file_id} ({len(content)} bytes)")

        return content
    except Exception as e:
        logger.error(f"Error in get_file_content: {e}")
        return f"Error: {str(e)}"


# Function for parsing the cmd-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Google Drive MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', 'sse', or 'streamable-http')",
        default=None,
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Google Drive MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    # Build kwargs for mcp.run() only with provided values
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        # Start the MCP server with optional transport/host/port
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise

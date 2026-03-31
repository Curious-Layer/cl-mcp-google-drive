import io
import logging
import os
from typing import Any
from pydantic import Field

from fastmcp import FastMCP
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .schemas import (
    ApiObjectResponse,
    CreateFolderToolResponse,
    FilesListToolResponse,
    MessageToolResponse,
    OAuthTokenData,
    ShareFileToolResponse,
    UploadFileToolResponse,
)
from .service import get_service

logger = logging.getLogger("google-drive-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="list_files",
        description="List files in Google Drive. Supports filtering by folder, name, and type.",
    )
    def list_files(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        folder_id: str | None = Field(default=None, description="Optional parent folder ID to filter by"),
        query: str = Field(default="", description="Optional additional Drive query fragment (e.g., `name contains 'report'`)"),
        page_size: int = Field(default=10, description="Maximum number of results to return (capped at 1000)")
    ) -> FilesListToolResponse:
        """
        Returns:
            File count and list of file metadata objects or error.
        """
        logger.info("Executing list_files")
        try:
            service = get_service(oauth_token)
            page_size = min(page_size, 1000)

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

    @mcp.tool(name="get_file_metadata", description="Get metadata for a specific file by ID")
    def get_file_metadata(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        file_id: str = Field(..., description="Google Drive file ID")
    ) -> ApiObjectResponse:
        """
        Returns:
            Full file metadata object or error.
        """
        logger.info("Executing get_file_metadata")
        logger.debug(f"File ID: {file_id}")
        try:
            service = get_service(oauth_token)
            file = service.files().get(fileId=file_id, fields="*").execute()
            logger.info(f"Retrieved metadata for file: {file.get('name')}")
            return file
        except Exception as e:
            logger.error(f"Error in get_file_metadata: {e}")
            return {"error": str(e)}

    @mcp.tool(
        name="download_file", description="Download a file from Google Drive to local disk"
    )
    def download_file(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        file_id: str = Field(..., description="Google Drive file ID"),
        destination_path: str = Field(..., description="Local destination path")
    ) -> MessageToolResponse:
        """
        Returns:
            Success message containing destination path or error.
        """
        logger.info("Executing download_file")
        logger.debug(f"Downloading file {file_id} to {destination_path}")
        try:
            service = get_service(oauth_token)

            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                logger.info(f"Download {int(status.progress() * 100)}%")

            with open(destination_path, "wb") as f:
                f.write(fh.getvalue())

            logger.info(f"File downloaded successfully to: {destination_path}")
            return {"message": f"File downloaded successfully to: {destination_path}"}
        except Exception as e:
            logger.error(f"Error in download_file: {e}")
            return {"error": str(e)}

    @mcp.tool(name="upload_file", description="Upload a file to Google Drive")
    def upload_file(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        file_path: str = Field(..., description="Local path to file being uploaded"),
        name: str | None = Field(default=None, description="Optional destination filename in Drive; defaults to local filename"),
        folder_id: str | None = Field(default=None, description="Optional parent folder ID in Drive"),
        mime_type: str | None = Field(default=None, description="Optional MIME type (e.g., `text/plain`, `application/pdf`)"),
    ) -> UploadFileToolResponse:
        """
        Returns:
            Success message and uploaded file metadata or error.
        """
        logger.info("Executing upload_file")
        try:
            service = get_service(oauth_token)

            if name is None:
                name = os.path.basename(file_path)

            logger.debug(f"Uploading {file_path} as {name}")

            file_metadata: dict[str, Any] = {"name": name}
            if folder_id:
                file_metadata["parents"] = [folder_id]

            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id, name, webViewLink")
                .execute()
            )

            logger.info(f"File uploaded successfully: {file['name']} (ID: {file['id']})")
            return {"message": "File uploaded successfully", "file": file}
        except Exception as e:
            logger.error(f"Error in upload_file: {e}")
            return {"error": str(e)}

    @mcp.tool(name="create_folder", description="Create a new folder in Google Drive")
    def create_folder(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        name: str = Field(..., description="Folder name"),
        parent_folder_id: str | None = Field(default=None, description="Optional parent folder ID"),
    ) -> CreateFolderToolResponse:
        """
        Returns:
            Success message and created folder metadata or error.
        """
        logger.info("Executing create_folder")
        try:
            service = get_service(oauth_token)

            file_metadata: dict[str, Any] = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder",
            }
            if parent_folder_id:
                file_metadata["parents"] = [parent_folder_id]

            folder = (
                service.files()
                .create(body=file_metadata, fields="id, name, webViewLink")
                .execute()
            )

            logger.info(f"Folder created successfully: {folder['name']} (ID: {folder['id']})")
            return {"message": "Folder created successfully", "folder": folder}
        except Exception as e:
            logger.error(f"Error in create_folder: {e}")
            return {"error": str(e)}

    @mcp.tool(name="delete_file", description="Delete a file or folder from Google Drive")
    def delete_file(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        file_id: str = Field(..., description="Google Drive file or folder ID to delete"),
    ) -> MessageToolResponse:
        """
        Returns:
            Deletion status message or error.
        """
        logger.info("Executing delete_file")
        logger.debug(f"Deleting file/folder: {file_id}")
        try:
            service = get_service(oauth_token)
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
    def search_files(
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        query: str = Field(..., description="Drive query expression (e.g., `name contains 'report'`)"),
        page_size: int = Field(default=10, description="Maximum number of results (capped at 1000)"),
    ) -> FilesListToolResponse:
        """
        Returns:
            File count and matching file metadata list or error.
        """
        logger.info("Executing search_files")
        logger.debug(f"Search query: {query}")
        try:
            service = get_service(oauth_token)
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
        oauth_token: OAuthTokenData = Field(..., description="OAuth token"),
        file_id: str = Field(..., description="Google Drive file ID"),
        email: str | None = Field(default=None, description="Recipient email when sharing with `share_type='user'`"),
        role: str = Field(default="reader", description="Permission role (e.g., `reader`, `commenter`, `writer`)"),
        share_type: str | None = Field(default=None, description="Permission type (e.g., `user`, `group`, `domain`, `anyone`)"),
    ) -> ShareFileToolResponse:
        """
        Returns:
            Sharing status, permission ID, links, or error.
        """
        logger.info("Executing share_file")
        try:
            service = get_service(oauth_token)

            if share_type is None:
                share_type = "user" if email else "anyone"

            permission = {"type": share_type, "role": role}
            if email:
                permission["emailAddress"] = email

            logger.debug(f"Sharing file {file_id} with {email or 'anyone'} as {role}")
            result = (
                service.permissions().create(fileId=file_id, body=permission, fields="id").execute()
            )

            file = (
                service.files().get(fileId=file_id, fields="webViewLink, webContentLink").execute()
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
    def get_file_content(oauth_token: OAuthTokenData = Field(description="OAuth token"), file_id: str = Field( description="Google Drive file ID")) -> str:
        """
        Returns:
            Decoded file content string, or an error message string.
        """
        logger.info("Executing get_file_content")
        try:
            service = get_service(oauth_token)

            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                _, done = downloader.next_chunk()

            content = fh.getvalue().decode("utf-8")
            logger.info(f"Retrieved content for file {file_id} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"Error in get_file_content: {e}")
            return f"Error: {str(e)}"

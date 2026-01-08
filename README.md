# Google Drive MCP Server

A Model Context Protocol (MCP) server that provides access to the Google Drive API.

This server allows you to interact with Google Drive for file management, search, and more, directly through MCP.

## Authentication

Authentication is handled by passing a valid `oauth_token` with each tool call. The server does not handle the OAuth flow to generate this token. You must obtain a valid token with the `https://www.googleapis.com/auth/drive` scope.

## Features

The server provides the following tools:

- **list_files**: List files and folders.
- **get_file_metadata**: Retrieve metadata for a file.
- **download_file**: Download a file to your local machine.
- **upload_file**: Upload a file to Google Drive.
- **create_folder**: Create a new folder.
- **delete_file**: Delete a file or folder.
- **search_files**: Perform advanced searches for files.
- **share_file**: Share files with other users.
- **get_file_content**: Read the content of a text-based file.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server:**
    The server can be run in different transport modes.

    - **For `stdio` transport (common for local clients):**
      ```bash
      python google_drive_mcp_server.py
      ```
    - **For `sse` (Server-Sent Events) transport:**
      ```bash
      python google_drive_mcp_server.py --transport sse --host 127.0.0.1 --port 8000
      ```

## Usage Examples

All tool calls require a valid `oauth_token` argument.

### List Root Folder
```json
{
  "tool": "list_files",
  "arguments": {
    "oauth_token": "your_oauth_token_string"
  }
}
```

### Upload a File
```json
{
  "tool": "upload_file",
  "arguments": {
    "oauth_token": "your_oauth_token_string",
    "file_path": "/path/to/your/local/file.txt",
    "name": "MyFile.txt"
  }
}
```

### Search for PDF Files
```json
{
  "tool": "search_files",
  "arguments": {
    "oauth_token": "your_oauth_token_string",
    "query": "mimeType='application/pdf'"
  }
}
```


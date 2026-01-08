# Google Drive MCP Server

A Model Context Protocol (MCP) server that provides access to Google Drive API endpoints.

## Features

This MCP server provides the following Google Drive operations:

- **list_files**: List files in Google Drive with filtering options
- **get_file_metadata**: Get detailed metadata for a specific file
- **download_file**: Download files from Google Drive to local disk
- **upload_file**: Upload files to Google Drive
- **create_folder**: Create new folders in Google Drive
- **delete_file**: Delete files or folders
- **search_files**: Advanced file search with queries
- **share_file**: Share files with users or make them public
- **get_file_content**: Read text file contents directly

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Authenticate with Google

**Important**: Before using the MCP server, you need to authenticate:

```bash
python authenticate.py
```

This will:
1. Open a browser window for Google OAuth authentication
2. Create a `token.json` file to store your credentials
3. The MCP server will use this token automatically

### 3. Configure Your MCP Client

The MCP server is designed to be run by an MCP client (like Claude Desktop), **not directly**.
Add it to your MCP client configuration (see below).

## Configuration for MCP Clients

### For Claude Desktop (stdio mode - default)

Add this to your Claude Desktop MCP settings file:

**Location**: `~/.config/Claude/claude_desktop_config.json` (Linux)

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "python3",
      "args": ["/home/shadyskies/Desktop/mcp-tools/google_drive_mcp_server.py"],
      "cwd": "/home/shadyskies/Desktop/mcp-tools"
    }
  }
}
```

### For HTTP/SSE Transport

You can run the server with different transport modes:

**SSE (Server-Sent Events)**:
```bash
python google_drive_mcp_server.py --transport sse --host 0.0.0.0 --port 8000
```

**Streamable HTTP**:
```bash
python google_drive_mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8000
```

**stdio (default)**:
```bash
python google_drive_mcp_server.py --transport stdio
```

### For Other MCP Clients

Configure your MCP client to run:
- **Command**: `python3`
- **Args**: `["/home/shadyskies/Desktop/mcp-tools/google_drive_mcp_server.py"]`
- **Working Directory**: `/home/shadyskies/Desktop/mcp-tools`

Or for HTTP/SSE, connect to `http://localhost:8000` after starting the server.

## Usage Examples

### List Files
```json
{
  "tool": "list_files",
  "arguments": {
    "page_size": 20
  }
}
```

### Upload a File
```json
{
  "tool": "upload_file",
  "arguments": {
    "file_path": "/path/to/local/file.pdf",
    "name": "My Document.pdf"
  }
}
```

### Search Files
```json
{
  "tool": "search_files",
  "arguments": {
    "query": "name contains 'report' and mimeType='application/pdf'"
  }
}
```

### Share a File
```json
{
  "tool": "share_file",
  "arguments": {
    "file_id": "1234567890abcdef",
    "email": "user@example.com",
    "role": "reader"
  }
}
```

## Google Drive Query Syntax

For `search_files` and `list_files` queries, you can use:

- `name contains 'text'` - Files containing text in name
- `mimeType='application/pdf'` - Filter by MIME type
- `modifiedTime > '2024-01-01T00:00:00'` - Modified after date
- `'folder_id' in parents` - Files in specific folder
- Combine with `and`, `or`, `not`

## Common MIME Types

- PDF: `application/pdf`
- Folder: `application/vnd.google-apps.folder`
- Google Docs: `application/vnd.google-apps.document`
- Google Sheets: `application/vnd.google-apps.spreadsheet`
- Images: `image/jpeg`, `image/png`
- Text: `text/plain`

## Troubleshooting

### "token.json not found" Error
This means you haven't authenticated yet. Run:
```bash
python authenticate.py
```

### Authentication Issues
If you get authentication errors:
1. Delete `token.json`
2. Run `python authenticate.py` again
3. Complete the OAuth flow in your browser

### "Cannot run server directly" 
MCP servers are not meant to be run directly from the command line. They must be launched by an MCP client (like Claude Desktop) which communicates with them via JSON-RPC over stdin/stdout.

### Permission Denied
Make sure your OAuth credentials in `secret.json` have the correct scopes enabled in the Google Cloud Console.

## Security Notes

- Keep `secret.json` and `token.json` secure and never commit them to version control
- The server uses OAuth 2.0 for secure authentication
- Access tokens are refreshed automatically when they expire

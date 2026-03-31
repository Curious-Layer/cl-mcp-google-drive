**Manage files and folders in Google Drive via API.**

A Model Context Protocol (MCP) server that exposes Google Drive's API for managing, uploading, downloading, and sharing files seamlessly.

---

## Overview

The Google Drive MCP Server provides stateless, multi-user access to Google Drive's core operations:

- **File Management** — Create, list, search, and delete files and folders
- **File Operations** — Upload and download files with full control over destinations
- **Sharing & Permissions** — Share files with users or make them publicly accessible

Perfect for:

- Automated file organization and bulk operations
- Building AI-driven document workflows
- Integrating cloud storage into multi-agent systems

---

## Tools

<details>
<summary><code>list_files</code> — List files in Google Drive with filtering options</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object with credentials
- `folder_id` (string, optional) — Specific folder ID to list files from (default: null)
- `query` (string, optional) — Search query string for filtering (default: "")
- `page_size` (integer, optional) — Maximum items per page (default: 10)

**Output:**

```json
{
  "result": {
    "count": 5,
    "files": [
      {
        "id": "file-id-123",
        "name": "document.pdf",
        "mimeType": "application/pdf"
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/list_files

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "folder_id": "abc123xyz",
  "page_size": 10
}
```

</details>

---

<details>
<summary><code>get_file_metadata</code> — Get metadata for a specific file by ID</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `file_id` (string, required) — The file ID to retrieve metadata for

**Output:**

```json
{
  "result": {
    "id": "file-id-123",
    "name": "document.pdf",
    "mimeType": "application/pdf",
    "size": "1024000",
    "createdTime": "2026-03-19T10:00:00Z",
    "modifiedTime": "2026-03-19T12:00:00Z"
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/get_file_metadata

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "file_id": "file-id-123"
}
```

</details>

---

<details>
<summary><code>download_file</code> — Download a file from Google Drive to local disk</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `file_id` (string, required) — The file ID to download
- `destination_path` (string, required) — Local file path where file will be saved

**Output:**

```json
{
  "result": {
    "message": "File downloaded successfully to /path/to/file"
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/download_file

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "file_id": "file-id-123",
  "destination_path": "/home/user/downloads/document.pdf"
}
```

</details>

---

<details>
<summary><code>upload_file</code> — Upload a file to Google Drive</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `file_path` (string, required) — Local file path to upload
- `name` (string, optional) — Custom name for the file in Drive (default: null)
- `folder_id` (string, optional) — Target folder ID in Drive (default: null)
- `mime_type` (string, optional) — MIME type of the file (default: null)

**Output:**

```json
{
  "result": {
    "message": "File uploaded successfully",
    "file": {
      "id": "new-file-id-123",
      "name": "document.pdf",
      "webViewLink": "https://drive.google.com/file/d/new-file-id-123"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/upload_file

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "file_path": "/home/user/documents/report.pdf",
  "folder_id": "abc123xyz",
  "name": "Q1 Report"
}
```

</details>

---

<details>
<summary><code>create_folder</code> — Create a new folder in Google Drive</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `name` (string, required) — Name of the new folder
- `parent_folder_id` (string, optional) — Parent folder ID (default: null, creates in root)

**Output:**

```json
{
  "result": {
    "message": "Folder created successfully",
    "folder": {
      "id": "folder-id-456",
      "name": "New Folder",
      "mimeType": "application/vnd.google-apps.folder"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/create_folder

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "name": "Project Files",
  "parent_folder_id": "abc123xyz"
}
```

</details>

---

<details>
<summary><code>delete_file</code> — Delete a file or folder from Google Drive</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `file_id` (string, required) — The file or folder ID to delete

**Output:**

```json
{
  "result": {
    "message": "File deleted successfully"
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/delete_file

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "file_id": "file-id-123"
}
```

</details>

---

<details>
<summary><code>search_files</code> — Search for files in Google Drive using advanced queries</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `query` (string, required) — Search query using Drive API query syntax
- `page_size` (integer, optional) — Maximum items per page (default: 10)

**Output:**

```json
{
  "result": {
    "count": 3,
    "files": [
      {
        "id": "file-id-789",
        "name": "report.docx",
        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/search_files

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "query": "name contains 'report' and mimeType = 'application/pdf'",
  "page_size": 20
}
```

</details>

---

<details>
<summary><code>share_file</code> — Share a file with a user or make it publicly accessible</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `file_id` (string, required) — The file ID to share
- `email` (string, optional) — Email address to share with (default: null)
- `role` (string, optional) — Permission level: "reader", "commenter", or "writer" (default: "reader")
- `share_type` (string, optional) — Type of sharing: "user", "group", "domain", or "anyone" (default: null)

**Output:**

```json
{
  "result": {
    "message": "File shared successfully",
    "permission_id": "perm-id-123",
    "webViewLink": "https://drive.google.com/file/d/file-id-123",
    "webContentLink": "https://drive.google.com/uc?id=file-id-123&export=download"
  }
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/share_file

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "file_id": "file-id-123",
  "email": "user@example.com",
  "role": "reader"
}
```

</details>

---

<details>
<summary><code>get_file_content</code> — Get the content of a text file from Google Drive</summary>

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `file_id` (string, required) — The text file ID to retrieve content from

**Output:**

```json
{
  "result": "File content as raw text string"
}
```

**Usage Example:**

```bash
POST /mcp/google-drive/get_file_content

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "file_id": "file-id-123"
}

```

</details>

---

## Reference & Support

<details>
<summary><strong>API Parameters Reference</strong></summary>

### Pagination

- `page_size` — Maximum results per page (default: 10)
- `page_token` — Token from previous response for paginating through results

### Query & Filtering

- `query` — Drive API query filter (e.g., `name contains 'report'`, `mimeType = 'application/pdf'`)

### Resource Formats

**File Resource:**

```
files/{FILE_ID}
Example: files/abc123xyz789def456
```

**Folder Resource:**

```
folders/{FOLDER_ID}
Example: folders/abc123xyz789def456
```

**MIME Types:**

```
application/pdf — PDF document
application/vnd.google-apps.document — Google Docs
application/vnd.google-apps.spreadsheet — Google Sheets
application/vnd.openxmlformats-officedocument.wordprocessingml.document — Word Document
text/plain — Plain text file
```

</details>

---

<details>
<summary><strong>OAuth Guide</strong></summary>

All tools require a valid Google OAuth token. Here's how to obtain one:

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Drive API** from the API Library

### Step 2: Create OAuth 2.0 Credentials

1. Navigate to **Credentials** in Google Cloud Console
2. Click **+ Create Credentials** → **OAuth client ID**
3. Select your application type (Desktop, Web, or other)
4. Download the credentials JSON file

### Step 3: Authenticate with Google

Use your Google account to authenticate and obtain the OAuth token. Refer to [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2) for detailed authentication steps specific to your use case.

### Step 4: Required Scopes

Ensure your OAuth token has these scopes:

- `https://www.googleapis.com/auth/drive` — Full Drive access (read, write, delete)
- `https://www.googleapis.com/auth/drive.file` — Access only to files created by the app
- `https://www.googleapis.com/auth/drive.readonly` — Read-only access to all files

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### **Missing or Invalid API Key**

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` header is present
  2. Check API key is active in your Curious Layer account
  3. Regenerate API key if expired

### **Rate Limit Exceeded**

- **Cause:** Too many requests sent to the API gateway
- **Solution:**
  1. Check rate limit headers in response: `X-RateLimit-Remaining`
  2. Implement exponential backoff for retries
  3. Spread requests over time

### **Insufficient Credits**

- **Cause:** API calls have exceeded your requests limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

### **Malformed Request Payload**

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values (string, integer, etc.)

### **Server Not Found**

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `/mcp/{server-name}/{tool-name}`
  2. Use lowercase server name: `/mcp/google-drive/...`
  3. Check available servers in documentation

### **OAuth Token Invalid or Expired**

- **Cause:** Token rejected by Google API or has expired
- **Solution:**
  1. Obtain a fresh OAuth token from Google
  2. Verify token has all required scopes
  3. Check token expiration and refresh if needed

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Google Drive API Documentation](https://developers.google.com/drive/api)** — Official API reference
- **[Google Cloud OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)** — Authentication setup guide
- **[Google Drive API Reference](https://developers.google.com/drive/api/v3/reference)** — Complete API endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification

</details>

---
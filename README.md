**Upload, search, and manage Google Drive files — directly from your AI workflows.**

A Model Context Protocol (MCP) server that exposes Google Drive's API for listing, searching, uploading, downloading, sharing, and organizing files and folders.


## Overview

The Google Drive MCP Server provides full programmatic access to Google Drive through a stateless, multi-tenant interface:

- List, search, upload, and download files using Drive's native query syntax
- Create and organize folders, manage file permissions and sharing
- Read text file content directly without downloading to disk

Perfect for:

- Automating file management and document workflows from AI agents
- Building assistants that can read, organize, and share Drive files
- Integrating Google Drive actions into LLM-powered pipelines


## Tools

<details>
<summary><code>list_files</code> — List files in Google Drive</summary>

Lists files in Google Drive with optional filtering by parent folder, name, or type.

**Inputs:**
```
- `folder_id` (string, optional) — Parent folder ID to filter results by
- `query` (string, optional) — Additional Drive query fragment e.g. `name contains 'report'`
- `page_size` (integer, optional) — Maximum number of results to return, capped at 1000. Default: `10`
```

**Output:**

```json
{
  "count": 3,
  "files": [
    {
      "id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs",
      "name": "report.pdf",
      "mimeType": "application/pdf",
      "size": "204800",
      "createdTime": "2024-01-15T10:00:00.000Z",
      "modifiedTime": "2024-03-20T14:30:00.000Z",
      "webViewLink": "https://drive.google.com/file/d/..."
    }
  ]
}
```

</details>


<details>
<summary><code>get_file_metadata</code> — Get metadata for a specific file by ID</summary>

Returns the full metadata object for a single file or folder.

**Inputs:**
```
- `file_id` (string, required) — Google Drive file ID
```

**Output:**

```json
{
  "id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs",
  "name": "report.pdf",
  "mimeType": "application/pdf",
  "size": "204800",
  "createdTime": "2024-01-15T10:00:00.000Z",
  "modifiedTime": "2024-03-20T14:30:00.000Z",
  "owners": [{ "displayName": "John Doe", "emailAddress": "john@example.com" }],
  "webViewLink": "https://drive.google.com/file/d/..."
}
```

</details>


<details>
<summary><code>download_file</code> — Download a file from Google Drive to local disk</summary>

Downloads a file from Drive and writes it to a specified local path.

**Inputs:**
```
- `file_id` (string, required) — Google Drive file ID
- `destination_path` (string, required) — Local filesystem path to save the file to
```

**Output:**

```json
{
  "message": "File downloaded successfully to: /path/to/file.pdf"
}
```

</details>


<details>
<summary><code>upload_file</code> — Upload a file to Google Drive</summary>

Uploads a local file to Google Drive with an optional destination name, folder, and MIME type.

**Inputs:**
```
- `file_path` (string, required) — Local filesystem path of the file to upload
- `name` (string, optional) — Destination filename in Drive. Defaults to the local filename
- `folder_id` (string, optional) — Parent folder ID in Drive to upload into
- `mime_type` (string, optional) — MIME type of the file e.g. `text/plain`, `application/pdf`
```

**Output:**

```json
{
  "message": "File uploaded successfully",
  "file": {
    "id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs",
    "name": "report.pdf",
    "webViewLink": "https://drive.google.com/file/d/..."
  }
}
```

</details>


<details>
<summary><code>create_folder</code> — Create a new folder in Google Drive</summary>

Creates a new folder, optionally nested inside a parent folder.

**Inputs:**
```
- `name` (string, required) — Folder name
- `parent_folder_id` (string, optional) — Parent folder ID to create the folder inside
```

**Output:**

```json
{
  "message": "Folder created successfully",
  "folder": {
    "id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs",
    "name": "Projects",
    "webViewLink": "https://drive.google.com/drive/folders/..."
  }
}
```

</details>


<details>
<summary><code>delete_file</code> — Delete a file or folder from Google Drive</summary>

Permanently deletes a file or folder. This action cannot be undone.

**Inputs:**
```
- `file_id` (string, required) — Google Drive file or folder ID to delete
```

**Output:**

```json
{
  "message": "File/folder with ID 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs deleted successfully"
}
```

</details>


<details>
<summary><code>search_files</code> — Search for files in Google Drive using advanced queries</summary>

Searches Drive using the full Drive query expression language and returns matching file metadata.

**Inputs:**
```
- `query` (string, required) — Drive query expression e.g. `name contains 'report'`, `mimeType='application/pdf'`
- `page_size` (integer, optional) — Maximum number of results to return, capped at 1000. Default: `10`
```

**Output:**

```json
{
  "count": 2,
  "files": [
    {
      "id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs",
      "name": "Q1 Report.pdf",
      "mimeType": "application/pdf",
      "webViewLink": "https://drive.google.com/file/d/..."
    }
  ]
}
```

</details>


<details>
<summary><code>share_file</code> — Share a file with a user or make it publicly accessible</summary>

Grants a permission on a file, either to a specific user or to anyone with the link.

**Inputs:**
```
- `file_id` (string, required) — Google Drive file ID
- `email` (string, optional) — Recipient email address when sharing with a specific user
- `role` (string, optional) — Permission role. Values: `reader`, `commenter`, `writer`. Default: `reader`
- `share_type` (string, optional) — Permission type. Values: `user`, `group`, `domain`, `anyone`. Defaults to `user` if email is provided, otherwise `anyone`
```

**Output:**

```json
{
  "message": "File shared successfully",
  "permission_id": "anyoneWithLink",
  "webViewLink": "https://drive.google.com/file/d/.../view",
  "webContentLink": "https://drive.google.com/uc?id=..."
}
```

</details>


<details>
<summary><code>get_file_content</code> — Get the content of a text file from Google Drive</summary>

Reads and returns the decoded text content of a file directly, without saving to disk.

**Inputs:**
```
- `file_id` (string, required) — Google Drive file ID
```

**Output:**

```json
"The full decoded text content of the file as a string."
```

</details>


## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `file_id` — Unique Google Drive file or folder identifier. Obtain from `list_files`, `search_files`, or any file response.
- `folder_id` — ID of a Drive folder. Use `list_files` or `search_files` with `mimeType='application/vnd.google-apps.folder'` to find folder IDs.
- `page_size` — Limits the number of items returned. Always capped at 1000.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Drive Query Syntax (`query` parameter):**

```
name contains 'report'                          — Files with "report" in name
name = 'budget.xlsx'                            — Exact filename match
mimeType = 'application/pdf'                    — Files of a specific MIME type
mimeType = 'application/vnd.google-apps.folder' — Folders only
'folder_id' in parents                          — Files inside a specific folder
modifiedTime > '2024-01-01T00:00:00'            — Files modified after a date
fullText contains 'quarterly'                   — Files containing text (Docs/Sheets only)
```

**Permission Roles:**

```
reader     — View only
commenter  — View and comment
writer     — View, comment, and edit
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Google Drive credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Google Drive API Error</strong></summary>

- **Cause:** Upstream Google Drive API returned an error
- **Solution:**
  1. Check Google service status at [Google Workspace Status Page](https://www.google.com/appsstatus)
  2. Verify your credential has the required Drive permissions
  3. Review the error message for specific details

</details>

---

### Resources

- **[Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)** — Official API reference
- **[Google Drive API Reference](https://developers.google.com/drive/api/reference/rest/v3)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

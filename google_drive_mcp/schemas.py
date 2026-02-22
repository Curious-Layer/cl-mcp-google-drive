from typing import Any, TypedDict


class ToolError(TypedDict):
    error: str


class OAuthTokenData(TypedDict, total=False):
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]


class FilesListResponse(TypedDict):
    count: int
    files: list[dict[str, Any]]


class MessageResponse(TypedDict):
    message: str


class UploadFileResponse(TypedDict):
    message: str
    file: dict[str, Any]


class CreateFolderResponse(TypedDict):
    message: str
    folder: dict[str, Any]


class ShareFileResponse(TypedDict, total=False):
    message: str
    permission_id: str
    webViewLink: str
    webContentLink: str


FilesListToolResponse = FilesListResponse | ToolError
MessageToolResponse = MessageResponse | ToolError
UploadFileToolResponse = UploadFileResponse | ToolError
CreateFolderToolResponse = CreateFolderResponse | ToolError
ShareFileToolResponse = ShareFileResponse | ToolError
ApiObjectResponse = dict[str, Any] | ToolError

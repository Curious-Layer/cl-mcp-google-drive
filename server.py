#!/usr/bin/env python3
"""MCP Server for Google Drive API."""

import logging
import os

from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, MewCPCredentialBackend, EnvCredentialBackend

from google_drive_mcp.cli import parse_args
from google_drive_mcp.config import configure_logging
from google_drive_mcp.tools import register_tools

configure_logging()
logger = logging.getLogger("google-drive-mcp-server")


def _build_backend():
    """
    Select credential backend based on environment.

    MewCP hosted:  set MEWCP_DB_URL + MEWCP_ENCRYPTION_KEY
    Local / OSS:   set GOOGLE_DRIVE_ACCESS_TOKEN, GOOGLE_DRIVE_REFRESH_TOKEN, etc.
    """
    if os.environ.get("MEWCP_DB_URL"):
        logger.info("Using MewCPCredentialBackend (MongoDB + AES-256 encryption)")
        return MewCPCredentialBackend(
            db_url=os.environ["MEWCP_DB_URL"],
            db_name=os.environ.get("MEWCP_DB_NAME", "mewcp"),
        )
    logger.info("Using EnvCredentialBackend (local / open-source mode)")
    return EnvCredentialBackend(prefix="GOOGLE_DRIVE_")


backend = _build_backend()
mcp = FastMCP("CL Google Drive MCP Server", middleware=[CredentialMiddleware(backend)])
register_tools(mcp)

# Expose ASGI app for hosting platforms (e.g. Vercel).
app = mcp.http_app(path="/mcp", transport="streamable-http")


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Google Drive MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

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
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise

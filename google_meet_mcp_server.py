#!/usr/bin/env python3
"""
MCP Server for Google Meet API
Provides access to Google Meet operations through Model Context Protocol

Documentation referred : https://googleapis.github.io/google-api-python-client/docs/dyn/meet_v2.html
"""

import json
import logging
import argparse
from typing import Dict

from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Google Meet API scopes
SCOPES = [
    "https://www.googleapis.com/auth/meetings.space.created",
    "https://www.googleapis.com/auth/meetings.space.readonly",
    "https://www.googleapis.com/auth/meetings.space.settings",
    "https://www.googleapis.com/auth/drive.readonly",
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("google-meet-mcp-server")

# Create FastMCP instance
mcp = FastMCP("CL Google Meet MCP Server")

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
    """Create Google Meet service with provided access token"""
    auth_data = _get_token_data(token_data)
    logger.info("Creating Google Meet API service with provided access token")
    creds = Credentials(**auth_data)
    service = build("meet", "v2", credentials=creds)
    logger.info("Google Meet API service created successfully")
    return service


# =======================================================================================
#                       MCP TOOLS START
# =======================================================================================


@mcp.tool(
    name="create_meeting_space", description="Create a new Google Meet meeting space"
)
def create_meeting_space(token_data: str) -> str:
    """
    Creates a new Google Meet meeting space.

    :param token_data: The JSON string of the user's access token.
    :return: A JSON string of the created meeting space.
    """
    try:
        service = _get_service(token_data)
        space = {}  # An empty body creates a space with default settings
        """
        
        space = {
        "name": string,
        "meetingUri": string,
        "meetingCode": string,
        "config": {
            object (SpaceConfig)
        },
        "activeConference": {
            object (ActiveConference)
        }
        
        """
        response = service.spaces().create(body=space).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create meeting space: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="get_meeting_space",
    description="Retrieve details for a given Google Meet meeting space",
)
def get_meeting_space(token_data: str, name: str) -> str:
    """
    Retrieves details for a given Google Meet meeting space.

    :param token_data: The JSON string of the user's access token.
    :param name: The name of the space to retrieve, e.g., "spaces/aaa-bbbb-ccc".
    :return: A JSON string of the meeting space details.
    """
    try:
        service = _get_service(token_data)
        response = service.spaces().get(name=name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get meeting space '{name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="end_meeting_space",
    description="End a Google Meet meeting space",
)
def end_meeting_space(token_data: str, name: str) -> str:
    """
    Ends a Google Meet meeting space.

    :param token_data: The JSON string of the user's access token.
    :param name: The name of the space to end, e.g., "spaces/aaa-bbbb-ccc".
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.spaces().end(name=name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to end meeting space '{name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="update_meeting_space",
    description="Update a Google Meet meeting space",
)
def update_meeting_space(
    token_data: str, name: str, update_mask: str, space: str
) -> str:
    """
    Updates a Google Meet meeting space.

    :param token_data: The JSON string of the user's access token.
    :param name: The name of the space to update, e.g., "spaces/aaa-bbbb-ccc".
    :param update_mask: The field mask specifying which fields to update.
    :param space: A JSON string representing the updated space details.
    :return: A JSON string of the updated meeting space.
    """
    try:
        service = _get_service(token_data)
        space_dict = json.loads(space)
        response = (
            service.spaces()
            .patch(name=name, updateMask=update_mask, body=space_dict)
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to update meeting space '{name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="get_conference_record",
    description="Get a Google Meet conference record",
)
def get_conference_record(token_data: str, name: str) -> str:
    """
    Gets a Google Meet conference record.

    :param token_data: The JSON string of the user's access token.
    :param name: The name of the conference record to retrieve, e.g., "conferenceRecords/aaa-bbbb-ccc".
    :return: A JSON string of the conference record.
    """
    try:
        service = _get_service(token_data)
        response = service.conferenceRecords().get(name=name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get conference record '{name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="list_conference_records",
    description="List Google Meet conference records",
)
def list_conference_records(
    token_data: str, page_size: int = None, page_token: str = None
) -> str:
    """
    Lists Google Meet conference records.

    :param token_data: The JSON string of the user's access token.
    :param page_size: The maximum number of conference records to return.
    :param page_token: The page token from a previous list request.
    :return: A JSON string of the conference records.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.conferenceRecords()
            .list(pageSize=page_size, pageToken=page_token)
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list conference records: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="get_participant",
    description="Get a participant from a Google Meet conference record",
)
def get_participant(token_data: str, name: str) -> str:
    """
    Gets a participant from a Google Meet conference record.

    :param token_data: The JSON string of the user's access token.
    :param name: The name of the participant to retrieve, e.g., "conferenceRecords/{conference_record}/participants/{participant}".
    :return: A JSON string of the participant.
    """
    try:
        service = _get_service(token_data)
        response = service.conferenceRecords().participants().get(name=name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get participant '{name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="list_participants",
    description="List participants from a Google Meet conference record",
)
def list_participants(
    token_data: str,
    parent: str,
    page_size: int = None,
    page_token: str = None,
    filter: str = None,
) -> str:
    """
    Lists participants from a Google Meet conference record.

    :param token_data: The JSON string of the user's access token.
    :param parent: The parent conference record, e.g., "conferenceRecords/{conference_record}".
    :param page_size: The maximum number of participants to return.
    :param page_token: The page token from a previous list request.
    :param filter: A filter for the list request.
    :return: A JSON string of the participants.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.conferenceRecords()
            .participants()
            .list(
                parent=parent,
                pageSize=page_size,
                pageToken=page_token,
                filter=filter,
            )
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list participants for '{parent}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="get_participant_session",
    description="Get a participant session from a Google Meet conference record by participant session ID.",
)
def get_participant_session(token_data: str, name: str) -> str:
    """
    Get a participant session from a Google Meet conference record by participant session ID.

    :param token_data: The JSON string of the user's access token.
    :param name: The name of the participant session to retrieve, e.g., "conferenceRecords/{conference_record}/participants/{participant}/participantSessions/{participant_session}".
    :return: A JSON string of the participant session.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.conferenceRecords()
            .participants()
            .participantSessions()
            .get(name=name)
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get participant session '{name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="list_participant_sessions",
    description="List participant sessions of a participant from a Google Meet conference record",
)
def list_participant_sessions(
    token_data: str,
    parent: str,
    page_size: int = None,
    page_token: str = None,
    filter: str = None,
) -> str:
    """
    List participant sessions of a participant from a Google Meet conference record

    :param token_data: The JSON string of the user's access token.
    :param parent: The parent participant, e.g., "conferenceRecords/{conference_record}/participants/{participant}".
    :param page_size: The maximum number of participant sessions to return.
    :param page_token: The page token from a previous list request.
    :param filter: A filter for the list request.
    :return: A JSON string of the participant sessions.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.conferenceRecords()
            .participants()
            .participantSessions()
            .list(
                parent=parent,
                pageSize=page_size,
                pageToken=page_token,
                filter=filter,
            )
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list participant sessions for '{parent}': {e}")
        return json.dumps({"error": str(e)})


# =======================================================================================
#                       MCP TOOLS END
# =======================================================================================


# Function for parsing the cmd-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Google Meet MCP Server")
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
    logger.info("Google Meet MCP Server Starting")
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

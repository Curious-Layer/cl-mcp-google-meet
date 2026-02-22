import json
import logging

from fastmcp import FastMCP

from .schemas import OAuthTokenData
from .service import get_service

logger = logging.getLogger("google-meet-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="create_meeting_space", description="Create a new Google Meet meeting space"
    )
    def create_meeting_space(token_data: OAuthTokenData) -> str:
        try:
            service = get_service(token_data)
            space = {}
            response = service.spaces().create(body=space).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to create meeting space: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="get_meeting_space",
        description="Retrieve details for a given Google Meet meeting space",
    )
    def get_meeting_space(token_data: OAuthTokenData, name: str) -> str:
        try:
            service = get_service(token_data)
            response = service.spaces().get(name=name).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to get meeting space '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(name="end_meeting_space", description="End a Google Meet meeting space")
    def end_meeting_space(token_data: OAuthTokenData, name: str) -> str:
        try:
            service = get_service(token_data)
            response = service.spaces().end(name=name).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to end meeting space '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(name="update_meeting_space", description="Update a Google Meet meeting space")
    def update_meeting_space(
        token_data: OAuthTokenData, name: str, update_mask: str, space: str
    ) -> str:
        try:
            service = get_service(token_data)
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
    def get_conference_record(token_data: OAuthTokenData, name: str) -> str:
        try:
            service = get_service(token_data)
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
        token_data: OAuthTokenData,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> str:
        try:
            service = get_service(token_data)
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
    def get_participant(token_data: OAuthTokenData, name: str) -> str:
        try:
            service = get_service(token_data)
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
        token_data: OAuthTokenData,
        parent: str,
        page_size: int | None = None,
        page_token: str | None = None,
        filter: str | None = None,
    ) -> str:
        try:
            service = get_service(token_data)
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
    def get_participant_session(token_data: OAuthTokenData, name: str) -> str:
        try:
            service = get_service(token_data)
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
        token_data: OAuthTokenData,
        parent: str,
        page_size: int | None = None,
        page_token: str | None = None,
        filter: str | None = None,
    ) -> str:
        try:
            service = get_service(token_data)
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

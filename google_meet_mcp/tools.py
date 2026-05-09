import json
import logging

from fastmcp import FastMCP
from .service import get_service
from pydantic import Field

logger = logging.getLogger("google-meet-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="create_meeting_space",
        description="Create a new Google Meet meeting space",
    )
    def create_meeting_space() -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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
    def get_meeting_space(
        name: str = Field(
            description="Space resource name, e.g. `spaces/abc-defg-hij`"
        ),
    ) -> str:
        """

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
            response = service.spaces().get(name=name).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to get meeting space '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(name="end_meeting_space", description="End a Google Meet meeting space")
    def end_meeting_space(
        name: str = Field(
            description="Space resource name, e.g. `spaces/abc-defg-hij`"
        ),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
            response = service.spaces().end(name=name).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to end meeting space '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="update_meeting_space", description="Update a Google Meet meeting space"
    )
    def update_meeting_space(
        name: str = Field(
            description="Space resource name, e.g. `spaces/abc-defg-hij`"
        ),
        update_mask: str = Field(
            description="Comma-separated field mask for patch operation"
        ),
        space: str = Field(
            description="JSON string body containing updated space fields"
        ),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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
    def get_conference_record(
        name: str = Field(
            description="Conference record resource name 'conferenceRecords/id' "
        ),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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
        page_size: int | None = Field(
            default=None, description="Optional max items per page"
        ),
        page_token: str | None = Field(
            default=None, description="Optional token from previous page"
        ),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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
    def get_participant(
        name: str = Field(description="Participant resource name"),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
            response = (
                service.conferenceRecords().participants().get(name=name).execute()
            )
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to get participant '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="list_participants",
        description="List participants from a Google Meet conference record",
    )
    def list_participants(
        parent: str = Field(description="Parent conference record resource name"),
        page_size: int | None = Field(
            default=None, description="Optional max items per page"
        ),
        page_token: str | None = Field(
            default=None, description="Optional token from previous page"
        ),
        filter: str | None = Field(
            default=None, description="Optional API filter expression"
        ),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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
    def get_participant_session(
        name: str = Field(description="Participant session resource name"),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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
        parent: str = Field(description="Parent participant resource name"),
        page_size: int | None = Field(
            default=None, description="Optional max items per page"
        ),
        page_token: str | None = Field(
            default=None, description="Optional token from previous page"
        ),
        filter: str | None = Field(
            default=None, description="Optional API filter expression"
        ),
    ) -> str:
        """
        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service()
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

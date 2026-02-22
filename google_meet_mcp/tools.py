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
    def create_meeting_space(oauth_token: OAuthTokenData) -> str:
        """Create a Google Meet space with default settings.

        Args:
            oauth_token: OAuth credentials object with token fields.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
    def get_meeting_space(oauth_token: OAuthTokenData, name: str) -> str:
        """Get details of an existing Meet space.

        Args:
            oauth_token: OAuth credentials object with token fields.
            name: Space resource name, e.g. `spaces/abc-defg-hij`.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
            response = service.spaces().get(name=name).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to get meeting space '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(name="end_meeting_space", description="End a Google Meet meeting space")
    def end_meeting_space(oauth_token: OAuthTokenData, name: str) -> str:
        """End an active Meet space.

        Args:
            oauth_token: OAuth credentials object with token fields.
            name: Space resource name, e.g. `spaces/abc-defg-hij`.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
            response = service.spaces().end(name=name).execute()
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Failed to end meeting space '{name}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(name="update_meeting_space", description="Update a Google Meet meeting space")
    def update_meeting_space(
        oauth_token: OAuthTokenData, name: str, update_mask: str, space: str
    ) -> str:
        """Update selected fields of a Meet space.

        Args:
            oauth_token: OAuth credentials object with token fields.
            name: Space resource name, e.g. `spaces/abc-defg-hij`.
            update_mask: Comma-separated field mask for patch operation.
            space: JSON string body containing updated space fields.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
    def get_conference_record(oauth_token: OAuthTokenData, name: str) -> str:
        """Get a conference record by name.

        Args:
            oauth_token: OAuth credentials object with token fields.
            name: Record resource name, e.g. `conferenceRecords/{id}`.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
        oauth_token: OAuthTokenData,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> str:
        """List conference records.

        Args:
            oauth_token: OAuth credentials object with token fields.
            page_size: Optional max items per page.
            page_token: Optional token from previous page.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
    def get_participant(oauth_token: OAuthTokenData, name: str) -> str:
        """Get a participant resource.

        Args:
            oauth_token: OAuth credentials object with token fields.
            name: Participant resource name,
                `conferenceRecords/{record}/participants/{participant}`.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
        oauth_token: OAuthTokenData,
        parent: str,
        page_size: int | None = None,
        page_token: str | None = None,
        filter: str | None = None,
    ) -> str:
        """List participants under a conference record.

        Args:
            oauth_token: OAuth credentials object with token fields.
            parent: Parent conference record, `conferenceRecords/{record}`.
            page_size: Optional max items per page.
            page_token: Optional token from previous page.
            filter: Optional API filter expression.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
    def get_participant_session(oauth_token: OAuthTokenData, name: str) -> str:
        """Get a participant session by full resource name.

        Args:
            oauth_token: OAuth credentials object with token fields.
            name: Participant session resource name,
                `conferenceRecords/{record}/participants/{participant}/participantSessions/{session}`.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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
        oauth_token: OAuthTokenData,
        parent: str,
        page_size: int | None = None,
        page_token: str | None = None,
        filter: str | None = None,
    ) -> str:
        """List participant sessions under a participant resource.

        Args:
            oauth_token: OAuth credentials object with token fields.
            parent: Parent participant resource,
                `conferenceRecords/{record}/participants/{participant}`.
            page_size: Optional max items per page.
            page_token: Optional token from previous page.
            filter: Optional API filter expression.

        Returns:
            JSON-serialized API response string, or JSON error string.
        """
        try:
            service = get_service(oauth_token)
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

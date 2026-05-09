**Create, manage, and inspect Google Meet sessions — directly from your AI workflows.**

A Model Context Protocol (MCP) server that exposes Google Meet's API for creating meeting spaces, managing conference records, and retrieving participant information.

---

## Overview

The Google Meet MCP Server provides full programmatic access to Google Meet through a stateless, multi-tenant interface:

- Create, update, and end Google Meet meeting spaces
- Retrieve conference records and meeting history
- List and inspect participants and their session details

Perfect for:

- Automating meeting creation and management from AI agents
- Building assistants that can schedule, start, and end Meet sessions
- Analyzing meeting attendance and participant data in LLM-powered pipelines

---

## Tools

<details>
<summary><code>create_meeting_space</code> — Create a new Google Meet meeting space</summary>

Creates a new Google Meet meeting space and returns its details including the join link.

**Inputs:**
```
None
```

**Output:**

```json
{
  "name": "spaces/abc-defg-hij",
  "meetingUri": "https://meet.google.com/abc-defg-hij",
  "meetingCode": "abc-defg-hij"
}
```

</details>



<details>
<summary><code>get_meeting_space</code> — Retrieve details for a Google Meet meeting space</summary>

Fetches the current details of an existing meeting space by its resource name.

**Inputs:**
```
- `name` (string, required) — Space resource name e.g. `spaces/abc-defg-hij`
```

**Output:**

```json
{
  "name": "spaces/abc-defg-hij",
  "meetingUri": "https://meet.google.com/abc-defg-hij",
  "meetingCode": "abc-defg-hij",
  "config": { "accessType": "OPEN" }
}
```

</details>


<details>
<summary><code>end_meeting_space</code> — End a Google Meet meeting space</summary>

Ends an active meeting space, disconnecting all participants.

**Inputs:**
```
- `name` (string, required) — Space resource name e.g. `spaces/abc-defg-hij`
```

**Output:**

```json
{}
```

</details>



<details>
<summary><code>update_meeting_space</code> — Update a Google Meet meeting space</summary>

Patches one or more fields of an existing meeting space using a field mask.

**Inputs:**
```
- `name` (string, required) — Space resource name e.g. `spaces/abc-defg-hij`
- `update_mask` (string, required) — Comma-separated field mask for the patch operation e.g. `config.accessType`
- `space` (string, required) — JSON string containing the updated space fields e.g. `{"config": {"accessType": "TRUSTED"}}`
```

**Output:**

```json
{
  "name": "spaces/abc-defg-hij",
  "meetingUri": "https://meet.google.com/abc-defg-hij",
  "config": { "accessType": "TRUSTED" }
}
```

</details>


<details>
<summary><code>get_conference_record</code> — Get a Google Meet conference record</summary>

Retrieves a single conference record by its resource name.

**Inputs:**
```
- `name` (string, required) — Conference record resource name e.g. `conferenceRecords/abc123`
```

**Output:**

```json
{
  "name": "conferenceRecords/abc123",
  "startTime": "2024-03-20T10:00:00.000Z",
  "endTime": "2024-03-20T11:00:00.000Z",
  "space": "spaces/abc-defg-hij"
}
```

</details>


<details>
<summary><code>list_conference_records</code> — List Google Meet conference records</summary>

Returns a paginated list of past conference records for the authenticated user.

**Inputs:**
```
- `page_size` (integer, optional) — Maximum number of records per page
- `page_token` (string, optional) — Pagination token from a previous response
```

**Output:**

```json
{
  "conferenceRecords": [
    {
      "name": "conferenceRecords/abc123",
      "startTime": "2024-03-20T10:00:00.000Z",
      "endTime": "2024-03-20T11:00:00.000Z",
      "space": "spaces/abc-defg-hij"
    }
  ],
  "nextPageToken": "token123"
}
```

</details>

<details>
<summary><code>get_participant</code> — Get a participant from a conference record</summary>

Retrieves details of a single participant from a conference record.

**Inputs:**
```
- `name` (string, required) — Participant resource name e.g. `conferenceRecords/abc123/participants/xyz`
```

**Output:**

```json
{
  "name": "conferenceRecords/abc123/participants/xyz",
  "signedinUser": {
    "user": "users/123",
    "displayName": "Jane Doe"
  },
  "earliestStartTime": "2024-03-20T10:02:00.000Z",
  "latestEndTime": "2024-03-20T10:58:00.000Z"
}
```

</details>


<details>
<summary><code>list_participants</code> — List participants from a conference record</summary>

Returns a paginated list of participants for a given conference record.

**Inputs:**
```
- `parent` (string, required) — Parent conference record resource name e.g. `conferenceRecords/abc123`
- `page_size` (integer, optional) — Maximum number of participants per page
- `page_token` (string, optional) — Pagination token from a previous response
- `filter` (string, optional) — API filter expression e.g. `signedinUser.user='users/123'`
```

**Output:**

```json
{
  "participants": [
    {
      "name": "conferenceRecords/abc123/participants/xyz",
      "signedinUser": { "displayName": "Jane Doe" }
    }
  ],
  "nextPageToken": "token123"
}
```

</details>


<details>
<summary><code>get_participant_session</code> — Get a participant session from a conference record</summary>

Retrieves a single participant session, representing one continuous join/leave interval.

**Inputs:**
```
- `name` (string, required) — Participant session resource name e.g. `conferenceRecords/abc123/participants/xyz/participantSessions/session1`
```

**Output:**

```json
{
  "name": "conferenceRecords/abc123/participants/xyz/participantSessions/session1",
  "startTime": "2024-03-20T10:02:00.000Z",
  "endTime": "2024-03-20T10:30:00.000Z"
}
```

</details>


<details>
<summary><code>list_participant_sessions</code> — List participant sessions of a participant</summary>

Returns a paginated list of all sessions for a given participant in a conference record.

**Inputs:**
```
- `parent` (string, required) — Parent participant resource name e.g. `conferenceRecords/abc123/participants/xyz`
- `page_size` (integer, optional) — Maximum number of sessions per page
- `page_token` (string, optional) — Pagination token from a previous response
- `filter` (string, optional) — API filter expression
```

**Output:**

```json
{
  "participantSessions": [
    {
      "name": "conferenceRecords/abc123/participants/xyz/participantSessions/session1",
      "startTime": "2024-03-20T10:02:00.000Z",
      "endTime": "2024-03-20T10:30:00.000Z"
    }
  ],
  "nextPageToken": "token123"
}
```

</details>

---
<details>
<summary><strong>API Parameters Reference</strong></summary>

### Common Parameters

- `name` — Full resource name identifying a Meet object. Always returned in API responses and used as the identifier for subsequent calls.
- `page_size` — Limits the number of items returned per page. If omitted, the API uses its default page size.
- `page_token` — Token from a previous paginated response. Pass it to retrieve the next page of results.
- `filter` — Standard API filter expression for narrowing list results.

### Resource Name Formats

**Meeting Space:**

```
spaces/{spaceId}
Example: spaces/abc-defg-hij
```

**Conference Record:**

```
conferenceRecords/{recordId}
Example: conferenceRecords/abc123xyz
```

**Participant:**

```
conferenceRecords/{recordId}/participants/{participantId}
Example: conferenceRecords/abc123/participants/p456
```

**Participant Session:**

```
conferenceRecords/{recordId}/participants/{participantId}/participantSessions/{sessionId}
Example: conferenceRecords/abc123/participants/p456/participantSessions/s789
```

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### **Missing or Invalid Headers**

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

### **Insufficient Credits**

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

### **Credential Not Connected**

- **Cause:** No Google credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

### **Malformed Request Payload**

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

### **Server Not Found**

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

### **Google Meet API Error**

- **Cause:** Upstream Google Meet API returned an error
- **Solution:**
  1. Check Google service status at [Google Workspace Status Page](https://www.google.com/appsstatus)
  2. Verify your credential has the required Meet permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Google Meet API Documentation](https://developers.google.com/meet/api/guides/overview)** — Official API reference
- **[Google Meet API Reference](https://developers.google.com/meet/api/reference/rest)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>

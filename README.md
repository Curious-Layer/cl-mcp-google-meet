# Google Meet MCP Server

This project is a server that lets you control Google Meet using simple commands. Think of it like a remote control for Google Meet! MCP stands for "Model Context Protocol," which is just a fancy way of saying it's a special kind of server.

## What it does

This server provides a set of "tools" that you can use to do things like:
*   Create new Google Meet meetings
*   Get information about your meetings
*   See who attended your meetings

## Setup

### 1. Install the requirements
First, you need to install the necessary libraries. You can do this by running the following command in your terminal:
```bash
pip install -r requirements.txt
```

### 2. Authentication
To use this server, you need to give it permission to access your Google Meet account. This is done using a special token. The server expects this token to be provided when you use a tool.

## How to run the server
You can start the server by running the following command in your terminal:
```bash
python google_meet_mcp_server.py
```

## Available Tools

Here are the tools you can use with this server:

### Meeting Spaces
A "meeting space" is just another name for a Google Meet meeting.

*   **`create_meeting_space`**: Creates a new Google Meet meeting.
*   **`get_meeting_space`**: Gets information about a specific meeting. You need to provide the name of the meeting space, which looks something like `spaces/aaa-bbbb-ccc`.
*   **`end_meeting_space`**: Ends a meeting.
*   **`update_meeting_space`**: Changes the settings of a meeting.

### Conference Records
A "conference record" is a recording of a past meeting.

*   **`get_conference_record`**: Gets information about a specific conference record. You need to provide the name of the conference record, which looks something like `conferenceRecords/aaa-bbbb-ccc`.
*   **`list_conference_records`**: Lists all of your past conference records.

### Participants
A "participant" is a person who attended a meeting.

*   **`get_participant`**: Gets information about a specific person who attended a meeting.
*   **`list_participants`**: Lists all the people who attended a specific meeting.

### Participant Sessions
A "participant session" is the period of time a person was in a meeting. If a person leaves and rejoins, they will have multiple sessions.

*   **`get_participant_session`**: Gets information about a specific participant session.
*   **`list_participant_sessions`**: Lists all the sessions for a specific participant in a meeting.

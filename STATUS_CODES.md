# LiveAgent Status Codes Reference

This document describes all the status codes used in the LiveAgent API and how they are implemented in the MCP server.

## Ticket Status Codes

| Code | Meaning | MCP Input Value |
|------|---------|-----------------|
| I | Init | init |
| N | New | new |
| T | Chatting | chatting |
| P | Calling | calling |
| R | Resolved | resolved |
| X | Deleted | deleted |
| B | Spam | spam |
| A | Answered | answered |
| C | Open | open |
| W | Postponed | postponed |
| L | Closed | closed |

## Channel Type Codes

| Code | Meaning |
|------|---------|
| E | Email |
| B | Contact Button |
| M | Contact Form |
| I | Invitation |
| C | Call |
| W | Call Button |
| F | Facebook |
| A | Facebook Message |
| T | Twitter |
| Q | Forum |
| S | Suggestion |

## Agent Status Codes

| Code | Meaning |
|------|---------|
| R | Read |
| M | Message |
| T | Chat |
| P | Phone |

## Call Status Codes

| Code | Meaning |
|------|---------|
| O | Callee Offline |
| Q | Waiting in Queue |
| R | Ringing to an Agent |
| C | Calling with an Agent |
| F | Finished |

## Contact Gender Codes

| Code | Meaning | MCP Input Value |
|------|---------|-----------------|
| M | Male | male |
| F | Female | female |
| O | Other | other |
| X | Unspecified | unspecified |

## Boolean Fields (Y/N)

Many fields in LiveAgent use Y/N values:

| Code | Meaning |
|------|---------|
| Y | Yes |
| N | No |

Examples:
- `do_not_send_mail`: Y = Don't send email, N = Send email
- `use_template`: Y = Use email template, N = Don't use template
- `is_html_message`: Y = HTML format, N = Plain text format

## Usage in MCP Server

The MCP server automatically translates between human-readable values and API codes:

- When listing tickets, the server displays both the code and its meaning (e.g., "Status: Resolved")
- When creating or updating tickets, you can use the human-readable values (e.g., "status": "resolved")
- The server includes descriptions in tool schemas to help LLMs understand what values are accepted

For example, when creating a ticket:
```json
{
  "subject": "Test ticket",
  "message": "This is a test",
  "contact_email": "test@example.com",
  "status": "new"  // Will be converted to "N" internally
}
```
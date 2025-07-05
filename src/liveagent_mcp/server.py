import os
import asyncio
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

import liveagent_api
from liveagent_api.rest import ApiException
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    CallToolRequest,
    ErrorData,
)

load_dotenv()

server = Server("liveagent")

BASE_URL = os.getenv("LIVEAGENT_BASE_URL", "").rstrip("/")
API_KEY = os.getenv("LIVEAGENT_V3_API_KEY", "")
TIMEOUT = int(os.getenv("LIVEAGENT_TIMEOUT", "30"))

if not BASE_URL or not API_KEY:
    raise ValueError("LIVEAGENT_BASE_URL and LIVEAGENT_V3_API_KEY must be set")

configuration = liveagent_api.Configuration()
configuration.host = f"{BASE_URL}/api/v3"
configuration.api_key["apikey"] = API_KEY
configuration.request_timeout = TIMEOUT

api_client = liveagent_api.ApiClient(configuration)

tickets_api = liveagent_api.TicketsApi(api_client)
agents_api = liveagent_api.AgentsApi(api_client)
contacts_api = liveagent_api.ContactsApi(api_client)
departments_api = liveagent_api.DepartmentsApi(api_client)
messages_api = liveagent_api.MessagesApi(api_client)
companies_api = liveagent_api.CompaniesApi(api_client)
chats_api = liveagent_api.ChatsApi(api_client)
calls_api = liveagent_api.CallsApi(api_client)

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="list_tickets",
            description="List tickets with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status: new (N), open (C), answered (A), resolved (R), closed (L), spam (B), deleted (X), chatting (T), calling (P), postponed (W), init (I)",
                        "enum": ["new", "open", "answered", "resolved", "closed", "spam", "deleted", "chatting", "calling", "postponed", "init"]
                    },
                    "department_id": {
                        "type": "string",
                        "description": "Filter by department ID"
                    },
                    "agent_id": {
                        "type": "string",
                        "description": "Filter by agent ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 20)",
                        "default": 20
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (default: 0)",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_ticket",
            description="Get details of a specific ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID"
                    }
                },
                "required": ["ticket_id"]
            }
        ),
        Tool(
            name="create_ticket",
            description="Create a new ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Ticket subject"
                    },
                    "message": {
                        "type": "string",
                        "description": "Initial message content"
                    },
                    "contact_email": {
                        "type": "string",
                        "description": "Contact email address"
                    },
                    "department_id": {
                        "type": "string",
                        "description": "Department ID (optional)"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority level",
                        "enum": ["low", "medium", "high", "urgent"]
                    },
                    "status": {
                        "type": "string",
                        "description": "Initial status (default: new)",
                        "enum": ["new", "open", "answered"],
                        "default": "new"
                    }
                },
                "required": ["subject", "message", "contact_email"]
            }
        ),
        Tool(
            name="update_ticket",
            description="Update a ticket's properties",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status: new (N), open (C), answered (A), resolved (R), closed (L), spam (B), deleted (X), chatting (T), calling (P), postponed (W), init (I)",
                        "enum": ["new", "open", "answered", "resolved", "closed", "spam", "deleted", "chatting", "calling", "postponed", "init"]
                    },
                    "priority": {
                        "type": "string",
                        "description": "New priority",
                        "enum": ["low", "medium", "high", "urgent"]
                    },
                    "agent_id": {
                        "type": "string",
                        "description": "Assign to agent ID"
                    },
                    "department_id": {
                        "type": "string",
                        "description": "Move to department ID"
                    }
                },
                "required": ["ticket_id"]
            }
        ),
        Tool(
            name="add_ticket_message",
            description="Add a message to an existing ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message content"
                    },
                    "is_public": {
                        "type": "boolean",
                        "description": "Whether the message is public (default: true)",
                        "default": True
                    }
                },
                "required": ["ticket_id", "message"]
            }
        ),
        Tool(
            name="list_agents",
            description="List all agents",
            inputSchema={
                "type": "object",
                "properties": {
                    "online_only": {
                        "type": "boolean",
                        "description": "Only show online agents",
                        "default": False
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 20)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_agent",
            description="Get details of a specific agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "The agent ID"
                    }
                },
                "required": ["agent_id"]
            }
        ),
        Tool(
            name="list_contacts",
            description="List contacts with optional search",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search term for contacts"
                    },
                    "email": {
                        "type": "string",
                        "description": "Filter by email address"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 20)",
                        "default": 20
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (default: 0)",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_contact",
            description="Get details of a specific contact",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The contact ID"
                    }
                },
                "required": ["contact_id"]
            }
        ),
        Tool(
            name="create_contact",
            description="Create a new contact",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Contact email address"
                    },
                    "firstname": {
                        "type": "string",
                        "description": "First name"
                    },
                    "lastname": {
                        "type": "string",
                        "description": "Last name"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number"
                    },
                    "company_id": {
                        "type": "string",
                        "description": "Company ID (optional)"
                    },
                    "gender": {
                        "type": "string",
                        "description": "Gender: male (M), female (F), other (O), unspecified (X)",
                        "enum": ["male", "female", "other", "unspecified"]
                    },
                    "city": {
                        "type": "string",
                        "description": "City"
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code (e.g., 'en', 'es', 'fr')"
                    },
                    "note": {
                        "type": "string",
                        "description": "Note about the contact"
                    }
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="list_departments",
            description="List all departments",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 20)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="search_tickets",
            description="Search tickets by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 20)",
                        "default": 20
                    }
                },
                "required": ["query"]
            }
        )
    ]

def handle_api_error(e: ApiException) -> list:
    error_message = f"LiveAgent API Error: {e.status} - {e.reason}"
    if e.body:
        error_message += f"\nDetails: {e.body}"
    
    return [TextContent(type="text", text=error_message)]

def format_ticket(ticket: Any) -> str:
    status_map = {
        'I': 'Init', 'N': 'New', 'T': 'Chatting', 'P': 'Calling', 
        'R': 'Resolved', 'X': 'Deleted', 'B': 'Spam', 'A': 'Answered', 
        'C': 'Open', 'W': 'Postponed', 'L': 'Closed'
    }
    channel_map = {
        'E': 'Email', 'B': 'Contact Button', 'M': 'Contact Form', 
        'I': 'Invitation', 'C': 'Call', 'W': 'Call Button', 
        'F': 'Facebook', 'A': 'Facebook Message', 'T': 'Twitter', 
        'Q': 'Forum', 'S': 'Suggestion'
    }
    return f"""Ticket ID: {ticket.id}
Code: {ticket.code}
Subject: {ticket.subject}
Status: {status_map.get(ticket.status, ticket.status)}
Channel: {channel_map.get(ticket.channel_type, ticket.channel_type)}
Department: {ticket.departmentid}
Agent: {ticket.agentid or 'Unassigned'}
Customer: {ticket.owner_name} ({ticket.owner_email})
Created: {ticket.date_created}
Last Updated: {getattr(ticket, 'date_changed', 'N/A')}"""

def format_agent(agent: Any) -> str:
    return f"""Agent ID: {agent.id}
Name: {agent.firstname} {agent.lastname}
Email: {agent.email}
Status: {'Online' if getattr(agent, 'is_online', False) else 'Offline'}
Role: {getattr(agent, 'role', 'Agent')}"""

def format_contact(contact: Any) -> str:
    return f"""Contact ID: {contact.id}
Name: {getattr(contact, 'firstname', '')} {getattr(contact, 'lastname', '')}
Email: {contact.email}
Phone: {getattr(contact, 'phone', 'N/A')}
Company: {getattr(contact, 'company_name', 'N/A')}"""

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list:
    try:
        tool_name = name
        params = arguments or {}
        
        if tool_name == "list_tickets":
            # Build filters for the API
            filters = {}
            if params.get("status"):
                status_map = {
                    'init': 'I', 'new': 'N', 'chatting': 'T', 'calling': 'P',
                    'resolved': 'R', 'deleted': 'X', 'spam': 'B', 'answered': 'A',
                    'open': 'C', 'postponed': 'W', 'closed': 'L'
                }
                filters["status"] = status_map.get(params["status"].lower(), 'N')
            if params.get("department_id"):
                filters["departmentid"] = params["department_id"]
            if params.get("agent_id"):
                filters["agentid"] = params["agent_id"]
            
            kwargs = {
                "per_page": params.get("limit", 20),
                "_from": params.get("offset", 0)
            }
            if filters:
                kwargs["filters"] = json.dumps(filters)
            
            tickets = await asyncio.to_thread(
                tickets_api.get_tickets_list,
                **kwargs
            )
            
            if not tickets:
                return [TextContent(type="text", text="No tickets found.")]
            
            result = f"Found {len(tickets)} tickets:\n\n"
            for ticket in tickets:
                result += format_ticket(ticket) + "\n" + "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif tool_name == "get_ticket":
            ticket = await asyncio.to_thread(
                tickets_api.get_ticket,
                ticket_id=params["ticket_id"]
            )
            
            result = format_ticket(ticket)
            
            if hasattr(ticket, 'messages') and ticket.messages:
                result += f"\n\nMessages ({len(ticket.messages)}):\n"
                for msg in ticket.messages[-5:]:
                    result += f"\n[{msg.date_created}] {msg.from_name}: {msg.message[:200]}..."
            
            return [TextContent(type="text", text=result)]
        
        elif tool_name == "create_ticket":
            # Create a ticket object with the required fields
            # Note: useridentifier is required but we'll use the email as identifier
            ticket_data = liveagent_api.TicketListItem(
                useridentifier=params["contact_email"],
                subject=params["subject"],
                message=params["message"],
                recipient=params["contact_email"],
                departmentid=params.get("department_id", "default")
            )
            
            # Set status with proper code
            if params.get("status"):
                status_map = {
                    'init': 'I', 'new': 'N', 'chatting': 'T', 'calling': 'P',
                    'resolved': 'R', 'deleted': 'X', 'spam': 'B', 'answered': 'A',
                    'open': 'C', 'postponed': 'W', 'closed': 'L'
                }
                ticket_data.status = status_map.get(params["status"].lower(), 'N')
            else:
                ticket_data.status = "N"  # Default to new
            
            # Set optional fields with their meanings:
            # do_not_send_mail: Y=yes (don't send), N=no (send email)
            ticket_data.do_not_send_mail = "N"
            # use_template: Y=yes (use email template), N=no
            ticket_data.use_template = "Y"
            # is_html_message: Y=yes (HTML format), N=no (plain text)
            ticket_data.is_html_message = "N"
            
            if "priority" in params:
                ticket_data.priority = params["priority"]
            
            ticket = await asyncio.to_thread(
                tickets_api.create_ticket,
                ticket=ticket_data
            )
            
            return [TextContent(type="text", text=f"Ticket created successfully!\n\n{format_ticket(ticket)}")]
        
        elif tool_name == "update_ticket":
            # Create update object
            update_data = liveagent_api.TicketUpdatable()
            
            if "status" in params:
                status_map = {
                    'init': 'I', 'new': 'N', 'chatting': 'T', 'calling': 'P',
                    'resolved': 'R', 'deleted': 'X', 'spam': 'B', 'answered': 'A',
                    'open': 'C', 'postponed': 'W', 'closed': 'L'
                }
                update_data.status = status_map.get(params["status"].lower(), 'N')
            if "priority" in params:
                update_data.priority = params["priority"]
            if "agent_id" in params:
                update_data.agentid = params["agent_id"]
            if "department_id" in params:
                update_data.departmentid = params["department_id"]
            
            ticket = await asyncio.to_thread(
                tickets_api.update_ticket,
                ticket_id=params["ticket_id"],
                ticket=update_data
            )
            
            return [TextContent(type="text", text=f"Ticket updated successfully!\n\n{format_ticket(ticket)}")]
        
        elif tool_name == "add_ticket_message":
            # Note: The LiveAgent Python SDK doesn't have a direct method to add messages to tickets
            # This would require using the raw API or updating the ticket with a new message
            return [TextContent(type="text", text="Adding messages to existing tickets is not supported by the LiveAgent Python SDK. Please create a new ticket or use the LiveAgent web interface.")]
        
        elif tool_name == "list_agents":
            agents = await asyncio.to_thread(
                agents_api.get_agents,
                per_page=params.get("limit", 20)
            )
            
            if params.get("online_only"):
                agents = [a for a in agents if getattr(a, 'is_online', False)]
            
            if not agents:
                return [TextContent(type="text", text="No agents found.")]
            
            result = f"Found {len(agents)} agents:\n\n"
            for agent in agents:
                result += format_agent(agent) + "\n" + "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif tool_name == "get_agent":
            agent = await asyncio.to_thread(
                agents_api.get_agent,
                agent_id=params["agent_id"]
            )
            
            return [TextContent(type="text", text=format_agent(agent))]
        
        elif tool_name == "list_contacts":
            # Build filters for contacts
            kwargs = {
                "per_page": params.get("limit", 20),
                "page": (params.get("offset", 0) // params.get("limit", 20)) + 1
            }
            
            # For contacts, we might need to use advanced filter format
            filters = []
            if params.get("search"):
                # Search in name fields
                filters.append(["firstname", "LIKE", f"%{params['search']}%"])
            if params.get("email"):
                # Search by exact email
                filters.append(["emails", "=", params["email"]])
                
            if filters:
                kwargs["filters"] = json.dumps(filters)
            
            contacts = await asyncio.to_thread(
                contacts_api.get_contacts_list,
                **kwargs
            )
            
            if not contacts:
                return [TextContent(type="text", text="No contacts found.")]
            
            result = f"Found {len(contacts)} contacts:\n\n"
            for contact in contacts:
                result += format_contact(contact) + "\n" + "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif tool_name == "get_contact":
            contact = await asyncio.to_thread(
                contacts_api.get_specific_contact,
                contact_id=params["contact_id"]
            )
            
            return [TextContent(type="text", text=format_contact(contact))]
        
        elif tool_name == "create_contact":
            # Create contact object - note that email should be in a list
            contact_data = liveagent_api.ContactRequest()
            
            # Email should be provided as a list
            contact_data.emails = [params["email"]]
            
            if "firstname" in params:
                contact_data.firstname = params["firstname"]
            if "lastname" in params:
                contact_data.lastname = params["lastname"]
            if "phone" in params:
                # Phone should be provided as a list
                contact_data.phones = [params["phone"]]
            if "company_id" in params:
                contact_data.company_id = params["company_id"]
            if "gender" in params:
                # Map gender to proper code
                gender_map = {
                    'male': 'M', 'female': 'F', 'other': 'O', 'unspecified': 'X'
                }
                contact_data.gender = gender_map.get(params["gender"].lower(), 'X')
            if "city" in params:
                contact_data.city = params["city"]
            if "language" in params:
                contact_data.language = params["language"]
            if "note" in params:
                contact_data.note = params["note"]
            
            contact = await asyncio.to_thread(
                contacts_api.create_contact,
                contact=contact_data
            )
            
            return [TextContent(type="text", text=f"Contact created successfully!\n\n{format_contact(contact)}")]
        
        elif tool_name == "list_departments":
            # Get all departments, the API doesn't support limit parameter
            departments = await asyncio.to_thread(
                departments_api.get_department_list
            )
            
            # Apply client-side limit
            limit = params.get("limit", 20)
            departments = departments[:limit] if departments else []
            
            if not departments:
                return [TextContent(type="text", text="No departments found.")]
            
            result = f"Found {len(departments)} departments:\n\n"
            for dept in departments:
                dept_info = f"ID: {getattr(dept, 'id', 'N/A')}\n"
                dept_info += f"Name: {getattr(dept, 'name', 'N/A')}\n"
                dept_info += f"Description: {getattr(dept, 'description', 'N/A')}\n"
                result += dept_info + "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif tool_name == "search_tickets":
            # Use list tickets with filters to search - use LIKE operator for partial match
            filters = [["subject", "LIKE", f"%{params['query']}%"]]
            tickets = await asyncio.to_thread(
                tickets_api.get_tickets_list,
                filters=json.dumps(filters),
                per_page=params.get("limit", 20),
                page=1
            )
            
            if not tickets:
                return [TextContent(type="text", text="No tickets found matching your search.")]
            
            result = f"Found {len(tickets)} tickets matching '{params['query']}':\n\n"
            for ticket in tickets:
                result += format_ticket(ticket) + "\n" + "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {tool_name}")]
    
    except ApiException as e:
        return handle_api_error(e)
    except Exception as e:
        import traceback
        import sys
        error_message = f"Unexpected error: {str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        print(f"Error in handle_call_tool: {error_message}", file=sys.stderr)
        return [TextContent(type="text", text=error_message)]

async def serve() -> None:
    import sys
    from mcp.server.stdio import stdio_server
    
    print(f"LiveAgent MCP Server starting...", file=sys.stderr)
    print(f"Base URL: {BASE_URL}", file=sys.stderr)
    print(f"API Key configured: {'Yes' if API_KEY else 'No'}", file=sys.stderr)
    
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

def main():
    asyncio.run(serve())

if __name__ == "__main__":
    main()
# LiveAgent MCP Server

An MCP (Model Context Protocol) server that provides access to LiveAgent API functionality, enabling AI assistants to interact with your LiveAgent helpdesk system.

## Features

- **Ticket Management**: List, create, update, and search tickets
- **Agent Management**: List agents and get agent details  
- **Contact Management**: List, create, and manage customer contacts
- **Department Support**: List departments for ticket routing
- **Message Handling**: Add messages to existing tickets
- **Full Search**: Search tickets by query

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/liveagent-mcp-server.git
cd liveagent-mcp-server

# Install dependencies
pip install -e .
```

## Configuration

Set the following environment variables:

```bash
# Required
LIVEAGENT_BASE_URL=https://your-instance.liveagent.com
LIVEAGENT_V3_API_KEY=your_api_key_here

# Optional
LIVEAGENT_TIMEOUT=30  # Request timeout in seconds (default: 30)
```

You can create a `.env` file in the project root with these variables.

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "liveagent": {
      "command": "python",
      "args": ["-m", "liveagent_mcp.server"],
      "env": {
        "LIVEAGENT_BASE_URL": "https://your-instance.liveagent.com",
        "LIVEAGENT_V3_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Available Tools

#### Ticket Management
- `list_tickets` - List tickets with filters (status, department, agent)
- `get_ticket` - Get detailed information about a specific ticket
- `create_ticket` - Create a new ticket
- `update_ticket` - Update ticket properties (status, priority, assignment)
- `add_ticket_message` - Add a message to an existing ticket
- `search_tickets` - Search tickets by query

#### Agent Management
- `list_agents` - List all agents (with online filter option)
- `get_agent` - Get details of a specific agent

#### Contact Management
- `list_contacts` - List contacts with search capability
- `get_contact` - Get details of a specific contact
- `create_contact` - Create a new contact

#### Other
- `list_departments` - List all departments

## Examples

### List open tickets
```
Use the list_tickets tool with status "open"
```

### Create a new ticket
```
Use the create_ticket tool with:
- subject: "Need help with order"
- message: "Customer inquiry about order status"
- contact_email: "customer@example.com"
- priority: "high"
```

### Search for tickets
```
Use the search_tickets tool with query "refund"
```

## Development

To contribute or modify:

1. Install development dependencies
2. Make your changes
3. Test with a LiveAgent instance
4. Submit a pull request

## License

MIT License - see LICENSE file for details
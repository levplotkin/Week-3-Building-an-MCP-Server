# Hands-on Lab: Building "Coroot" MCP Server 

**Reference:** Based on [mcp-coroot](https://github.com/jamesbrink/mcp-coroot) architecture

```json
{
  "mcpServers": {
    "calculator": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/lev.plotkin-ext@gong.io/dev/Week-3-Building-an-MCP-Server",
        "run",
        "coroot_mcp_server.py"
      ],
      "env": {
        "COROOT_BASE_URL": "http://localhost:8080",
        "COROOT_USERNAME": "admin",
        "COROOT_PASSWORD": "your-password"
      }
    }
  }
}
```

### For SSO/MFA Users

If your organization uses SSO or MFA, use session cookie authentication:

```json
{
  "mcpServers": {
    "coroot": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/lev.plotkin-ext@gong.io/dev/Week-3-Building-an-MCP-Server",
        "run",
        "coroot_mcp_server.py"
      ],
      "env": {
        "COROOT_BASE_URL": "http://localhost:8080",
        "COROOT_SESSION_COOKIE": "your-auth-cookie-value"
      }
    }
  }
}
```


To get your session cookie:
1. Login to Coroot through your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Copy the value of the `auth` cookie

## Authentication Methods

The server supports three authentication methods:

1. **Username/Password** (Recommended) - Automatic login and session management
2. **Session Cookie** - Required for SSO/MFA environments
3. **API Key** - Limited to data ingestion endpoints only

**Reference Implementation:**
- Study [mcp-coroot](https://github.com/jamesbrink/mcp-coroot) for production patterns
- 61 tools, proper error handling, authentication
- Great learning resource for advanced features

**The MCP Coroot server provides 61 tools for interacting with Coroot observability platform:**
- Authentication and user management (5 tools)
- Project creation and management (9 tools)
- Application monitoring and troubleshooting (3 tools)
- Infrastructure overview and incidents (2 tools)
- Deployment and system overviews (5 tools)
- Dashboard management (5 tools)
- Integration configuration (4 tools)
- Configuration management (9 tools)
- Advanced troubleshooting (3 tools)
- Custom cloud pricing (3 tools)
- Database instrumentation (2 tools)
- System configuration (4 tools)
- Risk overview (1 tool)
- Health checks (1 tool)
- Panel data and advanced configuration (6 tools)


## Available Commands

Once configured, you can ask Claude to:

### Monitoring & Analysis
- "Show me all Coroot projects"
- "Check the health of all applications in production"
- "Show me error logs for the API service in the last hour"
- "Find slow traces in the payment service"
- "Analyze why the frontend has high latency"
- "Show CPU profiling data for the backend service"

### Infrastructure Management
- "List all nodes in the production project"
- "Show me the resource usage of server01"
- "Check for any incidents in the last 24 hours"
- "Display the deployment history"
- "Show me the risk assessment for our infrastructure"

### Configuration & Integration
- "Set up Slack notifications for critical alerts"
- "Configure Prometheus integration"
- "Update SLO thresholds for the API service"
- "Show me the application categorization rules"
- "Create a new application category for microservices"
- "Update the database category to include new patterns"
- "Delete the test category we no longer need"
- "Create a custom dashboard for Redis monitoring"

### Advanced Features
- "Perform root cause analysis on the payment service failures"
- "Show database instrumentation settings for PostgreSQL"
- "Configure custom cloud pricing for our AWS instances"
- "Update the AI configuration for RCA"
- "List all API keys for the production project"


## Troubleshooting

### Connection Issues
- Verify COROOT_BASE_URL is correct and accessible
- Check if Coroot is running: `curl http://localhost:8080/health`
- Ensure no firewall is blocking the connection

### Authentication Errors
- For basic auth: Verify username and password are correct
- For SSO/MFA: Ensure session cookie is valid and not expired
- Session cookies expire after 7 days of inactivity

### Tool Errors
- "Tool not found": Restart Claude Desktop after configuration changes
- Large responses: Use time filters to reduce data size
- Empty responses: Normal for some operations (deletes, updates)
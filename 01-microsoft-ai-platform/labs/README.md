# Microsoft AI Platform Labs

This folder contains four hands-on labs that guide you from creating a prompt-based agent in Microsoft Foundry to integrating external tools, calling the agent from code, and publishing it to Agent 365.

1. **[Lab 1 - Create a prompt-based agent in Foundry](./lab-01x01-create-a-prompt-agent.md)**: Create and configure a prompt-based agent in Microsoft Foundry, add a built-in tool, test it in the playground, and inspect its definition.

2. **[Lab 2 - Add an MCP tool to your agent](./lab-01x02-add-an-mcp-tool.md)**: Build and expose a Python MCP server, connect it to your Foundry agent, and control external tool calls through an approval policy.

3. **[Lab 3 - Call your agent via the Responses API](./lab-01x03-call-via-responses-api.md)**: Invoke the agent from Python with Microsoft Entra ID authentication, stream its responses, and continue a stateful conversation.

4. **[Lab 4 - Publish to Agent 365 without OBO](./lab-01x04-publish-to-agent365-no-obo.md)**: Publish and govern the agent through Agent 365, understand its Entra Agent ID, and invoke it with app-only authentication instead of an on-behalf-of flow.

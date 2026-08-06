import express from "express";

const app = express();
app.use(express.json());

const manifest = {
  name: "demo-echo-server",
  version: "1.0.0",
  tools: [
    {
      name: "echo",
      description: "Returns the same text provided as input",
      inputSchema: {
        type: "object",
        properties: { text: { type: "string" } },
        required: ["text"]
      },
      outputSchema: {
        type: "object",
        properties: { text: { type: "string" } }
      }
    }
  ]
};

app.post("/", (req, res) => {
  const body = req.body;

  if (body.method === "manifest/get") {
    return res.json({ jsonrpc: "2.0", id: body.id, result: manifest });
  }

  if (body.method === "tools/list") {
    return res.json({ jsonrpc: "2.0", id: body.id, result: manifest.tools });
  }

  if (body.method === "tools/call") {
    const toolName = body.params?.name;
    const args = body.params?.arguments || {};

    if (toolName === "echo") {
      return res.json({
        jsonrpc: "2.0",
        id: body.id,
        result: { text: args.text || "" }
      });
    }

    return res.json({
      jsonrpc: "2.0",
      id: body.id,
      error: { code: -32601, message: "Unknown tool" }
    });
  }

  return res.json({
    jsonrpc: "2.0",
    id: body.id,
    error: { code: -32601, message: "Unknown MCP method" }
  });
});

app.listen(3000, () => {
  console.log("MCP server running on http://localhost:3000/");
});

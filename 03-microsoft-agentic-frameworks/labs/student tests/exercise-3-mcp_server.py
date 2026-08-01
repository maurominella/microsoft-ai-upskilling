from fastmcp import FastMCP
from rai_campaigns import CAMPAIGNS, get_campaign, list_campaigns, roi
import logging
logger = logging.getLogger(__name__)

mcp = FastMCP("RAI Campaigns MCP")

# --- TOOLS: actions an agent can call ---
@mcp.tool
def get_campaign_details(campaign_id: str) -> dict:
    """Full details of a campaign by its id (e.g. 'CMP-004')."""
    logger.info("Campaign details requested for %s", campaign_id)
    c = get_campaign(campaign_id)
    return c or {"error": f"campaign {campaign_id} not found"}

@mcp.tool
def all_campaigns() -> list:
    """Short list (id, client, sector) of all campaigns."""
    logger.info("All campaigns requested")
    return list_campaigns()

@mcp.tool
def top_campaigns_by_roi(n: int = 3) -> list:
    """Top n campaigns by descending ROI, with the ROI% value."""
    logger.info("Top ROI requested, n=%s", n)
    data = [{"id": c["id"], "client": c["client"], "roi_pct": roi(c["id"])}
            for c in CAMPAIGNS]
    data.sort(key=lambda x: x["roi_pct"], reverse=True)
    return data[:n]

# --- RESOURCE: readable data to ground the answers on ---
@mcp.resource("campaigns://all")
def campaigns_resource() -> list:
    """All campaigns as raw data (context for the agent)."""
    logger.info("All campaigns resource requested")
    return CAMPAIGNS

@mcp.tool
def compare_campaigns(id_a: str, id_b: str) -> dict:
    """Compare the ROI of two campaigns and say which performs better."""
    logger.info("Compare campaigns requested for %s and %s", id_a, id_b)
    ra, rb = roi(id_a), roi(id_b)
    better = id_a if (ra or -1e9) >= (rb or -1e9) else id_b
    return {"roi": {id_a: ra, id_b: rb}, "better": better}

# --- PROMPT: reusable template ---
@mcp.prompt
def evaluate_campaign(campaign_id: str) -> str:
    """Template to evaluate a campaign in a standard way."""
    logger.info("Evaluate campaign prompt requested for %s", campaign_id)
    return (
        f"Evaluate campaign {campaign_id}: fetch the data with the tools, "
        f"compute the ROI, compare it with the others and propose an action."
    )


if __name__ == "__main__":
    # HTTP transport: the server listens on http://127.0.0.1:8000/mcp
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="http", host="127.0.0.1", port=8000)
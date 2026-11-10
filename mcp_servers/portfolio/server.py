from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp_servers.portfolio.tools import search_evidence, get_case_study, list_skills
from mcp_servers.portfolio.resources import get_case_resource, get_proposal_resource
from mcp_servers.portfolio.prompts import answer_screening_prompt

# Initialize FastMCP Server
mcp = FastMCP("gigbid-portfolio-server")

@mcp.tool(
    name="search_evidence",
    description="Search verified portfolio case studies, repositories, and past proposals by requirement or skill. Returns items with type, source, date, and outcome."
)
def search_evidence_tool(requirement: str, k: int = 5, persona_id: str = "ai_engineer") -> list[dict[str, Any]]:
    return search_evidence(requirement=requirement, k=k, persona_id=persona_id)

@mcp.tool(
    name="get_case_study",
    description="Retrieve the complete text and outcome breakdown of a verified case study by evidence ID."
)
def get_case_study_tool(case_id: str, persona_id: str = "ai_engineer") -> dict[str, Any]:
    return get_case_study(case_id=case_id, persona_id=persona_id)

@mcp.tool(
    name="list_skills",
    description="List all verified skills and technical competencies backed by evidence in the freelancer profile."
)
def list_skills_tool(persona_id: str = "ai_engineer") -> list[str]:
    return list_skills(persona_id=persona_id)

@mcp.resource("portfolio://case/{case_id}")
def case_resource(case_id: str) -> str:
    """Load full case study item as an MCP resource."""
    return get_case_resource(case_id)

@mcp.resource("portfolio://proposal/{proposal_id}")
def proposal_resource(proposal_id: str) -> str:
    """Load past proposal details as an MCP resource."""
    return get_proposal_resource(proposal_id)

@mcp.prompt(name="answer_screening_question")
def screening_question_prompt(question: str, requirement: str = "") -> str:
    """Prompt template for answering screening questions using evidence citations."""
    return answer_screening_prompt(question, requirement)

if __name__ == "__main__":
    mcp.run()

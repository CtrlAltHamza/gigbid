# GigBid Portfolio MCP Server

A standalone, read-only Model Context Protocol (MCP) server that provides AI agents, Claude Desktop, and Cursor with verified portfolio evidence, case studies, and skills.

## Capabilities
- **Tools**:
  - `search_evidence(requirement, k, persona_id)`: Multi-modal search across case studies, code repositories, and past proposals.
  - `get_case_study(case_id, persona_id)`: Full case study text with problem, solution, and measured outcomes.
  - `list_skills(persona_id)`: Verified skills extracted from portfolio artifacts.
- **Resource Templates**:
  - `portfolio://case/{case_id}`: Full case study text.
  - `portfolio://proposal/{proposal_id}`: Full past proposal text and outcome status.
- **Prompt Templates**:
  - `answer_screening_question`: Grounds client screening answers in real portfolio evidence citations.

## Installation & Running

### Using `uvx`
```bash
uvx gigbid-portfolio-mcp
```

### Running Locally
```bash
python -m mcp_servers.portfolio.server
```

### Configuration in Claude Desktop / Cursor
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "gigbid-portfolio": {
      "command": "python",
      "args": ["-m", "mcp_servers.portfolio.server"],
      "cwd": "/path/to/gigbid"
    }
  }
}
```

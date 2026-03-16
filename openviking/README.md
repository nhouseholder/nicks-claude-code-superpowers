# OpenViking Integration

[OpenViking](https://github.com/volcengine/OpenViking) is an open-source context database for AI agents. It provides unified management of memories, resources, and skills using a filesystem paradigm with tiered context loading (L0/L1/L2).

## What's Included

### Skills (4)
| Skill | Description |
|-------|-------------|
| `ov-add-data` | Add resources, memories, and skills to OpenViking |
| `ov-search-context` | Search memories, skills, and resources from OpenViking |
| `ov-server-operate` | Install, configure, start/stop the OpenViking server |
| `memory-recall` | Recall long-term memories from OpenViking sessions |

### Hooks (Claude Memory Plugin)
| Hook | Trigger | Function |
|------|---------|----------|
| session-start.sh | SessionStart | Initialize OpenViking memory session |
| user-prompt-submit.sh | UserPromptSubmit | Hint that memory is available |
| stop.sh | Stop | Ingest conversation turn into session |
| session-end.sh | SessionEnd | Commit session and extract memories |

### MCP Server
- `server.py` — Exposes OpenViking RAG capabilities as MCP tools (query, search, add_resource)
- Connect via: `claude mcp add --transport http openviking http://localhost:2033/mcp`

## Quick Setup

### 1. Install OpenViking
```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install
mkdir -p ~/.openviking
cd ~/.openviking
uv venv --python 3.12 ov-venv
uv pip install --python ~/.openviking/ov-venv/bin/python3 openviking --force-reinstall
```

### 2. Configure
```bash
# Copy example configs
cp openviking/config/ov.conf.example ~/.openviking/ov.conf
cp openviking/config/ovcli.conf.example ~/.openviking/ovcli.conf

# Edit with your API keys (supports OpenAI, Ollama, or Volcengine)
```

### 3. Start Server
```bash
source ~/.openviking/ov-venv/bin/activate
mkdir -p ~/.openviking/log
nohup openviking-server > ~/.openviking/log/openviking-server.log 2>&1 &
curl http://localhost:1933/health
```

### 4. Add MCP Server to Claude
```bash
claude mcp add --transport http openviking http://localhost:2033/mcp
```

## Configuration Examples

### Using OpenAI embeddings
Edit `~/.openviking/ov.conf`:
```json
{
  "embedding": {
    "dense": {
      "provider": "openai",
      "model": "text-embedding-3-small",
      "api_key": "sk-...",
      "api_base": "https://api.openai.com/v1",
      "dimension": 1536
    }
  },
  "vlm": {
    "provider": "litellm",
    "model": "anthropic/claude-sonnet-4-20250514",
    "api_key": "sk-ant-...",
    "temperature": 0.0
  }
}
```

### Using Ollama (free, local)
```json
{
  "embedding": {
    "dense": {
      "provider": "ollama",
      "model": "nomic-embed-text",
      "api_base": "http://localhost:11434/v1",
      "dimension": 768,
      "input": "text"
    }
  },
  "vlm": {
    "provider": "litellm",
    "model": "ollama/llama3.1",
    "api_base": "http://localhost:11434",
    "temperature": 0.0
  }
}
```

# Autonomous AI Agent System with Tool Use & MCP Integration

A production-grade, autonomous AI agent built entirely from scratch in Python. Inspired by tools like Claude Code and Aider, this agent operates as an intelligent CLI assistant capable of reasoning, planning, and executing complex multi-step tasks using a rich set of built-in tools and external MCP servers.

---

## ✨ Features

- **Agentic Loop** — The agent reasons and acts iteratively across multiple turns until the task is complete
- **Streaming Responses** — Real-time token-by-token output from the LLM
- **Tool Use & Orchestration** — Executes filesystem, shell, web, and memory tools autonomously
- **MCP Integration** — Connects to external Model Context Protocol (MCP) servers for extensible tooling
- **Context Compression** — Automatically summarizes long conversations to stay within token limits
- **Loop Detection** — Detects and breaks out of repetitive action cycles
- **Approval Policies** — Configurable safety gates before executing mutating tools
- **Session Persistence** — Save, resume, and checkpoint entire conversation sessions
- **Hooks System** — Pre/post lifecycle hooks for agent and tool events
- **Rich Terminal UI** — Beautiful CLI output with streaming diffs, tool call display, and syntax highlighting

---

## 🏗️ Architecture

```
AI_AGENT_From_Scratch/
├── main.py                  # CLI entry point (click-based)
├── agent/
│   ├── agent.py             # Core agentic loop
│   ├── session.py           # Session state & component initialization
│   ├── events.py            # Streaming event types
│   └── persistance.py       # Save/load/checkpoint sessions
├── tools/
│   ├── base.py              # Abstract Tool base class
│   ├── registry.py          # Tool registry & invocation
│   ├── discovery.py         # Dynamic tool discovery
│   ├── subagents.py         # Sub-agent orchestration
│   ├── builtin/             # Built-in tools
│   │   ├── read_file.py
│   │   ├── write_file.py
│   │   ├── edit_file.py
│   │   ├── shell.py
│   │   ├── grep.py
│   │   ├── glob.py
│   │   ├── list_dir.py
│   │   ├── web_search.py
│   │   ├── web_fetch.py
│   │   ├── memory.py
│   │   └── todos.py
│   └── mcp/                 # MCP server integration
├── context/
│   ├── manager.py           # Token-aware message history
│   ├── compaction.py        # Context summarization
│   └── loop_detector.py     # Repetition detection
├── client/
│   ├── llm_client.py        # OpenAI-compatible LLM client
│   └── response.py          # Streaming response parser
├── config/
│   ├── config.py            # Pydantic config models
│   └── loader.py            # .env + TOML config loader
├── safety/
│   └── approval.py          # Approval policy enforcement
├── hooks/
│   └── hook_system.py       # Lifecycle hook execution
├── prompts/
│   └── system.py            # System prompt construction
├── ui/
│   └── tui.py               # Rich terminal UI
└── utils/
    └── text.py              # Token counting utilities
```

---

## 🛠️ Built-in Tools

| Tool | Kind | Description |
|---|---|---|
| `read_file` | Read | Read file contents |
| `write_file` | Write | Create or overwrite files |
| `edit_file` | Write | Make targeted edits with unified diffs |
| `shell` | Shell | Execute shell commands |
| `grep` | Read | Search file contents with regex |
| `glob` | Read | Find files by pattern |
| `list_dir` | Read | List directory contents |
| `web_search` | Network | Search the web via DuckDuckGo |
| `web_fetch` | Network | Fetch and parse web pages |
| `memory` | Memory | Persist user preferences and notes |
| `todos` | Memory | Track task progress across sessions |

---

## ⚙️ Configuration

Configuration is loaded from a `.env` file and an optional `agent.toml`.

### `.env`
```env
API_KEY=your_api_key_here
BASE_URL=https://openrouter.ai/api/v1   # or any OpenAI-compatible endpoint
```

### `agent.toml` (optional)
```toml
[model]
name = "arcee-ai/trinity-large-preview:free"
temperature = 1.0
context_window = 256000

[agent]
max_turns = 100
approval = "on_request"   # on_request | auto | yolo | never

[[mcp_servers.filesystem]]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
```

### Approval Policies

| Policy | Behavior |
|---|---|
| `on_request` | Ask before any mutating tool |
| `auto` | Approve automatically |
| `auto-edit` | Auto-approve edits only |
| `on_failure` | Ask only after a failure |
| `never` | Never approve (read-only mode) |
| `yolo` | Approve everything, no prompts |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- `uv` package manager

### Installation

```bash
# Clone the repo
git clone https://github.com/Pandharimaske/agent-forge.git
cd agent-forge

# Install dependencies
uv sync

# Set up environment
cp .env.example .env
# Edit .env with your API key and base URL
```

### Run

```bash
# Interactive mode
uv run main.py

# Single prompt mode
uv run main.py "Summarize all Python files in this directory"

# Set working directory
uv run main.py --cwd /path/to/project "Refactor the main module"
```

---

## 💬 Slash Commands

Once in interactive mode, the following commands are available:

| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/config` | Show current configuration |
| `/model <n>` | Switch LLM model |
| `/approval <policy>` | Change approval policy |
| `/tools` | List available tools |
| `/mcp` | Show connected MCP servers |
| `/stats` | Show session statistics (turns, tokens) |
| `/clear` | Clear conversation history |
| `/save` | Save current session |
| `/sessions` | List saved sessions |
| `/resume <id>` | Resume a saved session |
| `/checkpoint` | Create a session checkpoint |
| `/restore <id>` | Restore from checkpoint |
| `/exit` | Quit the agent |

---

## 🔌 MCP Server Integration

The agent supports connecting to any MCP-compatible tool server via stdio or HTTP/SSE transport.

```toml
# stdio transport
[[mcp_servers.my_tool]]
command = "python"
args = ["my_mcp_server.py"]

# HTTP/SSE transport
[[mcp_servers.remote_tool]]
url = "http://localhost:8000/sse"
```

Connected MCP tools are automatically registered in the tool registry and exposed to the agent alongside built-in tools.

---

## 🔁 How the Agentic Loop Works

```
User Message
     │
     ▼
┌─────────────────────────────────────┐
│           Agentic Loop              │
│                                     │
│  1. Check context size              │
│     → Compress if > 80% full        │
│                                     │
│  2. Stream LLM response             │
│     → Collect text + tool calls     │
│                                     │
│  3. If no tool calls → DONE         │
│                                     │
│  4. Execute tool calls              │
│     → Check approval policy         │
│     → Run tool                      │
│     → Feed results back             │
│                                     │
│  5. Check for loops                 │
│     → Inject loop-breaker prompt    │
│                                     │
│  6. Repeat up to max_turns          │
└─────────────────────────────────────┘
     │
     ▼
 Final Response
```

---

## 🧰 Tech Stack

| Library | Purpose |
|---|---|
| `openai` | OpenAI-compatible LLM client |
| `fastmcp` | MCP server integration |
| `rich` | Terminal UI & formatting |
| `click` | CLI argument parsing |
| `pydantic` | Config validation & schemas |
| `tiktoken` | Token counting |
| `httpx` | Async HTTP client |
| `ddgs` | DuckDuckGo web search |
| `tomli` | TOML config parsing |

---

## 🙋‍♂️ Author

**Pandhari Maske**  
[GitHub](https://github.com/Pandharimaske) · [LinkedIn](https://linkedin.com/in/pandharimaske)

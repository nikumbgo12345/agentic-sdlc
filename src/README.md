# agentic-sdlc

A practical guide to implementing deterministic software development workflows using agentic patterns with LangGraph and local LLMs.

## What This Repo Is

This repository demonstrates how to build deterministic, repeatable software development workflows using agentic patterns. It leverages LangGraph for workflow orchestration and local LLMs (Ollama) to implement a complete Software Development Life Cycle (SDLC) that can be run entirely offline.

The focus is on practical implementation rather than theoretical concepts, providing concrete examples of how to structure agent interactions, manage state, and ensure predictable outcomes in software development processes.

## Why Deterministic Workflows Matter

In software development, deterministic workflows provide:

- **Predictable outcomes**: Same inputs produce same outputs
- **Reproducible builds**: Consistent results across environments
- **Easier debugging**: Clear execution paths and error localization
- **Auditability**: Complete traceability of decisions and changes
- **Offline capability**: No dependency on external APIs or cloud services

These properties are crucial for production environments where reliability and security are paramount.

## Quickstart

```bash
# Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull required Ollama model
ollama pull qwen3-coder:30b
```

## Folder Structure

```
agentic-sdlc/
├── README.md
├── requirements.txt
├── src/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── implementer.py
│   │   ├── validator.py
│   │   └── commit_agent.py
│   ├── workflows/
│   │   └── sdls_workflow.py
│   ├── utils/
│   │   ├── ollama_client.py
│   │   └── file_utils.py
│   └── config/
│       └── settings.py
├── examples/
│   └── sample_project/
│       ├── src/
│       └── tests/
└── tests/
    └── test_workflow.py
```

## Example Workflow

The following example demonstrates a complete development cycle:

1. **Plan**: Agent analyzes requirements and creates development plan
2. **Implement**: Agent generates code based on plan
3. **Validate**: Agent tests implementation against requirements
4. **Commit**: Agent commits changes to version control

```python
# Example execution flow
workflow = SDLCWorkflow()
result = workflow.run(
    task="Implement REST API for user authentication",
    project_dir="examples/sample_project"
)
```

Each step is deterministic and state-aware, ensuring consistent behavior across runs.

## Safety Principles

- **Local execution**: All processing happens on local machine
- **Input validation**: Strict validation of all inputs and outputs
- **State isolation**: Each workflow step maintains clean state boundaries
- **Error handling**: Comprehensive error recovery and logging
- **Code review simulation**: Agents simulate peer review processes
- **No external dependencies**: All operations work offline
- **Reproducibility**: Same inputs always produce same outputs

## Roadmap

### Phase 1: Core Workflow
- [x] Basic SDLC workflow implementation
- [x] Local LLM integration with Ollama
- [x] State management and persistence

### Phase 2: Advanced Features
- [ ] Multi-agent collaboration patterns
- [ ] Integration with Git operations
- [ ] Automated testing orchestration

### Phase 3: Production Readiness
- [ ] Performance optimization
- [ ] Comprehensive error recovery
- [ ] Documentation and examples

### Phase 4: Extended Capabilities
- [ ] Support for additional LLM providers
- [ ] CI/CD pipeline integration
- [ ] Monitoring and observability

> Note: This is a work in progress. Contributions welcome via pull requests and issues.
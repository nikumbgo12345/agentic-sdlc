# agentic-sdlc

**A practical guide to implementing deterministic, agentic software development lifecycles using LangGraph and local LLMs.**

## What This Repo Is

This repository provides a production-ready framework for building **agentic software development workflows** using local LLMs (Ollama) and LangGraph. It demonstrates how to structure software development as a series of deterministic, traceable, and auditable steps that can be automated, monitored, and improved.

Unlike traditional approaches where LLMs are used as "smart assistants," this repo focuses on **structured, repeatable workflows** where LLMs act as agents within a defined system, making decisions based on clear inputs, constraints, and feedback loops.

## Why Deterministic Workflows Matter

In software development, especially when using LLMs, determinism ensures:

- **Reproducibility**: Same inputs produce same outputs
- **Auditability**: Every step is traceable and explainable
- **Reliability**: Systems behave predictably under similar conditions
- **Safety**: Reduces risk of unintended consequences from LLM outputs
- **Debugging**: Clear failure points and recovery mechanisms

This approach is critical when building systems that must be trusted in production environments.

## Quickstart

```bash
# 1. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull required local LLM
ollama pull qwen3-coder:30b
```

> **Note**: This repo assumes Ollama is installed and running locally. The default LLM model is `qwen3-coder:30b`.

## Folder Structure

```
agentic-sdlc/
├── src/
│   ├── agents/          # LLM agents for each SDLC stage
│   ├── workflows/       # LangGraph workflows
│   ├── tools/           # Utility functions and tooling
│   └── core/            # Core workflow logic and state management
├── examples/
│   └── sample_project/  # Sample project to demonstrate workflow
├── tests/
│   └── test_workflows.py # Unit tests for workflows
├── data/
│   └── logs/            # Workflow execution logs
├── config/
│   └── workflow_config.json # Configuration for workflow steps
├── README.md
└── requirements.txt
```

## Example Workflow: Plan → Implement → Validate → Commit

### 1. Plan
- Input: User-defined task (e.g., "Add user authentication")
- Agent: Planning agent
- Output: Structured plan with:
  - Implementation steps
  - File changes
  - Test requirements

### 2. Implement
- Input: Plan from previous step
- Agent: Code implementation agent
- Output: Modified files in working directory

### 3. Validate
- Input: Implemented changes
- Agent: Validation agent
- Output: Test results, linting, and correctness checks

### 4. Commit
- Input: Validated changes
- Agent: Git commit agent
- Output: Commit to repository with message and metadata

> **Note**: Each step is designed to be deterministic and auditable. All decisions are logged and can be replayed.

## Safety Principles

- **No arbitrary code execution**: All changes are validated and reviewed
- **Isolated execution**: Workflows run in isolated environments
- **Input sanitization**: All inputs are strictly validated
- **Reversible steps**: Each workflow step can be rolled back
- **Audit logs**: Every decision and action is recorded
- **Rate limiting**: Prevents abuse of LLM resources
- **Local execution**: No external data leakage or cloud dependency

## Roadmap

### Phase 1: Core Workflow
- [x] Basic plan → implement → validate → commit workflow
- [x] Integration with Ollama and LangGraph
- [x] Sample project with end-to-end example

### Phase 2: Advanced Features
- [ ] Multi-agent collaboration (e.g., code review, testing, deployment)
- [ ] Support for additional local LLMs (e.g., Llama3, Mistral)
- [ ] Integration with CI/CD pipelines
- [ ] Web UI for workflow monitoring

### Phase 3: Production Readiness
- [ ] Performance optimization
- [ ] Error recovery and retry mechanisms
- [ ] Scalability improvements
- [ ] Documentation and tutorials

---

*This project is licensed under the MIT License.*
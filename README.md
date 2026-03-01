# agentic-sdlc

A practical guide and reference implementation for implementing deterministic, agentic Software Development Life Cycle (SDLC) workflows using LangGraph and local LLMs (Ollama, qwen3-coder:30b).

## What This Repo Is

This repository demonstrates how to build an agentic SDLC system using LangGraph to orchestrate local LLMs for software development tasks. It provides best practices, example workflows, and safety patterns for automating code generation, validation, and commit processes using local LLMs (Ollama, qwen3-coder:30b) rather than cloud APIs.

## Why Deterministic Workflows Matter

In software development automation, deterministic workflows ensure:
- **Reproducible results**: Same inputs always produce same outputs
- **Auditability**: Clear traceability of decisions and changes
- **Debugging capability**: Easy to isolate and fix issues
- **Safety**: Reduced risk of unintended code changes
- **Compliance**: Meeting requirements for controlled environments

LangGraph provides the orchestration layer to create deterministic, step-by-step workflows that can be audited and validated.

## Quickstart

```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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
│   ├── __init__.py
│   ├── workflow.py          # Main LangGraph workflow definition
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── planner.py       # Planning agent
│   │   ├── implementer.py   # Code implementation agent
│   │   ├── validator.py     # Validation agent
│   │   └── committer.py     # Commit agent
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── safety.py        # Safety checks and validation utilities
│   │   └── ollama_client.py # Ollama client wrapper
│   └── config/
│       └── __init__.py      # Configuration management
├── examples/
│   └── sample_workflow.py   # Example usage
└── tests/
    └── test_workflow.py     # Unit tests
```

## Example Workflow

The core workflow follows these steps:

1. **Plan**: 
   - Analyze requirements
   - Break down into tasks
   - Create implementation plan

2. **Implement**: 
   - Generate code based on plan
   - Handle multiple code files
   - Maintain context

3. **Validate**: 
   - Run static analysis
   - Execute unit tests
   - Verify correctness

4. **Commit**: 
   - Create git commit
   - Add descriptive commit message
   - Push to remote

```python
# Example workflow execution
from src.workflow import agentic_workflow

# Input: requirements specification
requirements = "Create a Python function that sorts a list of dictionaries by a given key"

# Execute workflow
result = agentic_workflow.run(requirements)
print(result)
```

## Safety Principles

1. **Input Sanitization**: All inputs are validated before processing
2. **Output Validation**: Generated code is checked for syntax and correctness
3. **Execution Isolation**: Code generation happens in isolated environments
4. **Reversible Changes**: All changes can be reverted or reviewed before commit
5. **Rate Limiting**: Prevents abuse of local resources
6. **Configuration Management**: All LLM parameters are configurable and auditable

## Roadmap

### Phase 1: Core Workflow
- [x] Basic LangGraph workflow
- [x] Local LLM integration (Ollama)
- [x] Planning and implementation agents
- [x] Validation and commit agents

### Phase 2: Enhanced Safety
- [ ] Advanced input/output sanitization
- [ ] Execution sandboxing
- [ ] Comprehensive testing framework
- [ ] Error recovery mechanisms

### Phase 3: Advanced Features
- [ ] Multi-agent collaboration
- [ ] Git integration improvements
- [ ] Model selection and switching
- [ ] Performance optimization

### Phase 4: Documentation and Examples
- [ ] Detailed API documentation
- [ ] Real-world use case examples
- [ ] Performance benchmarks
- [ ] Security audit guidelines

*Note: This is a living repository. Contributions and feedback are welcome.*
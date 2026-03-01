# ARCHITECTURE.md

## Overview

This document describes the architectural decisions for our AI agent system, focusing on state machine-based reasoning using LangGraph, with careful attention to security, auditability, and extensibility.

## Why LangGraph State Machines Over Free-Form Agents

We use LangGraph state machines instead of free-form agents for the following reasons:

- **Predictable Control Flow**: State machines provide deterministic execution paths, making it easier to reason about agent behavior and debug issues
- **Improved Safety**: Explicit state transitions limit the agent's ability to make unexpected moves or escape controlled execution
- **Better Testing**: State machines can be easily unit tested with known input/output scenarios
- **Clear Boundaries**: Each state clearly defines what the agent can and cannot do, reducing security surface area
- **Auditability**: The explicit state transitions create a clear audit trail of agent decision-making

Free-form agents, while more flexible, introduce unpredictable behavior that makes it difficult to ensure security and compliance in production systems.

## Tool Boundary Design

### Shell Wrapper
All external commands are executed through a shell wrapper that:
- Enforces strict command allowlists
- Runs in isolated, read-only environments
- Prevents command injection through input sanitization
- Logs all executed commands with parameters

### Allowlists
- Only predefined commands can be executed
- Each tool has a configured allowlist of acceptable arguments
- Arguments are validated against expected patterns (regex, enum, etc.)
- No shell metacharacters or command composition allowed

### Working Directory (cwd)
- Tools execute in dedicated, isolated working directories
- No access to parent or sibling directories
- Temporary directories are cleaned up after execution
- No persistent state is maintained between tool invocations

### No Hidden Side Effects
- All tool operations are explicitly logged
- No automatic file creation, network connections, or system modifications
- All side effects are intentional and observable
- Tools must return explicit results rather than modifying environment state

## Logging/Audit Strategy

### Structured Logs
All agent actions are logged in structured JSON format with:
- Timestamp and execution ID
- Agent state transitions
- Tool invocations and their results
- Input/output data for each step
- Error details and stack traces

### Audit Trail
- Full execution history stored in persistent storage
- Each state transition is timestamped and auditable
- Tool execution logs are stored separately but linked to execution ID
- Compliance with audit requirements through detailed, immutable logs

### Security Monitoring
- Logs are monitored for suspicious patterns
- Failed tool executions trigger alerts
- Access to logs is restricted and audited
- Logs are retained according to compliance policies

## Git as Validation Layer

### Configuration Management
- All agent configurations are stored in Git repositories
- Version control ensures reproducible environments
- Changes to tools, workflows, or state definitions are reviewed through pull requests
- Rollbacks are possible through Git history

### Workflow Validation
- Workflow definitions are validated against a schema before deployment
- Tool configurations are validated against expected interfaces
- Changes are tested in isolated environments before merging
- Git hooks enforce code quality and security checks

### Deployment Pipeline
- Deployments are triggered by Git commits to specific branches
- Automated testing runs against Git-staged changes
- Rollbacks are implemented through Git history
- Immutable deployments ensure consistent execution environments

## Extending with New Workflows/Tools

### Adding New Tools
1. Create tool configuration in Git repository
2. Define allowlist of acceptable inputs
3. Implement tool wrapper with shell isolation
4. Test tool in isolated environment
5. Submit pull request for review
6. Merge after validation and security review

### Adding New Workflows
1. Define new state machine transitions
2. Create workflow configuration in Git
3. Implement state validation logic
4. Test workflow execution path
5. Submit pull request for review
6. Merge after testing and approval

### Extension Points
- Tool interfaces are standardized through JSON schemas
- Workflow definitions are extensible through configuration
- New tools can be added without modifying core agent logic
- State machine transitions are defined in configuration rather than code

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Input     │───▶│   State     │───▶│   Tool      │
│   Handler   │    │   Machine   │    │   Wrapper   │
└─────────────┘    └─────────────┘    └─────────────┘
                         │
                         ▼
               ┌─────────────────┐
               │   Git Repo      │
               │   (Validation)  │
               └─────────────────┘
                         │
                         ▼
               ┌─────────────────┐
               │   Audit Logs    │
               │   (Structured)  │
               └─────────────────┘
```
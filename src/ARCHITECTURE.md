# ARCHITECTURE.md

## Overview

This document describes the architectural principles and design decisions for our AI agent system, focusing on LangGraph-based state machines, secure tool execution, and operational reliability.

## Why LangGraph State Machines Over Free-Form Agents

We use LangGraph state machines instead of free-form agents for several practical reasons:

- **Predictable behavior**: State machines enforce clear transitions and prevent agents from "going off the rails" into unintended actions
- **Easier debugging**: With explicit states and transitions, we can trace exactly what the agent did and why
- **Better security**: We can audit and restrict state transitions, making it harder for malicious inputs to cause unexpected behavior
- **Maintainability**: Clear state boundaries make it easier to understand, modify, and extend agent behavior
- **Operational reliability**: State machines provide deterministic execution paths that are easier to monitor and alert on

## Tool Boundary Design

### Shell Wrapper
All external tool execution goes through a controlled shell wrapper that:
- Runs in a sandboxed environment with limited privileges
- Enforces strict command whitelisting
- Prevents command injection through input sanitization
- Logs all executed commands with arguments

### Allowlists
- Only pre-approved commands can be executed
- Each tool has a defined set of allowed arguments and flags
- Configuration files define tool permissions (e.g., `tools.yaml`)

### Working Directory
- Tools execute in a dedicated, isolated working directory
- No access to parent or sibling directories
- Directory is cleaned up after each tool execution
- No cross-contamination between tool executions

### No Hidden Side Effects
- All tool outputs are captured and logged
- No file system modifications outside of controlled paths
- No network connections beyond explicitly allowed domains
- No environment variable modifications

## Logging and Audit Strategy

### Structured Logging
All agent actions are logged in structured JSON format:
```json
{
  "timestamp": "2023-10-01T12:00:00Z",
  "agent_id": "reviewer-123",
  "action": "execute_tool",
  "tool_name": "git_status",
  "input": {"repo_path": "/tmp/repo-abc"},
  "output": {"status": "clean"},
  "duration_ms": 42,
  "user_id": "user-456"
}
```

### Audit Trail
- Every state transition is recorded
- Tool execution logs are stored separately but linked to the agent session
- Session IDs tie all logs together for traceability
- Logs are retained for 90 days with automated archival

### Monitoring
- Real-time alerts for failed tool executions
- Anomaly detection on execution patterns
- Resource usage monitoring (CPU, memory, disk)

## Git as Validation Layer

We use Git as a validation layer in several ways:

### State Validation
- Agent state is periodically committed to a Git repository
- Each state transition creates a new Git commit with metadata
- This allows us to rollback to previous valid states if needed
- Git history provides an immutable audit log of agent decisions

### Configuration Management
- All tool configurations are stored in Git
- Changes to allowed tools or parameters require pull requests
- Version control ensures we can track when and why tool permissions changed

### Workflow Validation
- Workflow definitions are stored in Git
- Each workflow change is reviewed and tested
- Git hooks validate workflow syntax and security before deployment

## Extending with New Workflows/Tools

### Adding New Tools
1. Define tool in `tools.yaml` with:
   - Name and description
   - Allowed arguments and flags
   - Required permissions
   - Output format specification
2. Implement tool in the shell wrapper
3. Add to allowlist in the configuration
4. Test with automated test suite
5. Create Git commit with documentation

### Adding New Workflows
1. Define workflow in `workflows.yaml`
2. Create state machine definition using LangGraph
3. Implement state transition logic
4. Add to workflow registry
5. Test with sample inputs
6. Document workflow behavior and expected inputs

### Example Extension Process
```
1. Create tool definition in tools.yaml
2. Implement shell wrapper logic
3. Add to allowlist
4. Write test cases
5. Commit to Git with documentation
6. Deploy to staging
7. Validate with automated tests
8. Promote to production
```

## System Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   LangGraph     │───▶│   Tool Executor │
│                 │    │   State Machine │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │   State Store   │    │   Shell Wrapper │
                    │                 │    │                 │
                    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │   Git Validator │    │   Audit Logger  │
                    │                 │    │                 │
                    └─────────────────┘    └─────────────────┘
```

## Implementation Notes

- All configurations are version-controlled in Git
- Tool execution is asynchronous with timeouts
- State machine transitions are idempotent where possible
- Error handling includes rollback to previous valid states
- Regular security audits of tool allowlists
- Automated testing for all workflow and tool changes

This architecture balances flexibility with security, allowing us to extend functionality while maintaining operational control and auditability.
# Architecture

## Why LangGraph State Machines over Free-Form Agents

Free-form agents lack structure and predictability. They can wander into unintended behaviors, make inconsistent decisions, or fail to terminate properly. LangGraph state machines provide:

- **Explicit state transitions** that are easy to reason about and test
- **Clear boundaries** between agent phases (planning, execution, validation)
- **Deterministic behavior** that enables reliable deployment and monitoring
- **Easier debugging** through explicit state tracking and transition logging

## Tool Boundary Design

Tools must be carefully sandboxed to prevent unintended side effects:

### Shell Wrapper
- Tools execute in isolated shell environments
- Each tool has its own dedicated execution context
- No shared state between tool invocations

### Allowlists
- Only pre-approved commands and file paths are permitted
- Tools cannot execute arbitrary shell commands
- File system access is restricted to explicitly allowed directories

### Working Directory (cwd)
- Tools execute in a dedicated, isolated working directory
- No access to parent process working directory
- All tool operations are confined to this boundary

### No Hidden Side Effects
- Tools cannot modify global state or environment variables
- All tool outputs must be explicitly returned via stdout/stderr
- No background processes or daemon creation allowed

## Logging/Audit Strategy

### Core Requirements
- **Complete traceability** of all agent decisions and tool usage
- **Audit-ready logs** for compliance and debugging
- **Structured logging** for automated analysis

### Log Structure
```json
{
  "timestamp": "2023-10-01T12:00:00Z",
  "agent_id": "task_executor_123",
  "workflow": "deploy_app",
  "step": "validate_config",
  "input": { "config": "..." },
  "output": { "valid": true },
  "tool_calls": [
    {
      "tool": "validate_yaml",
      "args": { "file": "config.yaml" },
      "result": { "valid": true }
    }
  ],
  "duration_ms": 123
}
```

### Storage
- Logs written to structured format (JSON) to stdout
- Aggregated in centralized logging system
- Retention policies applied per log type

## Git as Validation Layer

Git serves as the authoritative validation layer for all agent operations:

### Configuration Validation
- All agent configurations are stored in Git
- Changes must be committed and reviewed before deployment
- Git hooks validate configuration syntax and policy compliance

### Workflow Integrity
- Workflows are version-controlled and immutable
- Each workflow execution is tied to a specific Git commit
- Rollbacks are possible by reverting to previous commits

### Change Tracking
- Every tool invocation is logged with Git context
- Audits can trace back to exact code versions used
- Policy violations are flagged through Git diff analysis

## Extending with New Workflows/Tools

### Adding New Tools
1. Create tool in isolated directory with:
   - `tool.sh` - executable script
   - `metadata.json` - tool description and parameters
   - `allowlist.txt` - permitted commands/paths
2. Add to tool registry in Git
3. Run integration tests
4. Deploy with new commit

### Adding New Workflows
1. Define workflow in YAML format
2. Create state machine definition
3. Implement validation logic
4. Add to Git repository
5. Test with sample inputs

### Extension Points
- **Plugin system** for workflow composition
- **Hook system** for pre/post processing
- **Configuration-driven** tool selection and execution

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent Core    │    │   Tool Registry │    │   Workflow      │
│                 │    │                 │    │   Definition    │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  State    │  │    │  │  Tool     │  │    │  │  YAML     │  │
│  │  Machine  │  │    │  │  Config   │  │    │  │  Schema   │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  Input    │  │    │  │  Shell    │  │    │  │  State    │  │
│  │  Handler  │  │    │  │  Wrapper  │  │    │  │  Graph    │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  Output   │  │    │  │  Allowlist│  │    │  │  Validator│  │
│  │  Handler  │  │    │  │  Check    │  │    │  │  Logic    │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                    ┌─────────────────┐
                    │    Git Layer    │
                    │                 │
                    │  Version Control│
                    │  Policy Check   │
                    │  Audit Trail    │
                    └─────────────────┘
```
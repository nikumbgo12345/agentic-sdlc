# SAFETY.md

Safety guidelines for agentic coding workflows

## Human-in-the-loop Gates

All automated code generation and deployment operations must include human review checkpoints:

- **Code Review Required**: Any changes to production code, configuration files, or infrastructure-as-code must be reviewed by a human before execution
- **Deployment Approval**: Automated deployments to production environments require explicit human approval via CLI or web interface
- **Security Scan Results**: Automated security scans must be manually reviewed before any remediation actions are taken
- **Data Migration Confirmation**: Automated data migration operations require human confirmation of migration plan and rollback strategy
- **Performance Impact Assessment**: Any automated changes that could affect system performance must be reviewed by a human before execution

## Command Allowlisting / Denylisting

Implement strict command execution controls:

- **Allowlist Only**: Only explicitly approved commands may be executed by agents
- **Denylist Critical Operations**: Prohibit commands that modify system state, access sensitive data, or interact with external services
- **Command Validation**: All commands must be validated against a central registry before execution
- **Privilege Separation**: Agents must run with minimal required privileges; avoid root or admin-level access
- **Logging Required**: All command executions must be logged with full command line, user context, and execution timestamp

## Secrets Hygiene

Protect sensitive information in automated workflows:

- **Never Log Secrets**: All secrets must be redacted from logs, outputs, and error messages
- **Environment Variables Only**: Secrets must be passed via environment variables, never hardcoded or stored in files
- **Rotation Policy**: Automated secrets rotation must be implemented with human oversight
- **Access Control**: Secrets must be stored in secure vaults with granular access controls
- **Audit Trail**: All secret access must be logged and audited regularly

## Avoiding Destructive Operations

Prevent accidental system damage through operational safeguards:

- **No Direct Filesystem Modification**: Agents may not directly modify files outside of designated code generation directories
- **Backup Required**: Any operation that modifies existing code or configuration must create a backup before proceeding
- **Dry Run Mode**: All destructive operations must support a dry-run mode that shows what would be changed without executing
- **Revert Mechanism**: Every automated destructive operation must have a built-in rollback capability
- **Confirmation Required**: Any operation that could result in data loss must require explicit human confirmation

## Reproducibility Requirements

Ensure automated workflows are deterministic and reliable:

- **Version Pinning**: All dependencies, tools, and libraries must be pinned to specific versions
- **Isolated Environments**: Automated workflows must run in isolated environments with no shared state
- **Idempotent Operations**: All automated operations must be idempotent - running twice should have same effect as running once
- **Reproducible Builds**: Build artifacts must be reproducible given the same inputs and environment
- **Documentation**: Every automated workflow must include clear documentation of expected inputs, outputs, and side effects

## What NOT to Automate

Certain activities must remain human-controlled:

- **Security Policy Enforcement**: Security decisions, especially those involving risk assessment and compliance, must be human-reviewed
- **Strategic Planning**: Long-term architectural decisions, feature prioritization, and roadmap planning are not suitable for automation
- **Customer Interaction**: All direct customer communication, support tickets, and user experience decisions must remain human-controlled
- **Legal and Compliance**: Legal document review, regulatory compliance verification, and audit preparation require human judgment
- **Creative Design**: UI/UX design decisions, branding, and creative content generation should not be automated
- **Critical System Decisions**: Decisions about system shutdown, major service interruptions, or emergency responses must be human-initiated
- **Financial Transactions**: Any automated financial operations require human oversight and approval
- **Data Privacy**: Data handling decisions, especially involving personal information, must be human-reviewed
- **Ethical Considerations**: Any automated system that makes decisions affecting human welfare must include human oversight

---

*Last Updated: 2023-11-15*  
*Version: 1.0*
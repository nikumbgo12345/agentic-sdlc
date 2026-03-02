# SAFETY.md

## Safety Guidelines for Agentic Coding Workflows

This document outlines safety practices for automated coding systems to prevent unintended consequences, data loss, and security vulnerabilities.

## Human-in-the-Loop Gates

### Critical Decision Points
- **Code Execution**: Any code that modifies production systems or executes with elevated privileges must require explicit human approval
- **Deployment Operations**: Automated deployments to production environments must be blocked until human verification
- **Data Modification**: Any operation that modifies or deletes data (database, file systems, cloud resources) requires human confirmation
- **Security Changes**: Modifications to authentication, authorization, or security configurations must be reviewed by security personnel

### Implementation Requirements
- All human gates must be clearly marked in the workflow
- Timeout mechanisms should be implemented (e.g., 10-minute window for approval)
- Audit logs must record all human interventions
- Escalation paths should be defined for unresponsive gates

## Command Allowlisting / Denylisting

### Allowlisted Commands
- `git status`, `git diff`, `git log`
- `npm install`, `pip install`
- `docker build`, `docker run`
- `kubectl apply`, `kubectl delete`
- `terraform plan`, `terraform apply`

### Denylisted Commands
- `rm -rf`
- `dd`
- `mkfs`
- `shutdown`
- `sudo`
- `chmod 777`
- `wget` or `curl` to arbitrary URLs without validation

### Implementation Requirements
- All commands must be validated against allowlist before execution
- Denylist should be maintained as a comprehensive security reference
- Dynamic command validation should be implemented in the agent's execution layer
- Logs must record all command executions, including those that fail validation

## Secrets Hygiene

### Secret Management
- All secrets must be stored in secure vaults (HashiCorp Vault, AWS Secrets Manager, etc.)
- Secrets should never be hardcoded in source code or configuration files
- Environment variables should be used for secret injection, not direct file references
- Secrets should be rotated regularly (minimum 90 days for most credentials)

### Access Controls
- Least privilege principle: agents should only access secrets needed for their specific tasks
- Secrets should be rotated automatically when agents are compromised
- All secret access should be logged and audited
- Secrets should be automatically cleared from memory after use

### Implementation Requirements
- All automated systems must fail gracefully if secrets are not available
- Secret rotation should be integrated into the agent's lifecycle management
- Regular audits should verify no unauthorized secret access has occurred

## Avoiding Destructive Operations

### Safe Operation Principles
- All destructive operations must be reversible or have clear rollback procedures
- File system operations should be validated against a safe directory whitelist
- Database operations should be executed in transactions with proper rollback capabilities
- Cloud resource operations should be validated against resource type allowlists

### Validation Requirements
- Before any destructive operation, validate that:
  - The operation is within allowed scope
  - The target resources exist and are accessible
  - The operation will not cause unintended side effects
  - Backup procedures are in place

### Implementation Requirements
- Destructive operations should be flagged with clear warnings
- Operations should be tested in staging environments before production use
- Rollback mechanisms should be automatically triggered on failure
- All destructive operations should be logged with full context

## Reproducibility Requirements

### Version Control
- All automated workflows must be version-controlled with clear commit history
- Dependencies should be pinned to specific versions (lock files, package managers)
- Configuration files should be stored in version control with clear documentation
- Workflow definitions should be declarative and deterministic

### Environment Consistency
- All agents must run in reproducible environments (containerized, VM-based)
- Dependencies should be installed from trusted sources only
- Environment variables should be consistent across all execution contexts
- All system state should be captured and restored as needed

### Implementation Requirements
- Automated testing should validate reproducibility of workflows
- All workflow outputs should be deterministic given the same inputs
- State should be explicitly managed and not rely on implicit system state
- Versioning strategy should be applied to all components

## What NOT to Automate

### High-Risk Operations
- **Production Deployments**: Manual review required for all production changes
- **Security Configuration**: Authentication, authorization, network policies
- **Data Migration**: Large-scale data operations with potential for corruption
- **System Shutdown**: Any operation that could affect availability
- **Financial Operations**: Payment processing, billing, account management

### Human-Centric Tasks
- **Code Review**: Complex judgment calls require human expertise
- **Strategic Planning**: Business decisions and architectural choices
- **User Experience**: UI/UX decisions that require human empathy
- **Legal Compliance**: Regulatory and compliance decisions
- **Crisis Management**: Emergency response and troubleshooting

### Implementation Requirements
- Clear boundaries should be defined between automated and manual processes
- Risk assessments should be performed before any automation decision
- Manual override mechanisms should be available for all automated systems
- Regular review of automation scope should be conducted to ensure continued safety

## Emergency Procedures

### Immediate Actions
- Any automated system failure should trigger alerts to human operators
- All automated operations should have clear "emergency stop" mechanisms
- Backup and recovery procedures should be tested regularly
- Incident response protocols should be clearly documented

### Post-Incident Review
- All incidents should be documented and analyzed
- Root cause analysis should be performed for any automation failures
- Safety measures should be updated based on lessons learned
- Regular safety audits should be conducted on automated systems

---

*Last Updated: 2023*
*This document is a living standard and should be updated regularly based on operational experience and security considerations.*
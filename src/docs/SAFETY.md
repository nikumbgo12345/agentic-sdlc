# SAFETY.md

Safety guidelines for agentic coding workflows

## Human-in-the-Loop Gates

### Critical Decision Points
- **Code Generation Approval**: All code changes must be reviewed by a human before execution
- **File System Modifications**: Any file creation, deletion, or modification requires explicit human confirmation
- **External API Calls**: All external service interactions must be manually approved
- **Deployment Operations**: Any deployment or release actions require human sign-off
- **Security-sensitive Changes**: Modifications to authentication, authorization, or security configurations must be reviewed by security personnel

### Review Requirements
- **Pull Request Integration**: Automated changes must be submitted as pull requests for human review
- **Change Summary**: Automated agents must provide clear summaries of changes for human review
- **Risk Assessment**: Each automated operation must include a risk assessment and mitigation plan

## Command Allowlisting / Denylisting

### Allowlisted Commands
- `git status`, `git diff`, `git add`, `git commit`, `git push`
- `npm install`, `yarn install`, `pip install`
- `docker build`, `docker run`, `docker push`
- `kubectl apply`, `kubectl delete`, `kubectl get`
- `ls`, `cat`, `grep`, `find`
- `echo`, `printf`, `basename`, `dirname`

### Denylisted Commands
- `rm -rf`, `dd`, `mkfs`, `format`
- `su`, `sudo`, `chmod 777`
- `curl`, `wget` (unless explicitly allowed for specific endpoints)
- `shutdown`, `reboot`, `poweroff`
- `kill`, `pkill`, `killall`
- Any command that modifies system-level configurations without explicit human approval

### Implementation Notes
- Commands are validated at execution time
- Denylisted commands are blocked entirely
- Allowlisted commands are permitted with logging
- Configuration changes to allowlists require human approval

## Secrets Hygiene

### Secret Storage
- All secrets must be stored in encrypted vaults (e.g., HashiCorp Vault, AWS Secrets Manager)
- Secrets must never be stored in code repositories or logs
- Secrets must be rotated regularly (minimum every 90 days)

### Access Control
- Secrets must be accessed only through secure, authenticated channels
- Least privilege principle: agents must only access secrets necessary for their operations
- Access logs must be maintained for all secret access

### Environment Handling
- Secrets must never be passed as command-line arguments
- Environment variables containing secrets must be cleared after use
- Secrets must be injected at runtime, not compiled into binaries

## Avoiding Destructive Operations

### File System Safety
- All file operations must be performed in a sandboxed environment
- File deletions must be reversible (backup before deletion)
- Directory operations must be validated against a whitelist of allowed paths
- Operations on system directories (e.g., `/etc`, `/usr`) are strictly prohibited

### Database Operations
- All database changes must be wrapped in transactions
- Destructive operations (DELETE, DROP) must require explicit human confirmation
- Data backups must be performed before any destructive operation
- Schema changes must be validated against a test environment first

### Network Operations
- Network connectivity must be limited to pre-approved endpoints
- Port scanning operations are prohibited
- All network traffic must be logged and monitored

## Reproducibility Requirements

### Environment Consistency
- All agents must operate in identical environments
- Dependencies must be pinned to specific versions
- Container images must be built from deterministic sources
- Environment variables must be consistent across all executions

### Execution State
- All agent operations must be idempotent where possible
- State changes must be logged and replayable
- Execution history must be preserved for debugging
- Version control of agent configurations is required

### Output Validation
- Generated code must pass automated tests before human review
- Generated documentation must be validated against templates
- Generated artifacts must be compared against expected outputs

## What NOT to Automate

### High-Risk Operations
- **System-level modifications**: Kernel updates, system configuration changes
- **Security-sensitive tasks**: Certificate management, firewall rule changes
- **Data migration**: Large-scale data transfers, schema changes
- **Production deployments**: Direct deployment to production environments

### Creative Tasks
- **Code architecture decisions**: System design, architectural patterns
- **Business logic design**: Feature requirements, user experience decisions
- **Quality assurance**: Manual testing, user acceptance testing
- **Strategic planning**: Roadmap decisions, feature prioritization

### Human-Centric Activities
- **Code review**: Human judgment on code quality, maintainability
- **Stakeholder communication**: Client meetings, project status updates
- **Training and mentoring**: Knowledge transfer, skill development
- **Creative problem solving**: Innovative solutions, design thinking

### Regulatory Compliance
- **Legal review**: Contract terms, compliance requirements
- **Audit processes**: Internal and external audits
- **Regulatory submissions**: Government filings, compliance reports

### Exception Handling
- **Emergency response**: Crisis management, incident response
- **Ethical decision making**: Moral dilemmas, ethical considerations
- **Complex negotiation**: Multi-party negotiations, conflict resolution

## Monitoring and Alerting

### Safety Metrics
- Track all denied operations
- Monitor for unusual patterns in automated behavior
- Log all human approvals and interventions
- Monitor for security incidents

### Incident Response
- Immediate human intervention required for safety violations
- Automated rollback procedures for failed operations
- Clear escalation paths for safety concerns
- Post-incident analysis and process improvement

## Compliance Requirements

### Industry Standards
- Adhere to SOC 2, ISO 27001, or equivalent security standards
- Follow applicable data protection regulations (GDPR, CCPA)
- Maintain audit trails for all operations
- Comply with organizational security policies

### Documentation
- All safety procedures must be documented and maintained
- Change logs for safety configurations
- Regular safety training for all team members
- Incident reporting and analysis processes

---
*Last Updated: 2023*
*This document is a living specification and should be updated as automation capabilities evolve*
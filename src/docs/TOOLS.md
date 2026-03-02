# Tools and Boundaries for Local Agent System

This document defines the operational boundaries and constraints for tools used in our local agent system. These boundaries ensure security, predictability, and controlled execution of agent operations.

## Filesystem Rules

### Allowed Write Locations
Agents may write to:
- **Temporary directories**: `/tmp/agent-<timestamp>` or `C:\temp\agent-<timestamp>` (platform-specific)
- **Agent-specific workspaces**: `/var/lib/agent/<agent-id>/workspace/` (Linux) or `C:\ProgramData\agent\<agent-id>\workspace\` (Windows)
- **Output directories**: `/var/lib/agent/<agent-id>/output/` (Linux) or `C:\ProgramData\agent\<agent-id>\output\` (Windows)

### Disallowed Write Locations
Agents **must not** write to:
- System directories: `/etc`, `/bin`, `/usr/bin`, `/lib`
- User home directories: `~/.ssh`, `~/Documents`, `~/Downloads`
- Root filesystem: `/`, `/var`, `/home`
- Any directory outside of the agent's designated workspace

### Example Allowed Operations
```bash
# ✅ Valid - writing to temporary directory
mkdir -p /tmp/agent-123456789
echo "output" > /tmp/agent-123456789/result.txt

# ✅ Valid - writing to agent workspace
mkdir -p /var/lib/agent/abc123/workspace
echo "data" > /var/lib/agent/abc123/workspace/data.json
```

### Example Disallowed Operations
```bash
# ❌ Invalid - attempting to write to system directory
echo "config" > /etc/agent.conf

# ❌ Invalid - attempting to write to user directory
echo "output" > ~/.config/agent/output.txt
```

## Shell Rules

### Allowlisted Commands
Agents may execute the following commands:
- `ls`, `cat`, `grep`, `find`, `which`, `whereis`
- `mkdir`, `rm`, `cp`, `mv`, `chmod`, `chown`
- `python3`, `node`, `bash`, `sh`
- `git` (with specific restrictions)
- `curl`, `wget`
- `tar`, `gzip`, `gunzip`
- `ps`, `top`, `kill`

### Disallowed Commands
Agents **must not** execute:
- `sudo`, `su`, `passwd`, `useradd`, `userdel`
- `dd`, `mkfs`, `mount`, `umount`
- `rm -rf /`, `rm -rf ~`
- Any command that modifies system state or permissions
- `ssh`, `scp`, `telnet`, `ftp`

### Example Allowed Operations
```bash
# ✅ Valid - basic file operations
ls -la /tmp
grep "pattern" /var/log/app.log
mkdir -p /tmp/agent-workspace
cp file1.txt file2.txt

# ✅ Valid - network operations
curl -O https://example.com/data.json
wget https://example.com/file.txt
```

### Example Disallowed Operations
```bash
# ❌ Invalid - system modification
sudo apt-get update
rm -rf /
sudo useradd eviluser
```

## Git Rules

### Allowed Git Operations
Agents may execute:
- `git clone` (only from allowlisted repositories)
- `git pull` (only on existing repositories)
- `git status`, `git log`, `git diff`
- `git add`, `git commit`, `git push` (only to allowlisted branches)
- `git config --global user.name`, `user.email`

### Repository Restrictions
Agents may only operate on repositories:
- Hosted on allowlisted domains: `github.com`, `gitlab.com`
- Within allowlisted organizations: `mycompany/agent-repos`
- With specific repository patterns: `agent-*`, `project-*`

### Branch Restrictions
Agents may only push to:
- `main`, `develop`, `feature/*`
- `release/*`, `hotfix/*`
- Any branch matching `agent-*`

### Example Allowed Operations
```bash
# ✅ Valid - cloning from allowlisted repo
git clone https://github.com/mycompany/agent-repos.git

# ✅ Valid - pushing to allowed branch
git add .
git commit -m "Update"
git push origin main
```

### Example Disallowed Operations
```bash
# ❌ Invalid - cloning from unauthorized domain
git clone https://evil.com/repo.git

# ❌ Invalid - pushing to unauthorized branch
git push origin master
```

## GitHub Publishing Rules

### GitHub CLI Usage
Agents may use `gh` CLI for:
- `gh repo create` (only for allowlisted organization)
- `gh release create` (only for tagged releases)
- `gh pr create` (only for allowlisted branches)
- `gh issue create` (only for allowlisted repositories)

### Repository Permissions
Agents may only publish to:
- Repositories in `mycompany/agent-projects`
- Repositories with `agent-*` prefix
- Repositories where `gh` is configured with proper credentials

### Example Allowed Operations
```bash
# ✅ Valid - creating release
gh release create v1.2.3 --notes "Release notes"

# ✅ Valid - creating pull request
gh pr create --title "Fix bug" --body "Fixes issue #123"
```

### Example Disallowed Operations
```bash
# ❌ Invalid - creating repository in unauthorized organization
gh repo create evilorg/repo

# ❌ Invalid - creating issue in unauthorized repository
gh issue create --repo evilorg/repo --title "Bug"
```

## Logging and Trace Expectations

### Log Output Format
All agent operations must output structured logs in JSON format:
```json
{
  "timestamp": "2023-12-01T10:00:00Z",
  "agent_id": "abc123",
  "operation": "file_write",
  "status": "success",
  "details": {
    "path": "/tmp/agent-123456789/result.txt",
    "size": 1024
  }
}
```

### Trace Requirements
- All operations must include a unique trace ID
- Operations must be logged at `INFO` level or higher
- Failed operations must be logged at `ERROR` level with stack traces
- Timing information must be recorded for all operations

### Example Log Output
```bash
# Operation log
{"timestamp":"2023-12-01T10:00:00Z","agent_id":"abc123","operation":"git_clone","status":"success","details":{"repo":"https://github.com/mycompany/agent-repos.git","trace_id":"trace-456789"}}

# Error log
{"timestamp":"2023-12-01T10:00:05Z","agent_id":"abc123","operation":"file_write","status":"error","details":{"path":"/etc/config.conf","error":"Permission denied","trace_id":"trace-456789"}}
```

### Log Storage
- Logs must be written to `/var/log/agent/<agent-id>/`
- Log rotation must occur daily
- Logs must be retained for 30 days
- Error logs must be sent to centralized monitoring system
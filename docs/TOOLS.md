# Tools and Boundaries

This document defines the operational boundaries and rules for local agent tools within our system. These boundaries ensure security, reproducibility, and controlled execution.

## Filesystem Rules

### Allowed Write Locations
Agents may only write to:
- `/tmp/agent-<timestamp>` - Temporary working directory (automatically cleaned up)
- `$HOME/.agent/cache` - Persistent cache directory
- `$HOME/.agent/logs` - Log output directory

### Disallowed Operations
- Writing to `/etc`, `/usr`, or system directories
- Modifying files outside the allowed paths
- Creating symbolic links outside allowed scope
- Writing to `/tmp` outside the agent-specific directory

### Example
```bash
# ✅ Allowed
echo "data" > /tmp/agent-123456789/output.txt
mkdir -p $HOME/.agent/cache/project-a

# ❌ Not Allowed
echo "data" > /etc/passwd
cp file.txt /usr/local/bin/
```

## Shell Command Rules

### Allowlisted Commands
Agents may execute these commands:
- `ls`, `cat`, `grep`, `find`
- `mkdir`, `rm`, `cp`, `mv`
- `python3`, `node`, `bash`
- `git` (with restrictions)
- `curl`, `wget`
- `tar`, `gzip`, `unzip`

### Disallowed Commands
- `sudo`, `su`, `chmod`, `chown`
- `ssh`, `telnet`, `nc`
- `rm -rf /`
- Any command that could modify system state

### Example
```bash
# ✅ Allowed
ls -la
find . -name "*.py" -type f
python3 script.py
curl https://api.example.com/data

# ❌ Not Allowed
sudo apt-get update
rm -rf /
ssh user@host
```

## Git Rules

### Allowed Operations
- `git clone` (with repository validation)
- `git status`, `git diff`, `git log`
- `git add`, `git commit`, `git push` (with specific branch restrictions)
- `git checkout`, `git merge` (local only)
- `git remote` (read-only)

### Disallowed Operations
- `git init` in non-allowed directories
- Direct push to protected branches
- `git reset --hard`
- Any operation modifying remote repositories without explicit permission

### Example
```bash
# ✅ Allowed
git clone https://github.com/user/repo.git
git add .
git commit -m "update"
git push origin main

# ❌ Not Allowed
git init
git reset --hard HEAD
git push origin master  # if master is protected
```

## GitHub Publishing Rules

### gh CLI Usage
Agents may use `gh` CLI for:
- Creating issues: `gh issue create`
- Creating pull requests: `gh pr create`
- Uploading artifacts: `gh release create`
- Listing repositories: `gh repo list`

### Disallowed Operations
- Direct repository creation
- Modifying repository settings
- Deleting releases or branches
- Pushing directly to protected branches
- Using `gh` without explicit repository context

### Example
```bash
# ✅ Allowed
gh issue create --title "Bug Report" --body "..."
gh pr create --title "Fix bug" --body "..."
gh release create v1.0.0 --notes "Release notes"

# ❌ Not Allowed
gh repo create my-repo
gh release delete v1.0.0
gh repo edit --description "new description"
```

## Logging and Trace Expectations

### Log Format
All logs must be in structured JSON format:
```json
{
  "timestamp": "2023-12-01T10:00:00Z",
  "level": "info",
  "message": "Operation completed",
  "operation": "file_write",
  "duration_ms": 150,
  "metadata": {
    "path": "/tmp/agent-123456789/output.txt"
  }
}
```

### Log Levels
- `info`: General operational information
- `warn`: Recoverable issues
- `error`: Non-recoverable failures
- `debug`: Development debugging information

### Log Destination
All logs must be written to `$HOME/.agent/logs/agent-<timestamp>.log` with rotation:
- Maximum 100MB per log file
- Rotate when file reaches 100MB
- Keep 3 rotated files

### Example Log Entry
```json
{
  "timestamp": "2023-12-01T10:00:00Z",
  "level": "info",
  "message": "File written successfully",
  "operation": "file_write",
  "duration_ms": 150,
  "metadata": {
    "path": "/tmp/agent-123456789/output.txt",
    "size_bytes": 1024
  }
}
```
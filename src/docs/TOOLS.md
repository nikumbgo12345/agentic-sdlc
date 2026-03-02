# Tools and Boundaries

This document defines the operational boundaries and constraints for local agent tools in our system. These boundaries ensure security, predictability, and maintainability of automated operations.

## Filesystem Rules

### Allowed Write Locations
Agents may only write to:
- `$HOME/.agent-data/` (created on first use)
- `$HOME/.cache/agent-cache/` (for temporary caching)
- `$HOME/Downloads/agent-output/` (for exportable results)

### Example
```bash
# ✅ Allowed
echo "output" > $HOME/.agent-data/my-task.json
mkdir -p $HOME/.cache/agent-cache/tmp && echo "cache" > $HOME/.cache/agent-cache/tmp/data.txt

# ❌ Not Allowed
echo "output" > /etc/config.txt
echo "output" > /tmp/myfile.txt
```

### Restrictions
- No writes to system directories (`/usr`, `/bin`, `/etc`)
- No writes to parent directories of allowed locations
- No symbolic link resolution outside allowed paths
- No file operations on `/tmp` or `/var/tmp`

## Shell Command Rules

### Allowlisted Commands
Agents may execute only these commands:
- `ls`, `cat`, `grep`, `find`, `stat`, `pwd`, `basename`, `dirname`
- `mkdir`, `cp`, `mv`, `rm`, `chmod`, `chown`
- `git`, `gh`, `curl`, `wget`, `tar`, `unzip`
- `python3`, `node`, `bash` (limited to script execution)
- `date`, `whoami`, `id`, `uname`

### Example
```bash
# ✅ Allowed
ls -la $HOME/.agent-data/
mkdir -p $HOME/.cache/agent-cache/
git status
curl -s https://api.github.com/repos/user/repo

# ❌ Not Allowed
rm -rf /
chmod 777 /etc/passwd
ping google.com
```

## Git Rules

### Repository Operations
Agents may:
- Clone repositories to `$HOME/.agent-data/`
- Create new branches with `git checkout -b`
- Commit changes with `git commit -m`
- Push to remote with `git push origin <branch>`
- Pull changes with `git pull origin <branch>`

### Restrictions
- No direct repository creation (`git init`)
- No force pushes (`git push --force`)
- No access to `.git` directory outside of allowed operations
- No modification of git config outside of agent-controlled settings

### Example
```bash
# ✅ Allowed
git clone https://github.com/user/repo.git $HOME/.agent-data/repo
cd $HOME/.agent-data/repo && git checkout -b feature-branch
git add . && git commit -m "Update"

# ❌ Not Allowed
git init
git push --force origin main
echo "config" > .git/config
```

## GitHub Publishing Rules

### gh CLI Usage
Agents may use `gh` CLI for:
- Creating issues: `gh issue create`
- Creating pull requests: `gh pr create`
- Uploading releases: `gh release create`
- Managing repositories: `gh repo create`

### Restrictions
- No repository deletion
- No access to organization-level commands
- No direct API token management
- No access to `gh auth` or credential management

### Example
```bash
# ✅ Allowed
gh issue create --title "Bug Report" --body "Issue description"
gh pr create --title "Fix bug" --body "Fixes #123"
gh release create v1.0.0 --notes "Release notes"

# ❌ Not Allowed
gh repo delete my-repo
gh auth login
gh org list
```

## Logging and Trace Expectations

### Logging Format
All agent operations must log to `$HOME/.agent-data/logs/` with timestamped JSON format:

```json
{
  "timestamp": "2023-10-15T14:30:00Z",
  "operation": "git_checkout",
  "status": "success",
  "duration_ms": 1250,
  "details": {
    "repository": "user/repo",
    "branch": "feature-branch"
  }
}
```

### Trace Requirements
- All operations must be traceable to a unique task ID
- Operations must log start and end timestamps
- Error operations must include stack trace or error details
- All file operations must log the full path used

### Example Log Entry
```json
{
  "timestamp": "2023-10-15T14:30:00Z",
  "operation": "file_write",
  "status": "success",
  "duration_ms": 50,
  "details": {
    "path": "/home/user/.agent-data/output.json",
    "size_bytes": 1024,
    "task_id": "task-12345"
  }
}
```

### Error Handling
- All errors must be logged with status "error"
- Critical errors must be reported to monitoring system
- Failed operations must include recovery steps if applicable
- No sensitive information should appear in logs

### Example Error Log
```json
{
  "timestamp": "2023-10-15T14:30:05Z",
  "operation": "git_push",
  "status": "error",
  "duration_ms": 2000,
  "details": {
    "error": "remote rejected",
    "task_id": "task-12345",
    "retry_count": 3
  }
}
```
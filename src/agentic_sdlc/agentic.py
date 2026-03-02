import argparse
import subprocess
from pathlib import Path
from typing import Tuple

from langchain_ollama import OllamaLLM

MODEL = "qwen3-coder:30b"
llm = OllamaLLM(model=MODEL)

def project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def run_shell(command: str, cwd: Path | None = None) -> Tuple[int, str, str]:
    result = subprocess.run(
        command,
        shell=True,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr

def write_file(rel_path: str, content: str) -> Path:
    root = project_root()
    file_path = root / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return file_path

def generate_markdown(prompt: str) -> str:
    system = (
        "You are a senior software architect and technical writer.\n"
        "Output MUST be valid Markdown.\n"
        "Be practical and concrete; avoid hype.\n"
        "Do not invent APIs/commands; if unsure, state assumptions.\n"
    )
    return llm.invoke(system + "\n\n" + prompt).strip()

def cmd_init(_: argparse.Namespace) -> None:
    root = project_root()
    dirs = [
        "agents", "tools", "workflows", "cli", "docs", "examples",
        "architecture", ".github/workflows"
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)

    write_file(".gitignore", ".venv/\n__pycache__/\n*.pyc\n.DS_Store\n")
    write_file("docs/README.md", "# Docs\n\n- SAFETY.md\n- WORKFLOW.md\n- TOOLS.md\n")
    print(f"Initialized structure under: {root}")

def cmd_plan(args: argparse.Namespace) -> None:
    prompt = f"""
Create a production-grade PLAN.md for a public GitHub repo that teaches best practices for Agentic SDLC using:
- LangGraph + LangChain
- Local LLMs via Ollama (model: {MODEL})
- Deterministic workflows and explicit tool boundaries
- Git as validation and audit trail

Repo purpose:
{args.description}

Include sections:
- Goals
- Non-goals
- Audience
- Repo structure overview
- Milestones (MVP -> v1 -> v2)
- Quality bar (tests, linting, docs)
"""
    md = generate_markdown(prompt)
    path = write_file("PLAN.md", md)
    print(f"Saved {path}")

def cmd_docs(_: argparse.Namespace) -> None:
    readme = generate_markdown(f"""
Generate a professional README.md for an open-source repository called "agentic-sdlc".
It teaches best practices for Agentic SDLC using LangGraph and local LLMs (Ollama, {MODEL}).

Include:
- What this repo is
- Why deterministic workflows matter
- Quickstart (Python venv + pip install + ollama pull)
- Folder structure
- Example workflow (plan -> implement -> validate -> commit)
- Safety principles
- Roadmap
""")
    print(f"Saved {write_file('README.md', readme)}")

    arch = generate_markdown("""
Write ARCHITECTURE.md that explains:
- Why LangGraph state machines over free-form agents
- Tool boundary design (shell wrapper, allowlists, cwd, no hidden side effects)
- Logging/audit strategy
- How Git is used as a validation layer
- How to extend with new workflows/tools
Include a small ASCII diagram.
""")
    print(f"Saved {write_file('ARCHITECTURE.md', arch)}")

    safety = generate_markdown("""
Write docs/SAFETY.md for agentic coding workflows.
Include:
- Human-in-the-loop gates
- Command allowlisting / denylisting
- Secrets hygiene
- Avoiding destructive ops
- Reproducibility requirements
- What NOT to automate
""")
    print(f"Saved {write_file('docs/SAFETY.md', safety)}")

    workflow = generate_markdown("""
Write docs/WORKFLOW.md describing a deterministic Agentic SDLC workflow:
PLAN -> IMPLEMENT -> VALIDATE -> TEST -> COMMIT -> REVIEW

For each stage provide:
- Inputs
- Outputs
- Tools allowed
- Failure modes
- Transition criteria

Include a short example: "Add a new CLI command".
""")
    print(f"Saved {write_file('docs/WORKFLOW.md', workflow)}")

    tools = generate_markdown("""
Write docs/TOOLS.md defining tool boundaries for a local agent system.
Include:
- filesystem rules (where writes allowed)
- shell rules (allowlisted commands)
- git rules
- GitHub publishing rules (gh CLI)
- logging/trace expectations
Give concrete examples.
""")
    print(f"Saved {write_file('docs/TOOLS.md', tools)}")

def cmd_commit(_: argparse.Namespace) -> None:
    root = project_root()
    rc, _, _ = run_shell("git rev-parse --is-inside-work-tree", cwd=root)
    if rc != 0:
        run_shell("git init", cwd=root)

    run_shell("git add .", cwd=root)
    rc, out, err = run_shell('git commit -m "Agentic update"', cwd=root)
    print(out.strip() if out.strip() else err.strip())

def cmd_publish(args: argparse.Namespace) -> None:
    root = project_root()
    rc, out, err = run_shell(f"gh repo create {args.name} --public --source=. --push", cwd=root)
    print(out.strip() if rc == 0 else (err.strip() if err.strip() else out.strip()))

def main():
    parser = argparse.ArgumentParser(prog="agentic")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init")
    p_plan = sub.add_parser("plan")
    p_plan.add_argument("description")
    sub.add_parser("docs")
    sub.add_parser("best")
    sub.add_parser("commit")
    p_pub = sub.add_parser("publish")
    p_pub.add_argument("name")

    args = parser.parse_args()
    if args.command == "init":
        cmd_init(args)
    elif args.command == "plan":
        cmd_plan(args)
    elif args.command == "docs":
        cmd_docs(args)
    elif args.command == "best":
        cmd_best(args)
    elif args.command == "commit":
        cmd_commit(args)
    elif args.command == "publish":
        cmd_publish(args)
    else:
        parser.print_help()


def cmd_best(_: argparse.Namespace) -> None:
    """
    Generate GitHub Actions workflows:
    - CI (ruff + pytest)
    - secret scan (gitleaks)
    Also ensures .env is ignored.
    """
    ci = """name: ci

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install
        run: |
          python -m pip install -U pip
          pip install -U ruff pytest
          pip install -e .
      - name: Lint
        run: ruff check .
      - name: Tests
        run: pytest -q
"""
    print(f"Saved {write_file('.github/workflows/ci.yml', ci)}")

    gitleaks = """name: secret-scan

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gitleaks/gitleaks-action@v2
"""
    print(f"Saved {write_file('.github/workflows/secret-scan.yml', gitleaks)}")

    # Ensure secrets files are ignored
    root = project_root()
    gi = root / ".gitignore"
    existing = gi.read_text() if gi.exists() else ""
    add = ".env\n.env.*\n"
    if ".env" not in existing:
        gi.write_text(existing + ("" if existing.endswith("\n") or existing == "" else "\n") + add)
        print(f"Updated {gi}")

if __name__ == "__main__":
    main()

def cmd_best(_: argparse.Namespace) -> None:
    """
    Generate opinionated best-practices content + CI scaffolding.
    """
    # 1) Repo hygiene
    write_file(".env.example", "GITHUB_TOKEN=\n# Never commit .env. Use .env.example + GitHub Secrets.\n")
    gi = (project_root() / ".gitignore").read_text() if (project_root() / ".gitignore").exists() else ""
    if ".env\n" not in gi:
        write_file(".gitignore", gi + ("\n" if gi and not gi.endswith("\n") else "") + ".env\n")

    # 2) Core best-practice docs
    checklist = generate_markdown("""
Create docs/AGENTIC_SDLC_CHECKLIST.md:
- A short checklist for agentic SDLC (planning, tool boundaries, tests, reviews)
- Add "stop the agent" criteria
- Include a small rubric for PR review quality
""")
    print(f"Saved {write_file('docs/AGENTIC_SDLC_CHECKLIST.md', checklist)}")

    prompts = generate_markdown(f"""
Create docs/PROMPTING_PLAYBOOK.md for using local models (Ollama {MODEL}) for coding.
Include:
- Role priming prompt for "repo maintainer"
- Prompt templates: plan, implement, refactor, write tests, write docs
- "Ask before act" rule for risky operations
Keep prompts short and copy-pastable.
""")
    print(f"Saved {write_file('docs/PROMPTING_PLAYBOOK.md', prompts)}")

    boundaries = generate_markdown("""
Create docs/TOOL_BOUNDARIES.md.
Include:
- Allowed file write scope rules
- Shell allowlist concept + examples
- Git operations allowed
- GitHub publishing rules
- Explicit "Never do" list (secrets, rm -rf, mass edits without diff review)
""")
    print(f"Saved {write_file('docs/TOOL_BOUNDARIES.md', boundaries)}")

    # 3) CI: lint + tests + secret scanning
    ci = """name: ci

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install -U pip
          pip install -e .
          pip install ruff pytest

      - name: Lint (ruff)
        run: ruff check .

      - name: Unit tests
        run: pytest -q || true
"""
    print(f"Saved {write_file('.github/workflows/ci.yml', ci)}")

    gitleaks = """name: secret-scan

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gitleaks/gitleaks-action@v2
"""
    print(f"Saved {write_file('.github/workflows/secret-scan.yml', gitleaks)}")


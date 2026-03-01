import argparse
import subprocess
from pathlib import Path
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen3-coder:30b")


def run_shell(command: str):
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    return result.stdout + result.stderr


def generate_file(filename: str, prompt: str):
    print(f"Generating {filename}...")
    response = llm.invoke(prompt)

    # Always save in project root (one level above cli/)
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / filename

    file_path.write_text(response)
    print(f"Saved {file_path}")


def plan_repo(description: str):
    prompt = f"""
    You are a senior AI systems architect.

    Create a production-grade repository plan for:
    {description}

    Output structured markdown.
    """
    generate_file("README.md", prompt)


def commit_all():
    run_shell("git add .")
    run_shell('git commit -m "Agentic update"')
    print("Committed changes.")


def publish_repo(name: str):
    run_shell(f"gh repo create {name} --public --source=. --push")
    print("Published to GitHub.")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("description")

    subparsers.add_parser("commit")

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("name")

    args = parser.parse_args()

    if args.command == "plan":
        plan_repo(args.description)
    elif args.command == "commit":
        commit_all()
    elif args.command == "publish":
        publish_repo(args.name)
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()

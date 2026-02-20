# agents/fetcher.py
from tools.github_tools import parse_repo_url, get_repo_info, get_repo_tree, get_file_content
from rag.code_store import build_code_index
from config import MAX_FILE_SIZE

def fetcher_agent(state: dict) -> dict:
    print("\n[FETCHER] Fetching repository files from GitHub...")

    repo_url          = state["pr_url"]
    owner, repo       = parse_repo_url(repo_url)
    repo_info         = get_repo_info(owner, repo)

    print(f"Repo: {repo_info['name']} | ⭐ {repo_info['stars']} stars")
    print(f"Language: {repo_info['language']}")
    print(f"{repo_info['description']}")

    # Get all file paths from all folders
    all_paths = get_repo_tree(owner, repo, repo_info["default_branch"])
    print(f"\nLoading {len(all_paths)} code files...")

    # Load all files
    files = []
    for path in all_paths:
        content = get_file_content(owner, repo, path)
        if content.strip():
            files.append({
                "filename":  path,
                "status":    "existing",
                "additions": content.count("\n"),
                "deletions": 0,
                "content":   content[:MAX_FILE_SIZE],
                "patch":     ""
            })

    print(f"[FETCHER] Loaded {len(files)} files")

    #Build RAG index from all files
    vectorstore = build_code_index(files, owner, repo)

    pr_info = {
        "title":         f"Repository Review: {repo_info['name']}",
        "description":   repo_info["description"],
        "author":        repo_info["owner"],
        "base_branch":   repo_info["default_branch"],
        "head_branch":   repo_info["default_branch"],
        "changed_files": len(files),
        "additions":     sum(f["additions"] for f in files),
        "deletions":     0,
        "state":         "open"
    }

    return {
        **state,
        "pr_info":     pr_info,
        "files":       files,
        "owner":       owner,
        "repo":        repo,
        "pr_number":   0,
        "repo_info":   repo_info,
        "vectorstore": vectorstore
    }

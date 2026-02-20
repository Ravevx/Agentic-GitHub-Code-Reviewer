# tools/github_tools.py
import requests
import re
import base64
from config import GITHUB_TOKEN

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

#update CODE_EXTENSIONS as per requirements
CODE_EXTENSIONS = {
    ".py",
}


def parse_repo_url(url: str) -> tuple[str, str]:
    pattern = r"github\.com/([^/]+)/([^/\s]+)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f"❌ Invalid GitHub URL: {url}")
    owner = match.group(1)
    repo  = match.group(2).rstrip("/").split("/")[0]
    return owner, repo

def get_repo_info(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return {
        "name":           data["name"],
        "description":    data.get("description") or "No description.",
        "language":       data.get("language") or "Unknown",
        "stars":          data["stargazers_count"],
        "forks":          data["forks_count"],
        "default_branch": data["default_branch"],
        "owner":          data["owner"]["login"]
    }

def get_repo_tree(owner: str, repo: str, branch: str = "main") -> list[str]:
    """Get ALL file paths recursively across ALL folders."""
    for b in [branch, "main", "master"]:
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{b}?recursive=1"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            tree = response.json().get("tree", [])
            
            # Debug print everything found
            print(f"\n   🌳 Raw tree has {len(tree)} total items")
            
            filtered = []
            for item in tree:
                if item["type"] != "blob":
                    continue
                path = item["path"]
                ext  = "." + path.split(".")[-1] if "." in path else ""
                size = item.get("size", 0)
                
                if ext in CODE_EXTENSIONS and size < 200000:
                    filtered.append(path)
                    print(f"      ✅ {path}  ({size} bytes)")
                else:
                    print(f"      ⏭️  skipped: {path}  ext={ext}")

            return filtered
    return []

def get_file_content(owner: str, repo: str, filepath: str) -> str:
    """Fetch content of a single file via GitHub contents API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f" Failed to load: {filepath} ({response.status_code})")
        return ""
    data = response.json()
    try:
        content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        print(f" Loaded {len(content)} chars: {filepath}")
        return content
    except Exception as e:
        print(f" Decode error {filepath}: {e}")
        return ""

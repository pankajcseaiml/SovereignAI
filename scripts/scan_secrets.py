"""
SovereignAI — Pre-Commit & Pre-Push Enterprise Secret Scanner
Scans source files, staged files, and git history for accidentally exposed credentials.
Rule 2 Enforced: Never prints or exposes secret values. Reports only location and status.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

# Patterns that indicate secrets
SECRET_PATTERNS = [
    (r"-----BEGIN (?:RSA|EC|DSA|OPENSSH|PGP|ENCRYPTED|PRIVATE) KEY", "Private Key Header"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key Pattern"),
    (r"gh[pousr]_[A-Za-z0-9_]{36,}", "GitHub Token Pattern"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,48}", "Slack Token Pattern"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key Pattern"),
    (r"(?:sk-[a-zA-Z0-9]{20,})", "OpenAI / Anthropic Secret Key"),
    (r"(?:postgres(?:ql)?:\/\/[a-zA-Z0-9_]+:[a-zA-Z0-9_!@#$%^&*()+=]+@[a-zA-Z0-9.-]+)", "Database URL with embedded credentials"),
]

# Sensitive files that must NEVER be tracked by Git
FORBIDDEN_FILE_PATTERNS = [
    r"^\.env$",
    r"^\.env\.local$",
    r"^\.env\.production$",
    r".*\.kdbx$",
    r".*\.pem$",
    r".*\.key$",
    r".*\.p12$",
    r".*\.pfx$",
    r".*rclone\.conf$",
]

EXCLUDED_PATHS = [
    ".git",
    "venv",
    ".venv",
    "backend/venv",
    "node_modules",
    "frontend/node_modules",
    "frontend/.next",
    "__pycache__",
    ".pytest_cache",
    ".env.example",  # Allowed template
    "backups",
]


def is_git_ignored(path: Path) -> bool:
    """Checks if a path is ignored by git."""
    try:
        res = subprocess.run(["git", "check-ignore", "-q", str(path)], check=False)
        return res.returncode == 0
    except Exception:
        return False


def is_excluded(path: Path) -> bool:
    path_str = str(path).replace("\\", "/")
    for exc in EXCLUDED_PATHS:
        parts = path_str.split("/")
        if exc in parts:
            return True
        if path_str.startswith(exc):
            return True
    return False


def scan_file(file_path: Path) -> List[Tuple[str, int, str]]:
    """Scans a single file for secret patterns. Returns list of (file, line_no, pattern_desc)."""
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                if file_path.name == ".env.example":
                    continue
                for pattern, desc in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        findings.append((str(file_path), line_no, desc))
    except Exception:
        pass
    return findings


def scan_workspace_git_scope() -> List[Tuple[str, int, str]]:
    """Scans all non-ignored files that could potentially be committed."""
    findings = []
    root = Path(".")
    for p in root.rglob("*"):
        if p.is_file() and not is_excluded(p):
            # If the file is git-ignored, it won't be pushed to git
            if is_git_ignored(p):
                continue
            # Check forbidden filenames
            for forbidden_re in FORBIDDEN_FILE_PATTERNS:
                if re.match(forbidden_re, p.name, re.IGNORECASE):
                    findings.append((str(p), 0, f"Forbidden sensitive file detected: {p.name}"))
            # Check content
            findings.extend(scan_file(p))
    return findings


def scan_git_history_and_index() -> List[str]:
    """Scans git index and commit history for committed secrets."""
    findings = []
    try:
        res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                             capture_output=True, text=True, check=False)
        if res.returncode != 0:
            return []  # Not a git repo yet

        # Check git tracked files
        res_ls = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=False)
        if res_ls.returncode == 0:
            for f in res_ls.stdout.splitlines():
                f_name = Path(f).name
                for forbidden_re in FORBIDDEN_FILE_PATTERNS:
                    if re.match(forbidden_re, f_name, re.IGNORECASE):
                        findings.append(f"Git-tracked forbidden file: {f}")

        # Scan commit diffs
        res_log = subprocess.run(["git", "log", "-p", "--all", "-n", "50"],
                                capture_output=True, text=True, check=False)
        if res_log.returncode == 0:
            for line in res_log.stdout.splitlines():
                if line.startswith("+") and not line.startswith("+++"):
                    for pattern, desc in SECRET_PATTERNS:
                        if re.search(pattern, line[1:]):
                            findings.append(f"Historical commit secret leak: {desc}")
    except Exception:
        pass
    return findings


def main():
    print("========================================================")
    print("  SovereignAI — Enterprise Pre-Commit Secret Scanner   ")
    print("========================================================")
    print("[*] Scanning workspace files and configurations in Git scope...")

    findings = scan_workspace_git_scope()
    history_findings = scan_git_history_and_index()

    total_issues = len(findings) + len(history_findings)

    if total_issues == 0:
        print("\n[SUCCESS] 0 secrets detected! Workspace is safe for Git commit.")
        print("========================================================")
        sys.exit(0)
    else:
        print(f"\n[SECURITY ALERT] {total_issues} potential secret exposure(s) detected!\n", file=sys.stderr)
        for fpath, lno, desc in findings:
            loc = f"Line {lno}" if lno > 0 else "File Pattern"
            print(f"  [!] {fpath} ({loc}): {desc}", file=sys.stderr)
        for h in history_findings:
            print(f"  [!] {h}", file=sys.stderr)
        print("\n[BLOCKED] Commit or push cannot proceed until secrets are removed.", file=sys.stderr)
        print("========================================================", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

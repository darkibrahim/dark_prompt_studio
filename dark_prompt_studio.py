#!/usr/bin/env python3
"""
DARK PROMPT STUDIO v1.0
Author  : DARK IBRAHIM (Md Ibrahim)
GitHub  : https://github.com/darkibrahim
Purpose : Prompt-to-Code GitHub-Ready Project & ZIP Generator
"""

import argparse
import json
import os
import re
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path

# ANSI Colors (Works cleanly in Termux & Linux without external libraries)
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""{CYAN}{BOLD}
██████╗  █████╗ ██████╗ ██╗  ██╗    ██╗██████╗ ██████╗  █████╗ ██╗  ██╗██╗███╗   ███╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██║██╔══██╗██╔══██╗██╔══██╗██║  ██║██║████╗ ████║
██║  ██║███████║██████╔╝█████╔╝     ██║██████╔╝██████╔╝███████║███████║██║██╔████╔██║
██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║██╔══██╗██╔══██╗██╔══██║██╔══██║██║██║╚██╔╝██║
██████╔╝██║  ██║██║  ██║██║  ██╗    ██║██████╔╝██║  ██║██║  ██║██║  ██║██║██║ ╚═╝ ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝
{RESET}{MAGENTA}======================================================================================{RESET}
  {WHITE}{BOLD}TOOL   :{RESET} {GREEN}DARK PROMPT STUDIO v1.0 (Prompt-to-Code & GitHub ZIP Builder){RESET}
  {WHITE}{BOLD}AUTHOR :{RESET} {CYAN}DARK IBRAHIM (Md Ibrahim){RESET}
  {WHITE}{BOLD}GITHUB :{RESET} {YELLOW}https://github.com/darkibrahim{RESET}
{MAGENTA}======================================================================================{RESET}
"""


def show_banner(animate: bool = True) -> None:
    if not animate:
        print(BANNER)
        return
    for line in BANNER.splitlines():
        print(line)
        time.sleep(0.025)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9\s_-]", "", text.lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-")[:42] or "dark-ibrahim-project"


def build_project_spec(prompt: str) -> dict:
    name = slugify(prompt)
    title = name.replace("-", " ").title()
    py_name = f"{name.replace('-', '_')}.py"
    now = datetime.now().strftime("%Y-%m-%d")

    web_keywords = [
        "html", "css", "web", "dashboard", "portal",
        "todo", "to-do", "ui", "landing", "site", "page"
    ]
    is_web = any(k in prompt.lower() for k in web_keywords)

    if is_web:
        files = {
            "index.html": f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | DARK IBRAHIM</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="app">
    <header>
      <span class="badge">DARK IBRAHIM EDITION</span>
      <h1>{title}</h1>
      <p>{prompt}</p>
    </header>
    <main class="panel">
      <div class="controls">
        <input id="taskInput" type="text" placeholder="Enter item or command..." />
        <button id="addBtn" type="button">Add</button>
      </div>
      <ul id="outputList"></ul>
    </main>
    <footer>Built with DARK PROMPT STUDIO • github.com/darkibrahim</footer>
  </div>
  <script src="app.js"></script>
</body>
</html>
""",
            "style.css": """* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  background: #0d1117;
  color: #e6edf3;
  padding: 20px;
}
.app { max-width: 720px; margin: 0 auto; }
.badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #58a6ff;
  background: rgba(88, 166, 255, 0.14);
  border: 1px solid rgba(88, 166, 255, 0.4);
  padding: 3px 10px;
  border-radius: 999px;
  margin-bottom: 8px;
}
h1 { margin: 0 0 6px; color: #58a6ff; }
p { margin: 0 0 18px; color: #8b949e; }
.panel {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 10px;
  padding: 16px;
}
.controls { display: flex; gap: 8px; }
input {
  flex: 1;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #30363d;
  background: #0d1117;
  color: #e6edf3;
}
button {
  padding: 10px 14px;
  border-radius: 8px;
  border: none;
  background: #58a6ff;
  color: #0d1117;
  font-weight: 600;
  cursor: pointer;
}
ul { list-style: none; padding: 0; margin: 16px 0 0; }
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #21262d;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 8px;
}
footer {
  margin-top: 18px;
  text-align: center;
  font-size: 0.8rem;
  color: #8b949e;
}
""",
            "app.js": """const input = document.getElementById("taskInput");
const addBtn = document.getElementById("addBtn");
const list = document.getElementById("outputList");

function addEntry() {
  const val = input.value.trim();
  if (!val) return;
  const li = document.createElement("li");
  const span = document.createElement("span");
  span.textContent = val;
  const btn = document.createElement("button");
  btn.textContent = "Delete";
  btn.onclick = () => li.remove();
  li.append(span, btn);
  list.appendChild(li);
  input.value = "";
  input.focus();
}

addBtn.addEventListener("click", addEntry);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") addEntry();
});
""",
        }
        run_cmd = 'termux-open-url "file://$(pwd)/index.html" 2>/dev/null || python3 -m http.server 8080'
    else:
        files = {
            py_name: f"""#!/usr/bin/env python3
\"\"\"
{title}
Author  : DARK IBRAHIM (Md Ibrahim)
GitHub  : https://github.com/darkibrahim
Prompt  : {prompt}
Date    : {now}
\"\"\"

import argparse
import json
import sys
from datetime import datetime

CYAN = "\033[96m"
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""{{CYAN}}{{BOLD}}
==================================================
  {title.upper()}
  Author : DARK IBRAHIM | github.com/darkibrahim
=================================================={{RESET}}
"""


def execute(target: str | None = None, verbose: bool = False) -> dict:
    if verbose:
        print(f"{{GREEN}}[*] Executing {title} -> target: {{target or 'default'}}{{RESET}}")
    return {{
        "project": "{name}",
        "author": "DARK IBRAHIM",
        "prompt": {json.dumps(prompt)},
        "target": target or "default",
        "generated_at": datetime.now().isoformat(),
        "status": "completed",
    }}


def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description={json.dumps(title)})
    parser.add_argument("-t", "--target", help="Target input or host")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-o", "--save", help="Save JSON report to file")
    args = parser.parse_args()

    result = execute(target=args.target, verbose=args.verbose)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"{{GREEN}}[+] Report saved to {{args.save}}{{RESET}}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(1)
""",
        }
        run_cmd = f'python3 "{py_name}" "$@"'

    file_bullets = "\n".join(f"- `{fname}`" for fname in files.keys())
    files["README.md"] = f"""# {title}

> {prompt}

**Author:** DARK IBRAHIM (Md Ibrahim)  
**GitHub:** [darkibrahim](https://github.com/darkibrahim)

## Included Files
{file_bullets}
- `install.sh` — Setup & permission helper
- `run.sh` — Quick launcher script
- `.gitignore` — Clean Git rules

## Quick Start (Termux / Linux)
```bash
bash install.sh
bash run.sh
```
"""

    files["install.sh"] = f"""#!/usr/bin/env bash
set -e
echo "[*] Setting up {title} by DARK IBRAHIM..."
chmod +x run.sh
echo "[+] Installation complete! Start with: bash run.sh"
"""

    files["run.sh"] = f"""#!/usr/bin/env bash
set -e
{run_cmd}
"""

    files[".gitignore"] = """__pycache__/
*.py[cod]
*.log
.env
.DS_Store
"""

    return {"name": name, "files": files}


def create_github_bundle(prompt: str, out_root: str = "output_projects") -> tuple[Path, Path]:
    spec = build_project_spec(prompt)
    project_name = spec["name"]
    files = spec["files"]

    base_dir = Path(out_root)
    project_dir = base_dir / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    for rel_name, content in files.items():
        fpath = project_dir / rel_name
        fpath.parent.mkdir(parents=True, exist_ok=True)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content if content.endswith("\n") else content + "\n")
        if rel_name.endswith(".sh") or rel_name.endswith(".py"):
            os.chmod(fpath, 0o755)

    zip_path = base_dir / f"{project_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(project_dir.rglob("*")):
            if file_path.is_file():
                arcname = Path(project_name) / file_path.relative_to(project_dir)
                zf.write(file_path, arcname.as_posix())

    return project_dir, zip_path


def main():
    parser = argparse.ArgumentParser(
        description="DARK PROMPT STUDIO — Prompt-to-Code & GitHub ZIP Generator by DARK IBRAHIM"
    )
    parser.add_argument("prompt", nargs="*", help="Project prompt (leave blank for interactive mode)")
    parser.add_argument("-o", "--out", default="output_projects", help="Output folder")
    parser.add_argument("--no-anim", action="store_true", help="Disable banner typing animation")
    args = parser.parse_args()

    show_banner(animate=not args.no_anim)

    if args.prompt:
        prompt_text = " ".join(args.prompt).strip()
    else:
        prompt_text = input(f"{CYAN}[?] Enter your project prompt:{RESET} ").strip()

    if not prompt_text:
        print(f"{YELLOW}[!] Error: Prompt cannot be empty.{RESET}", file=sys.stderr)
        sys.exit(1)

    folder, zip_file = create_github_bundle(prompt_text, out_root=args.out)

    print(f"\n{GREEN}{BOLD}[+] GitHub Project Bundle Ready!{RESET}")
    print(f"    {WHITE}Folder :{RESET} {folder.resolve()}")
    print(f"    {WHITE}ZIP    :{RESET} {zip_file.resolve()}")
    print(f"\n{CYAN}[*] Generated Files:{RESET}")
    for item in sorted(folder.rglob("*")):
        if item.is_file():
            print(f"    - {item.name}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Exited by user.")
        sys.exit(0)

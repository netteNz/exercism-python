import os
import sys
import json
import shlex
import difflib
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Tuple

WORKSPACE = Path.cwd().resolve()  # run from Exercism java track root

AGENT_DIR = WORKSPACE / "_agent"
NOTES_DIR = WORKSPACE / "_notes"
REVIEWS_DIR = WORKSPACE / "_reviews"

RULES_PATH = AGENT_DIR / "AGENT_RULES.md"

DEFAULT_COPILOT_CMD = os.environ.get("COPILOT_CMD", "").strip()
DEFAULT_COPILOT_FLAGS = os.environ.get("COPILOT_FLAGS", "").strip()

# --------- safety: sandbox paths ---------
def safe_path(rel: str) -> Path:
    p = (WORKSPACE / rel).resolve()
    if not str(p).startswith(str(WORKSPACE)):
        raise ValueError("Refusing to access outside the Exercism track directory.")
    return p

def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")

def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# --------- exercism helpers ---------
def list_exercises() -> List[str]:
    """
    Detect Exercism Java exercises in common layouts, including:
      - <track_root>/<exercise-slug>/
      - <track_root>/exercises/practice/<exercise-slug>/
      - <track_root>/exercises/concept/<exercise-slug>/
      - <track_root>/exercises/*/<exercise-slug>/
      - <track_root>/.../practice/<exercise-slug>/ (nested)
    We return slugs as relative paths from WORKSPACE so commands can use them.
    """
    candidates = []

    # Common explicit folders
    search_roots = [
        WORKSPACE,
        WORKSPACE / "exercises",
        WORKSPACE / "exercises" / "practice",
        WORKSPACE / "exercises" / "concept",
    ]

    # Add any existing search roots
    actual_roots = [p for p in search_roots if p.exists()]

    # Also search deeper, but not infinitely
    for root in actual_roots:
        for p in root.rglob("*"):
            if not p.is_dir():
                continue
            if p.name.startswith("_") or p.name.startswith("."):
                continue

            # Heuristic: an exercise directory has src/main/java or src/test/java or README.md
            if (p / "src" / "main" / "java").exists() or (p / "src" / "test" / "java").exists() or (p / "README.md").exists():
                rel = p.relative_to(WORKSPACE)
                candidates.append(str(rel))

    # Deduplicate and keep only "leaf-most" dirs (avoid listing parent folders)
    candidates = sorted(set(candidates))

    # Filter out obvious non-exercise dirs
    bad = {"_agent", "_notes", "_reviews"}
    filtered = []
    for rel in candidates:
        parts = Path(rel).parts
        if parts and parts[0] in bad:
            continue
        filtered.append(rel)

    return filtered


def exercise_paths(slug: str) -> Dict[str, List[Path]]:
    slug = resolve_exercise_slug(slug)
    ex = safe_path(slug)
    if not ex.exists() or not ex.is_dir():
        raise FileNotFoundError(f"Exercise folder not found: {slug}")

    readme = ex / "README.md"
    tests_dir = ex / "src" / "test" / "java"
    main_dir = ex / "src" / "main" / "java"

    tests = list(tests_dir.rglob("*.java")) if tests_dir.exists() else []
    mains = list(main_dir.rglob("*.java")) if main_dir.exists() else []

    return {
        "readme": [readme] if readme.exists() else [],
        "tests": sorted(tests),
        "mains": sorted(mains),
    }

def load_rules() -> str:
    return read_text(RULES_PATH)

# --------- copilot runner ---------
def run_copilot(prompt: str) -> str:
    """
    Uses GitHub Copilot CLI in non-interactive prompt mode:
      copilot -p "<prompt>" -s --no-color --stream off --add-dir "<workspace>"
    """
    if not DEFAULT_COPILOT_CMD:
        raise RuntimeError(
            'COPILOT_CMD is not set. Run:\n'
            '  setx COPILOT_CMD "copilot"\n'
            '  setx COPILOT_FLAGS "-s --no-color --stream off"\n'
            'Then open a new terminal.'
        )

    cmd = shlex.split(DEFAULT_COPILOT_CMD)

    # Non-interactive prompt mode
    cmd += ["-p", prompt]

    # Script-friendly flags
    if DEFAULT_COPILOT_FLAGS:
        cmd += shlex.split(DEFAULT_COPILOT_FLAGS)

    # Restrict Copilot file access to this Exercism track directory
    cmd += ["--add-dir", str(WORKSPACE)]

    proc = subprocess.run(
        cmd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        shell=False
    )

    if proc.returncode != 0:
        err = proc.stderr.strip() or "(no stderr)"
        raise RuntimeError(f"Copilot CLI failed (exit {proc.returncode}):\n{err}")

    return (proc.stdout or "").strip()


# --------- prompt builders ---------
def format_file_block(path: Path, max_chars: int = 8000) -> str:
    text = read_text(path)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... (truncated)"
    rel = path.relative_to(WORKSPACE)
    return f"\n\n---\nFILE: {rel}\n---\n{text}\n"

def build_context(slug: str) -> Tuple[str, Dict[str, List[Path]]]:
    rules = load_rules()
    paths = exercise_paths(slug)

    parts = []
    if rules:
        parts.append(f"RULES:\n{rules}\n")

    if paths["readme"]:
        parts.append(format_file_block(paths["readme"][0], max_chars=6000))

    # Tests are key
    for t in paths["tests"][:6]:  # cap a bit
        parts.append(format_file_block(t, max_chars=7000))

    # Your solution, if exists
    for m in paths["mains"][:4]:
        parts.append(format_file_block(m, max_chars=7000))

    context = "\n".join(parts).strip()
    return context, paths

def prompt_explain(slug: str, context: str) -> str:
    return f"""
You are a DSA + Java tutor helping me with Exercism (Java track).
Exercise: {slug}

Use the README + tests to infer requirements.
Explain:
- What the exercise wants
- What the tests are enforcing
- Key Java concepts / DSA pattern (if any)
- Edge cases
- Complexity
- 3 practice variations

Also include a short "Python -> Java mapping" section relevant to this exercise (syntax + patterns).

Do NOT give a full final solution unless I explicitly ask for it.
Prefer hint ladder + pseudocode + small targeted snippets.

CONTEXT:
{context}
""".strip()

def prompt_hint(slug: str, context: str) -> str:
    return f"""
You are a tutor. Provide a 3-level hint ladder for Exercism Java exercise: {slug}
- Hint 1: approach and pattern
- Hint 2: edge cases and pitfalls
- Hint 3: pseudocode + minimal snippet skeleton (NOT a full working solution)

Include complexity notes and "Python -> Java mapping" relevant to the approach.

Do NOT provide a complete solution.

CONTEXT:
{context}
""".strip()

def prompt_review(slug: str, context: str) -> str:
    return f"""
You are reviewing my Java solution for Exercism exercise: {slug}

Check:
- Correctness vs tests
- Style and readability
- Complexity
- Java best practices (immutability, naming, exceptions, streams vs loops)
- Provide a revised snippet ONLY for problematic parts (avoid full rewrite unless necessary)

End with:
- 3 focused improvement tasks for me
- 3 quick quiz questions
- A short "Python -> Java mapping" focused on what I did in code

CONTEXT:
{context}
""".strip()

def prompt_syntax(topic: str, context: str) -> str:
    return f"""
Create a concise but useful "Python vs Java" cheat-sheet for the topic/exercise: {topic}

Include:
- Syntax equivalents (variables, loops, conditionals, functions/methods, classes)
- Common DSA constructs: list/array, dict/map, set, stack/queue, sorting, iterating
- Pitfalls: mutability, pass-by-value semantics, integer overflow, char/string differences
- Tiny examples in BOTH languages (short!)

If context indicates an Exercism exercise, tailor the examples to it.

CONTEXT (if any):
{context}
""".strip()

# --------- commands ---------
def cmd_explain(slug: str) -> None:
    context, _ = build_context(slug)
    out = run_copilot(prompt_explain(slug, context))
    write_text(NOTES_DIR / "exercises" / f"{slug}.md", out)
    print(f"Wrote: _notes/exercises/{slug}.md")

def cmd_hint(slug: str) -> None:
    context, _ = build_context(slug)
    out = run_copilot(prompt_hint(slug, context))
    write_text(NOTES_DIR / "exercises" / f"{slug}_hints.md", out)
    print(f"Wrote: _notes/exercises/{slug}_hints.md")

def cmd_review(slug: str) -> None:
    context, paths = build_context(slug)
    if not paths["mains"]:
        print("No solution file found yet under src/main/java. Solve first, then review.")
        return
    out = run_copilot(prompt_review(slug, context))
    write_text(REVIEWS_DIR / f"{slug}.md", out)
    print(f"Wrote: _reviews/{slug}.md")

def cmd_syntax(topic_or_slug: str) -> None:
    # If it's an exercise folder, include its context; else just do generic
    context = ""
    ex_path = WORKSPACE / topic_or_slug
    if ex_path.exists() and ex_path.is_dir():
        context, _ = build_context(topic_or_slug)
    out = run_copilot(prompt_syntax(topic_or_slug, context))
    write_text(NOTES_DIR / "syntax" / f"{topic_or_slug}.md", out)
    print(f"Wrote: _notes/syntax/{topic_or_slug}.md")

def cmd_status() -> None:
    exs = list_exercises()
    print(f"Track root: {WORKSPACE}")
    print(f"Exercises detected: {len(exs)}\n")

    if len(exs) == 0:
        print("No exercises found. Check where Exercism downloads exercises.")
        return

    # Print up to 80 paths so you can see structure
    for rel in exs[:80]:
        main_dir = WORKSPACE / rel / "src" / "main" / "java"
        solved = main_dir.exists() and any(main_dir.rglob("*.java"))
        print(f"{'[x]' if solved else '[ ]'} {rel}")

    if len(exs) > 80:
        print(f"... (+{len(exs)-80} more)")
        

def resolve_exercise_slug(slug: str) -> str:
    # direct hit
    p = WORKSPACE / slug
    if p.exists() and p.is_dir():
        return slug

    # try case-insensitive match
    exs = list_exercises()
    for e in exs:
        if e.lower() == slug.lower():
            return e

    # suggest closest
    close = difflib.get_close_matches(slug, exs, n=1, cutoff=0.6)
    if close:
        raise FileNotFoundError(f"Exercise folder not found: {slug}\nDid you mean: {close[0]} ?")

    raise FileNotFoundError(f"Exercise folder not found: {slug}")



def main():
    """
    Usage (run from Exercism java track root):
      python agent.py status
      python agent.py explain <exercise-slug>
      python agent.py hint <exercise-slug>
      python agent.py review <exercise-slug>
      python agent.py syntax <exercise-slug|topic>

    Environment:
      COPILOT_CMD   e.g. "gh copilot suggest"  OR "copilot"
      COPILOT_FLAGS optional extra flags
    """
    if len(sys.argv) < 2:
        print(main.__doc__)
        return

    cmd = sys.argv[1].lower()

    # Ensure dirs exist
    (AGENT_DIR).mkdir(parents=True, exist_ok=True)
    (NOTES_DIR / "exercises").mkdir(parents=True, exist_ok=True)
    (NOTES_DIR / "syntax").mkdir(parents=True, exist_ok=True)
    (REVIEWS_DIR).mkdir(parents=True, exist_ok=True)

    if cmd == "status":
        cmd_status()
    elif cmd in ("explain", "hint", "review", "syntax"):
        if len(sys.argv) < 3:
            print("Missing argument.\n")
            print(main.__doc__)
            return
        arg = " ".join(sys.argv[2:]).strip()
        if cmd == "explain":
            cmd_explain(arg)
        elif cmd == "hint":
            cmd_hint(arg)
        elif cmd == "review":
            cmd_review(arg)
        elif cmd == "syntax":
            cmd_syntax(arg)
    else:
        print("Unknown command.\n")
        print(main.__doc__)

if __name__ == "__main__":
    main()

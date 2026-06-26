#!/usr/bin/env python3
"""
Validate water-engineering skill structure and content.
Checks: file existence, markdown syntax, broken references, version consistency.
"""
import os, re, sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = 0
warnings = 0

def check(cond, msg, level="error"):
    global errors, warnings
    if not cond:
        if level == "error":
            errors += 1
            print(f"  ERROR: {msg}")
        else:
            warnings += 1
            print(f"  WARN:  {msg}")

def main():
    global errors, warnings
    print(f"Validating water-engineering skill in: {SKILL_DIR}")

    # 1. Required files exist
    required = ["skill.md", "README.md", "CHANGELOG.md", "VERSION", "LICENSE"]
    for f in required:
        check(os.path.exists(os.path.join(SKILL_DIR, f)), f"Missing required file: {f}")

    required_refs = [
        "references/report-templates.md", "references/structural-engineering.md",
        "references/hydropower-irrigation.md", "references/software.md",
        "references/external-tools.md", "references/projects.md",
        "references/groundwater.md", "references/landlab.md",
    ]
    for f in required_refs:
        check(os.path.exists(os.path.join(SKILL_DIR, f)), f"Missing reference: {f}")

    # 2. VERSION format
    version_file = os.path.join(SKILL_DIR, "VERSION")
    if os.path.exists(version_file):
        with open(version_file) as f:
            v = f.read().strip()
        check(re.match(r'^\d+\.\d+\.\d+$', v), f"VERSION format invalid: {v}")
        print(f"  Version: {v}")

    # 3. skill.md frontmatter
    skill_file = os.path.join(SKILL_DIR, "skill.md")
    if os.path.exists(skill_file):
        with open(skill_file, encoding='utf-8') as f:
            content = f.read()
        check(content.startswith('---'), "skill.md missing frontmatter (---)")
        check('name: water-engineering' in content, "skill.md missing name field")
        check('description:' in content, "skill.md missing description field")
        # Count sections
        sections = len(re.findall(r'^##\s+\d', content, re.MULTILINE))
        print(f"  skill.md sections: {sections}")
        lines = content.count('\n') + 1
        print(f"  skill.md lines: {lines}")

    # 4. CHANGELOG format
    changelog = os.path.join(SKILL_DIR, "CHANGELOG.md")
    if os.path.exists(changelog):
        with open(changelog) as f:
            content = f.read()
        check('[1.0.0]' in content, "CHANGELOG missing [1.0.0] entry")

    # 5. Reference file sizes
    ref_dir = os.path.join(SKILL_DIR, "references")
    if os.path.exists(ref_dir):
        for f in os.listdir(ref_dir):
            path = os.path.join(ref_dir, f)
            sz = os.path.getsize(path)
            check(sz > 100, f"Reference file too small: {f} ({sz} bytes)", "warn")

    print(f"\n{'='*40}")
    print(f"  {errors} errors, {warnings} warnings")
    return 1 if errors > 0 else 0

if __name__ == "__main__":
    sys.exit(main())

import re
import sys

from utils.config_loader import load_config
from utils.command_runner import run_command
from utils.version_compare import compare_versions
from utils.prompt import prompt_yes_no

def run_requirements_check(config_path="config.json"):
    """
    1. Loads 'config.json'
    2. For each requirement, checks if installed & correct version
    3. Prompts user to install/upgrade if missing or mismatched
    """
    config = load_config(config_path)
    requirements = config.get("requirements", [])
    if not requirements:
        print("[INFO] No requirements found in config.json.")
        return

    for req in requirements:
        check_requirement(req)

def check_requirement(req):
    """
    Checks a single requirement:
      - name
      - check_command
      - version_regex
      - required_version
      - install_instructions
      - upgrade_instructions
    """
    name = req.get("name")
    check_command = req.get("check_command")
    version_regex = req.get("version_regex")
    required_version_str = req.get("required_version")
    install_instructions = req.get("install_instructions", "No instructions provided.")
    upgrade_instructions = req.get("upgrade_instructions", "No instructions provided.")

    print(f"\n=== Checking requirement: {name} ===")

    if not name or not check_command or not version_regex or not required_version_str:
        print(f"[WARN] Incomplete requirement definition for '{name}'. Skipping.")
        return

    # 1) Try to get installed version
    output = run_command(check_command)
    if output is None:
        # Means the command wasn't found or failed => presumably not installed
        print(f"[INFO] {name} is not installed or not on PATH.")
        if prompt_yes_no(f"Do you want to install {name}?"):
            print(f"\n[INSTALL] {install_instructions}")
            # Realistically, you might run something like 'run_command("choco install nodejs")'
            # We'll just show instructions here so user can do it themselves.
        else:
            print("[SKIP] User chose not to install.")
        return
    else:
        # 2) Parse version from output
        match = re.search(version_regex, output)
        if not match:
            print(f"[WARN] Couldn't parse {name} version from output:\n{output}")
            return
        installed_version_str = match.group(1).strip()

        print(f"[INFO] {name} installed version: {installed_version_str}")
        print(f"[INFO] {name} required version: {required_version_str}")

        # 3) Compare
        compare_result = compare_versions(installed_version_str, required_version_str)
        if compare_result < 0:
            # installed < required
            print(f"[WARN] {name} is older than required.")
            if prompt_yes_no(f"Do you want to upgrade {name}?"):
                print(f"\n[UPGRADE] {upgrade_instructions}")
            else:
                print("[SKIP] User chose not to upgrade.")
        elif compare_result > 0:
            # installed > required
            print(f"[WARN] {name} is newer than required. Possibly okay, but might cause issues.")
            if prompt_yes_no(f"Do you want to downgrade {name} to {required_version_str}?"):
                print(f"\n[DOWNGRADE] {upgrade_instructions}")
            else:
                print("[SKIP] User chose not to downgrade.")
        else:
            print(f"[OK] {name} version is acceptable.")



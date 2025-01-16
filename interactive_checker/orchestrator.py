import re
import json
from interactive_checker.command_runner import run_command, run_command_live
from interactive_checker.version_compare import compare_versions
from interactive_checker.prompt import prompt_yes_no


def load_tools_config(config_file="requirements.json"):
    """
    Load tools configuration from a JSON file.
    """
    print(f"[DEBUG] Reading configuration from: {config_file}")
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
            tools = config.get("tools", [])
            if not tools:
                print("[WARN] No tools found in the configuration file.")
            return tools
    except FileNotFoundError:
        print(f"[ERROR] Configuration file '{config_file}' not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse '{config_file}'. JSON error: {e}")
        return []


def generate_commands(tool):
    """
    Generate default commands for a tool dynamically based on its name and version.
    """
    name = tool["name"].lower()
    required_version = tool["required_version"]

    return {
        "check_command": f"{name} --version",
        "install_command": f"choco install {name} --version={required_version} -y",
        "upgrade_command": f"choco upgrade {name} --version={required_version} -y",
    }


def get_installed_version(name, check_cmd, version_regex):
    """
    Retrieve the installed version of a tool using a check command.
    """
    output = run_command(check_cmd)
    if not output:
        print(f"[INFO] {name} is not installed or not in PATH.")
        return None

    match = re.search(version_regex, output)
    if not match:
        print(f"[WARN] Could not parse {name} version from output:\n{output}")
        return None

    return match.group(1).strip()


def manage_tool(tool):
    """
    Handle installation, upgrade, or downgrade of a tool.
    """
    # Dynamically generate commands
    commands = generate_commands(tool)

    # Use dynamically generated commands
    check_cmd = commands["check_command"]
    install_cmd = commands["install_command"]
    upgrade_cmd = commands["upgrade_command"]

    # Other metadata
    name = tool["name"]
    version_regex = tool["version_regex"]
    required_version = tool["required_version"]

    print(f"\n=== Managing {name} ===")

    # Check the tool's installed version
    installed_version = get_installed_version(name, check_cmd, version_regex)
    if not installed_version:
        if prompt_yes_no(f"{name} is not installed. Do you want to install it?"):
            success = run_command_live(install_cmd)
            if success:
                print(f"[SUCCESS] {name} installed successfully.")
            else:
                print(f"[ERROR] Failed to install {name}.")
        return

    # Compare and handle version mismatches
    compare_result = compare_versions(installed_version, required_version)
    if compare_result == 0:
        print(f"[OK] {name} is up to date.")
    elif compare_result < 0:
        # Installed version is older
        if prompt_yes_no(f"{name} is outdated. Upgrade to {required_version}?"):
            success = run_command_live(upgrade_cmd)
            if success:
                print(f"[SUCCESS] {name} upgraded successfully.")
            else:
                print(f"[ERROR] Failed to upgrade {name}.")
    else:
        # Installed version is newer
        if prompt_yes_no(f"{name} is newer than required. Downgrade to {required_version}?"):
            success = run_command_live(install_cmd)
            if success:
                print(f"[SUCCESS] {name} downgraded successfully.")
            else:
                print(f"[ERROR] Failed to downgrade {name}.")


def run_interactive_setup(config_file="requirements.json"):
    """
    Run interactive setup for all tools in the configuration.
    """
    tools = load_tools_config(config_file)
    if not tools:
        print("[INFO] No tools found in configuration. Exiting.")
        return

    for tool in tools:
        try:
            manage_tool(tool)
        except KeyError as e:
            print(f"[ERROR] Missing required key '{e.args[0]}' in tool configuration: {tool}")
        except Exception as e:
            print(f"[ERROR] Unexpected error while managing {tool['name']}: {e}")
    print("\n[INFO] Setup complete.")

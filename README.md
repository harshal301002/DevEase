# Zero Config Dev (Windows-Friendly)

This project checks a list of requirements (tools) on Windows, compares their installed versions to a required version, and—if missing or outdated—prompts the user to install or upgrade.

## How It Works

1. `config.json` lists each requirement:
   - A command to check the version
   - A regex to extract the version
   - A required version
   - Instructions or commands for install/upgrade

2. `main.py` calls `requirements_checker.py`, which:
   - Loads the config
   - For each requirement, checks if it's installed
   - If missing, prompts to install
   - If version doesn't match, prompts to upgrade/downgrade

3. **No external dependencies**—all modules are from Python's standard library.

## Usage

1. **Edit `config.json`** to define your tools.
2. **Run**:
   ```bash
   python main.py

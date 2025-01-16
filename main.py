#!/usr/bin/env python3
"""
main.py - Ensures admin rights on Windows, then runs interactive environment setup.
"""

from interactive_checker.orchestrator import run_interactive_setup
from interactive_checker.admin_access import ensure_admin

import traceback


def main():
    try:
        ensure_admin()  # Re-launches as admin if needed
        run_interactive_setup()  # Executes the main setup logic
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n[INFO] Operation cancelled by user.")
    except Exception:
        traceback.print_exc()
        input("An unexpected error occurred. Press Enter to close...")


if __name__ == "__main__":
    main()

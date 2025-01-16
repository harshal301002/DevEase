import sys
import ctypes

def ensure_admin():
    """
    Re-run the script as admin if not already elevated.
    Windows will show a UAC prompt unless UAC is disabled.
    """
    try:
        # `IsUserAnAdmin` returns a non-zero value if admin
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        print("[INFO] Not running as admin - attempting to elevate privileges...")
        # Re-run the script with admin rights
        # Note: This will cause a UAC popup
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas",                 # operation
            sys.executable,          # the python interpreter
            " ".join(sys.argv),      # the script + arguments
            None, 
            1                        # SW_SHOWNORMAL
        )
        sys.exit(0)  # Important to exit the current process

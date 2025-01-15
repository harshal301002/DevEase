import subprocess

def run_command(cmd: str):
    """
    Runs a shell command on Windows.
    Returns the command's output (stdout) as a string, or None if the command fails/not found.
    """
    try:
        # On Windows, shell=True allows usage of built-in commands (like 'dir', etc.)
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        return output.strip()
    except FileNotFoundError:
        # Means the command doesn't exist
        return None
    except subprocess.CalledProcessError:
        # Means the command ran but returned an error code
        return None

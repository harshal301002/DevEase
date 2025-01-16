import subprocess


def run_command(cmd: str) -> str:
    """
    Runs a shell command, returning its output as a string,
    or None if the command fails. Ideal for quick checks.
    """
    try:
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        return output.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[ERROR] Command failed: {cmd}\nReason: {str(e)}")
        return None


def run_command_live(cmd: str) -> bool:
    """
    Runs a shell command, streaming stdout to the console in real-time.
    Returns True if exit code == 0 (success), else False.
    """
    print(f"[CMD] {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end="")  # Pass output line-by-line directly
    exit_code = process.wait()
    return exit_code == 0

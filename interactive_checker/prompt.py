def prompt_yes_no(question: str) -> bool:
    """
    Asks the user a yes/no question in the console. Returns True if yes, False if no.
    """
    while True:
        ans = input(f"{question} (y/n): ").strip().lower()
        if ans in ["y", "yes"]:
            return True
        elif ans in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")

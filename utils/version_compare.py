def compare_versions(installed: str, required: str) -> int:
    """
    Compares two version strings (e.g. '16.14.2' vs '16.14.0').
    Returns:
      -1 if installed < required
       0 if installed == required
      +1 if installed > required

    This is naive: only handles up to major.minor.patch.
    Extra fields are ignored (e.g., build metadata).
    """
    i_parts = installed.split('.')[:3]
    r_parts = required.split('.')[:3]

    # Pad with zeros if missing patch or minor
    while len(i_parts) < 3:
        i_parts.append('0')
    while len(r_parts) < 3:
        r_parts.append('0')

    i_nums = list(map(int, i_parts))
    r_nums = list(map(int, r_parts))

    if i_nums == r_nums:
        return 0
    elif i_nums < r_nums:
        return -1
    else:
        return 1

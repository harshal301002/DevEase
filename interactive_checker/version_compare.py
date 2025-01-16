def compare_versions(installed: str, required: str) -> int:
    """
    Compare two version strings, e.g. '16.14.2' vs '16.14.0'.
    Returns:
        0 if installed == required
       -1 if installed < required
       +1 if installed > required
    """

    i_parts = installed.split('.')[:3]
    r_parts = required.split('.')[:3]

    # Pad to length 3
    while len(i_parts) < 3:
        i_parts.append('0')
    while len(r_parts) < 3:
        r_parts.append('0')

    try:
        i_nums = list(map(int, i_parts))
        r_nums = list(map(int, r_parts))
    except ValueError:
        return 0  # can't compare properly

    if i_nums == r_nums:
        return 0
    elif i_nums < r_nums:
        return -1
    else:
        return 1

import datetime


def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names' for the ticket.
    Returns '' if name is not a string or has no words.
    A single-word name is returned as just the surname (no trailing comma).
    """
    if not isinstance(name, str):
        return ''
    parts = name.split()
    if not parts:
        return ''
    surname = parts[-1].title()
    given = ' '.join(parts[:-1]).title()
    if not given:
        return surname
    return surname + ', ' + given


def parse_group_ages(text):
    """
    Parses space-separated ages into a list of ints.
    Returns [] if text is not a string. Values that are not whole
    numbers (e.g. 'abc', '3.5') are skipped.
    """
    if not isinstance(text, str):
        return []
    ages = []
    for token in text.split():
        try:
            ages.append(int(token))
        except ValueError:
            continue
    return ages


def parse_visit_date(text):
    """
    Parses a YYYY-MM-DD date into a (year, month, day) tuple.
    Returns None if text is not a string or is not a valid calendar date.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split('-')
    if len(parts) != 3:
        return None
    try:
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        datetime.date(year, month, day)  # validates ranges / leap years
    except (ValueError, OverflowError):
        return None
    return year, month, day


def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value))

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    print("Visit date (year, month, day):", parse_visit_date(value))


if __name__ == "__main__":
    main()

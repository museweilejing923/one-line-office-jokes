#!/usr/bin/env python3
"""One-line office joke: check the fixed entry, then write it out.

Trust falls, nobody catches the intern, and suddenly there is a new
team building exercise. This program never accepts outside text: it
holds exactly one joke, proves that joke is well formed, and saves it
to a file. There is no input, no network access, no clock, and no
randomness anywhere in here.
"""

import sys

ENTRY = "Our team building exercise was trust falls. Nobody caught the intern. We have a new team building exercise now."
CHAR_LIMIT = 199
DESTINATION = "/output/entry.txt"
ENDERS = (".", "!", "?")
FILLER = set(".,!?;:'\"-() ")


def fail(problem):
    """Print why the entry was refused and stop without writing."""
    print(f"refused: {problem}", file=sys.stderr)
    raise SystemExit(1)


def guard_nonempty(text):
    return bool(text and text.strip())


def guard_short_enough(text):
    return len(text) <= CHAR_LIMIT


def guard_no_controls(text):
    return all(ord(letter) >= 32 for letter in text)


def guard_tidy_spacing(text):
    stripped = text.strip()
    return text == stripped and "  " not in text and "\t" not in text


def guard_has_letters(text):
    return any(letter.isalpha() for letter in text)


def guard_not_only_marks(text):
    return not all(letter in FILLER for letter in text)


def guard_not_only_digits(text):
    return not text.strip().isdigit()


def guard_ends_with_mark(text):
    return text.rstrip().endswith(ENDERS)


def guard_names_intern(text):
    return "intern" in text.lower()


def guard_no_asides(text):
    # No asides in parentheses: one line, straight through.
    return "(" not in text and ")" not in text


def guard_opens_capital(text):
    # A joke told straight starts with a capital letter.
    return text[:1].isupper()


# Every guard is listed with the complaint shown when it trips. The
# checker runs them in this order and stops at the first failure, so a
# bad entry never reaches the file.
RULES = [
    ("entry must mention the intern", guard_names_intern),
    ("entry must not contain parentheses", guard_no_asides),
    ("entry must start with a capital letter", guard_opens_capital),
    ("entry is empty", guard_nonempty),
    ("entry is longer than the 199 character limit", guard_short_enough),
    ("entry contains control characters", guard_no_controls),
    ("entry has ragged spacing or a tab", guard_tidy_spacing),
    ("entry contains no letters", guard_has_letters),
    ("entry is punctuation only", guard_not_only_marks),
    ("entry is digits only", guard_not_only_digits),
    ("entry does not end with punctuation", guard_ends_with_mark),
]


def check_entry(text):
    for problem, guard in RULES:
        if not guard(text):
            fail(problem)


def main():
    check_entry(ENTRY)
    with open(DESTINATION, "w", encoding="utf-8") as out:
        out.write(ENTRY + "\n")


if __name__ == "__main__":
    main()

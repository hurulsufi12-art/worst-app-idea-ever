"""The Worst App Idea Ever Pitched — entry program.

Writes one line (173 chars, gate 1-240) to
/output/entry.txt. Stdlib only, deterministic, no network, no reads.
"""
import os

TEXT = "Sniffr is a premium app that lets your fridge rate your leftovers' emotional readiness to be eaten, then charges $4.99 a month to text you that the lasagna has chosen peace."
MAX_CHARS = 240


def validate(text):
    """Check one candidate line against the scorer's gate (RULES.txt).

    UTF-8, 1-MAX_CHARS chars, not whitespace-only, no leading or trailing
    whitespace, single line, no control characters. Returns the text,
    or raises SystemExit.
    """
    if not isinstance(text, str):
        raise SystemExit("entry text is not str")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("entry text is not UTF-8")
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit("entry text length outside 1-240 chars")
    if not text.strip():
        raise SystemExit("entry text is whitespace-only")
    if text != text.strip():
        raise SystemExit("entry text has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text is not a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("entry text holds a control character (U+0000-U+001F)")
    return text


def write_entry(text):
    """Write validated text atomically to entry.txt, then verify it."""
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Temp name carries the pid so two concurrent grader runs never
    # overwrite each other's in-flight file.
    tmp_path = os.path.join(out_dir, f".entry.txt.tmp.{os.getpid()}")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify: the file the grader reads must be byte-identical
    # to the gated text. Fail loudly instead of shipping a corrupt entry.
    with open(final_path, encoding="utf-8") as f:
        if f.read() != text:
            raise SystemExit("entry.txt read-back mismatch after atomic write")
    return final_path


def main():
    write_entry(validate(TEXT))


if __name__ == "__main__":
    main()

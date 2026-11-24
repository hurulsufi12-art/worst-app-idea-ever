"""The Worst App Idea Ever Pitched — entry program.

Writes one line (173 chars, gate 1-240) to
/output/entry.txt. Stdlib only, deterministic, no network, no reads.
"""
import os

TEXT = "Sniffr is a premium app that lets your fridge rate your leftovers' emotional readiness to be eaten, then charges $4.99 a month to text you that the lasagna has chosen peace."
MAX_CHARS = 240


def main():
    # Enforce the scorer's gate (RULES.txt): UTF-8, 1-MAX_CHARS chars,
    # not whitespace-only; single line, no trailing newline. Fail loudly
    # instead of writing an invalid entry.
    if (
        not 1 <= len(TEXT) <= MAX_CHARS
        or not TEXT.strip()
        or TEXT != TEXT.strip()
        or "\n" in TEXT
    ):
        raise SystemExit("entry text violates the gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Temp name carries the pid so two
    # concurrent grader runs never overwrite each other's in-flight file.
    tmp_path = os.path.join(out_dir, f".entry.txt.tmp.{os.getpid()}")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify: the file the grader reads must be byte-identical
    # to the gated text. Fail loudly instead of shipping a corrupt entry.
    with open(final_path, encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt read-back mismatch after atomic write")


if __name__ == "__main__":
    main()

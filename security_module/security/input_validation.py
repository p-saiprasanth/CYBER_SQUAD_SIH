"""
input_validation.py
--------------------
Phase 1 (remainder) — Input validation & secure API practices.

Every piece of input that enters the system from a user or API call
should pass through here before it touches business logic, the file
system, or the database. This blocks malformed IDs, oversized/unsafe
file uploads, and basic injection-style payloads.
"""

import os
import re

# --- Rules -----------------------------------------------------------

ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")          # e.g. CASE001, E001, U001
ALLOWED_EVIDENCE_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".txt", ".csv", ".mp3", ".mp4", ".docx"
}
MAX_EVIDENCE_FILE_SIZE_MB = 200

# characters/patterns that should never appear in free-text fields
# (basic defense-in-depth; the real defense is parameterized queries /
# ORM usage wherever this data eventually reaches a database)
SUSPICIOUS_PATTERNS = [
    re.compile(r"(--|;|/\*|\*/|xp_)", re.IGNORECASE),          # SQL injection markers
    re.compile(r"<\s*script.*?>", re.IGNORECASE),               # XSS
    re.compile(r"\.\./"),                                        # path traversal
]


class ValidationError(Exception):
    pass


def validate_id(value: str, field_name: str = "id") -> str:
    """Validate a case/evidence/user id: alphanumeric, dash/underscore, 3-32 chars."""
    if not value or not ID_PATTERN.match(value):
        raise ValidationError(
            f"Invalid {field_name}: {value!r}. Must be 3-32 chars, letters/digits/-/_ only."
        )
    return value


def validate_text_field(value: str, field_name: str = "field", max_length: int = 2000) -> str:
    """Validate a free-text field: length limit + reject obviously malicious patterns."""
    if value is None:
        raise ValidationError(f"{field_name} is required")
    if len(value) > max_length:
        raise ValidationError(f"{field_name} exceeds max length of {max_length} characters")
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.search(value):
            raise ValidationError(f"{field_name} contains disallowed characters/pattern")
    return value


def validate_evidence_file(file_path: str) -> str:
    """
    Validate an evidence file before it's hashed/registered:
    - must exist
    - extension must be in the allow-list
    - size must be under the configured max
    """
    if not os.path.isfile(file_path):
        raise ValidationError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EVIDENCE_EXTENSIONS:
        raise ValidationError(
            f"File type '{ext}' not allowed. Allowed types: {sorted(ALLOWED_EVIDENCE_EXTENSIONS)}"
        )

    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_EVIDENCE_FILE_SIZE_MB:
        raise ValidationError(
            f"File too large ({size_mb:.1f} MB). Max allowed is {MAX_EVIDENCE_FILE_SIZE_MB} MB."
        )

    return file_path


if __name__ == "__main__":
    print(validate_id("CASE001", "case_id"))

    try:
        validate_id("CASE 001; DROP TABLE cases;", "case_id")
    except ValidationError as e:
        print("Blocked bad id:", e)

    try:
        validate_text_field("<script>alert(1)</script>", "notes")
    except ValidationError as e:
        print("Blocked XSS attempt:", e)

    try:
        validate_text_field("../../etc/passwd", "notes")
    except ValidationError as e:
        print("Blocked path traversal attempt:", e)

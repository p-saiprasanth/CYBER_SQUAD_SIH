# Audit Log Schema — Proposal for Team Sync
**From:** Prasanth (Cybersecurity + Blockchain)
**To:** Aman
**Purpose:** Align on a single audit log schema so my security module's logs and yours merge cleanly into one system-wide audit trail — instead of two incompatible log formats.

---

## Proposed schema (what my module currently produces)

```json
{
  "user_id": "U001",
  "action": "EVIDENCE_VERIFIED",
  "case_id": "CASE001",
  "evidence_id": "E001",
  "timestamp": "2026-09-08T05:50:12.520204+00:00",
  "ip": "10.0.0.5",
  "result": "VALID"
}
```

### Field definitions
| Field | Type | Required? | Notes |
|---|---|---|---|
| `user_id` | string | required | Who performed the action |
| `action` | string (enum) | required | See action list below — please tell me if you need more added |
| `case_id` | string \| null | optional | Present when the action relates to a specific case |
| `evidence_id` | string \| null | optional | Present when the action relates to specific evidence |
| `timestamp` | string (ISO 8601, UTC) | required | Always UTC, with timezone offset included |
| `ip` | string \| null | optional | Requester IP, for security forensics |
| `result` | string \| null | optional | e.g. "VALID", "MISMATCH", "SUCCESS", "FAILED" |

### Current action enum (from my module)
```
LOGIN, CASE_CREATED, EVIDENCE_ADDED, EVIDENCE_UPLOADED, EVIDENCE_PROCESSED,
EVIDENCE_VERIFIED, EVIDENCE_HASH_MISMATCH, GRAPH_GENERATED, GRAPH_ACCESSED,
AI_QUERY, PREDICTION_GENERATED, REPORT_EXPORTED
```

## Questions for Aman
1. Does your side need additional fields (e.g. `session_id`, `request_id` for tracing)?
2. Are there actions from your modules (e.g. graph generation, AI queries) that should log through my `audit.py` instead of a separate system — or do we keep two log streams and merge at query time?
3. Where should the canonical log store live — my local JSON file is a placeholder; do we standardize on a shared DB table (e.g. Postgres `audit_logs`) that both our modules write to directly?
4. Naming convention check — are you using `snake_case` action names too, or something else? Let's not end up with `EVIDENCE_VERIFIED` on my side and `evidenceVerified` on yours.

## What I need from you to finalize
Once we agree on the shape above, I'll update `get_audit_trail()` / `log_action()` in `security/audit.py` to match exactly, so there's one consistent schema across the whole platform before final integration.

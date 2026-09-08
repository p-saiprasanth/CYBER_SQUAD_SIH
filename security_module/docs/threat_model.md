# Threat Model — AI-Powered Criminal Network Intelligence Platform
### Cybersecurity + Blockchain module — Phase 6

Each threat is analyzed as: **Threat → Impact → Mitigation → Implementation**
(Implementation column references the actual file/function that enforces the mitigation.)

---

### 1. Unauthorized Access
- **Threat:** An unauthenticated or unauthorized user accesses case data, evidence, or the graph.
- **Impact:** Sensitive investigation data exposed; compromises ongoing investigations and victim/suspect privacy.
- **Mitigation:** Mandatory authentication (session tokens) + role-based authorization on every sensitive action.
- **Implementation:** `auth.py` — `authenticate_user()`, `get_session()`, `require_permission()` decorator.

### 2. Evidence Tampering
- **Threat:** Someone modifies an evidence file after it has been logged (altering a transaction amount, editing a document).
- **Impact:** Corrupted evidence undermines the legal validity of an investigation; false leads or false exonerations.
- **Mitigation:** SHA-256 hash generated at registration; any future verification re-hashes and compares, flagging any mismatch immediately.
- **Implementation:** `hashing.py`, `verification.py`, `blockchain.py` — `register_evidence()` / `verify_evidence()`.

### 3. Privilege Escalation
- **Threat:** An INVESTIGATOR or ANALYST attempts to perform an ADMIN-only action (e.g. managing users, changing system config).
- **Impact:** Unauthorized users gain control over accounts, roles, or system settings — a total trust breakdown.
- **Mitigation:** Explicit permission table per role; every protected function checks role permissions before executing, never trusting client-side role claims.
- **Implementation:** `auth.py` — `PERMISSIONS` dict, `has_permission()`, `require_permission()`.

### 4. API Abuse / Brute Force
- **Threat:** Repeated rapid requests to login, verify-evidence, or AI-query endpoints (credential stuffing, denial-of-service attempts).
- **Impact:** Account compromise via brute force; degraded system performance for legitimate investigators.
- **Mitigation:** Sliding-window rate limiting per user/IP on sensitive endpoints.
- **Implementation:** `rate_limiter.py` — `login_limiter`, `verify_limiter`, `ai_query_limiter`.

### 5. Malicious Input (Injection Attacks)
- **Threat:** SQL injection, XSS, or path traversal payloads submitted through case IDs, notes, or file uploads.
- **Impact:** Database compromise, script execution in the dashboard, unauthorized file system access.
- **Mitigation:** Strict input validation (allow-listed ID formats, pattern-based rejection of injection markers) on every external input before it reaches business logic.
- **Implementation:** `input_validation.py` — `validate_id()`, `validate_text_field()`, `validate_evidence_file()`.

### 6. Data Leakage
- **Threat:** Sensitive data (PII, case details) exposed via verbose error messages, logs, or an over-permissive API response.
- **Impact:** Privacy violation, potential legal liability, compromised source protection.
- **Mitigation:** Structured, minimal audit logs (no raw evidence content logged, only metadata); secrets never hardcoded or logged.
- **Implementation:** `audit.py` (metadata-only logging), `secrets_manager.py` (env-var based secrets, never hardcoded).

### 7. Fake / Forged Evidence
- **Threat:** Someone attempts to introduce fabricated evidence into the system as if it were originally registered.
- **Impact:** Corrupts the integrity of the entire investigation; could frame an innocent person or clear a guilty one.
- **Mitigation:** Every evidence registration is hash-anchored to a ledger record with a timestamp and transaction ID at the moment of intake — evidence introduced later cannot retroactively claim an earlier registration time.
- **Implementation:** `blockchain.py` — `register_evidence()` records `tx_id` + `timestamp` at intake.

### 8. Model Manipulation / Prompt Injection
- **Threat:** Malicious text embedded in case notes or uploaded documents attempts to hijack the AI assistant's behavior ("ignore previous instructions...").
- **Impact:** AI could leak data, take unauthorized actions, or produce misleading investigative summaries.
- **Mitigation:** Pattern-based prompt-injection scanning on all text entering the LLM context; strict allow-list of AI tool actions.
- **Implementation:** `ai_guardrails.py` — `sanitize_ai_input()`, `authorize_ai_tool_call()`.

### 9. Unauthorized Graph Access
- **Threat:** A user queries or exports parts of the knowledge graph belonging to cases they aren't assigned to.
- **Impact:** Cross-case data exposure; violates case confidentiality boundaries between investigation teams.
- **Mitigation:** Graph queries pass through the same RBAC/permission layer as other actions; `GRAPH_ACCESSED` events are audit-logged per case.
- **Implementation:** `auth.py` (`view_graph` permission), `audit.py` (`GRAPH_ACCESSED` logging).

---

## Summary
Every threat above maps to a concrete, already-implemented control in this
module — this table is not aspirational, it documents what the code in
`security/` actually enforces today.

# Cyber Squad - PostgreSQL Database

## Database
Supabase PostgreSQL

## Tables

### cases
Stores investigation case information.

- id
- case_number
- title
- description
- status
- created_at

### entities
Stores persons, organizations and locations.

- id
- case_id
- entity_type
- name
- confidence

### evidence
Stores investigation evidence.

- id
- case_id
- file_name
- content
- hash
- source
- created_at

### relationships
Stores connections between entities.

- id
- case_id
- source_entity
- target_entity
- relationship_type
- confidence
- evidence_id

### events
Stores investigation timeline events.

- id
- case_id
- entity_id
- event_type
- timestamp
- location

### users
Stores application users.

### audit_logs
Stores system activity and audit information.

## Synthetic Data

Current seed data contains:

- 2 cases
- 10 entities
- 5 evidence records
- 10 relationships
- 5 events

## Files

- schema.sql - creates database tables
- seed.sql - inserts synthetic investigation data

## Architecture

CSV / JSON
    ↓
PostgreSQL
    ↓
FastAPI
    ↓
React Dashboard
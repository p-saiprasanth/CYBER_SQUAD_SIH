-- Cyber Squad
-- PostgreSQL Database Schem

CREATE TABLE cases (
    id BIGSERIAL PRIMARY KEY,
    case_number VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT REFERENCES cases(id) ON DELETE CASCADE,
    file_name VARCHAR(255),
    content TEXT,
    hash VARCHAR(255),
    source VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE entities (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT REFERENCES cases(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    confidence DECIMAL(5,4)
);

CREATE TABLE relationships (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT REFERENCES cases(id) ON DELETE CASCADE,
    source_entity BIGINT REFERENCES entities(id) ON DELETE CASCADE,
    target_entity BIGINT REFERENCES entities(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100),
    confidence DECIMAL(5,4),
    evidence_id BIGINT REFERENCES evidence(id) ON DELETE SET NULL
);

CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT REFERENCES cases(id) ON DELETE CASCADE,
    entity_id BIGINT REFERENCES entities(id) ON DELETE SET NULL,
    event_type VARCHAR(100),
    timestamp TIMESTAMP,
    location VARCHAR(255)
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100),
    table_name VARCHAR(100),
    record_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
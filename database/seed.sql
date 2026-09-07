-- Cyber Squad
-- Synthetic investigation seed data

INSERT INTO cases (case_number, title, description, status)
VALUES
('CASE-001', 'Operation Shadow Network',
 'Investigation into an organized criminal network.',
 'active'),
('CASE-002', 'Project Black Route',
 'Investigation involving suspicious financial transactions.',
 'active');

INSERT INTO entities (case_id, entity_type, name, confidence)
VALUES
(1, 'PERSON', 'Raj Kumar', 0.98),
(1, 'PERSON', 'Amit Sharma', 0.95),
(1, 'PERSON', 'Vikram Reddy', 0.91),
(1, 'PERSON', 'Suresh Rao', 0.89),
(1, 'PERSON', 'Priya Singh', 0.94),
(1, 'ORGANIZATION', 'Shadow Logistics', 0.93),
(1, 'ORGANIZATION', 'Black Route Ltd', 0.88),
(1, 'LOCATION', 'Hyderabad', 0.99),
(1, 'LOCATION', 'Vijayawada', 0.97),
(1, 'LOCATION', 'Chennai', 0.96);

INSERT INTO evidence
(case_id, file_name, content, hash, source)
VALUES
(1, 'communication_001.txt',
 'Communication record involving Raj Kumar and Amit Sharma.',
 'hash001', 'Synthetic Dataset'),
(1, 'transaction_001.json',
 'Suspicious financial transaction record.',
 'hash002', 'Synthetic Dataset'),
(1, 'location_001.csv',
 'Location movement record.',
 'hash003', 'Synthetic Dataset'),
(1, 'document_001.pdf',
 'Investigation document.',
 'hash004', 'Synthetic Dataset'),
(1, 'photo_001.jpg',
 'Photographic evidence.',
 'hash005', 'Synthetic Dataset');

INSERT INTO relationships
(case_id, source_entity, target_entity, relationship_type,
 confidence, evidence_id)
VALUES
(1, 1, 2, 'COMMUNICATED_WITH', 0.92, 1),
(1, 1, 3, 'ASSOCIATED_WITH', 0.87, 2),
(1, 2, 4, 'FINANCIAL_LINK', 0.84, 2),
(1, 3, 6, 'WORKS_FOR', 0.91, 3),
(1, 4, 7, 'CONNECTED_TO', 0.82, 4),
(1, 5, 6, 'ASSOCIATED_WITH', 0.79, 5),
(1, 1, 6, 'CONNECTED_TO', 0.90, 1),
(1, 2, 7, 'CONNECTED_TO', 0.85, 2),
(1, 3, 8, 'LOCATED_IN', 0.95, 3),
(1, 4, 9, 'LOCATED_IN', 0.93, 4);

INSERT INTO events
(case_id, entity_id, event_type, timestamp, location)
VALUES
(1, 1, 'MEETING', '2026-08-01 10:30:00', 'Hyderabad'),
(1, 2, 'TRANSACTION', '2026-08-03 14:00:00', 'Vijayawada'),
(1, 3, 'TRAVEL', '2026-08-05 09:15:00', 'Chennai'),
(1, 4, 'COMMUNICATION', '2026-08-07 18:30:00', 'Hyderabad'),
(1, 5, 'MEETING', '2026-08-10 11:00:00', 'Vijayawada');
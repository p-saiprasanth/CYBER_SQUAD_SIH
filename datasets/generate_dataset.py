"""
generate_dataset.py

Deterministic generator for a synthetic criminal-network investigation
dataset (SIH26189). Produces:

    data/cases.csv
    data/persons.csv
    data/organizations.csv
    data/locations.csv
    data/communications.csv
    data/transactions.csv
    data/events.csv
    data/evidence.csv
    data/graph_data.json   (DERIVED from the CSVs above, not invented)

All names, places, orgs are fictional. Hidden associations are built from
multiple indirect signals (common neighbour, shared org, shared location,
temporal proximity, transaction chains) and are NEVER inserted as a direct
edge -- they only emerge from combining several CSV rows.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import random
import re
from datetime import datetime, timedelta

random.seed(2026)

OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

START_DATE = datetime(2026, 1, 10)


def save_csv(filename, rows, fieldnames=None):
    path = os.path.join(OUT_DIR, filename)
    if not rows:
        return
    fieldnames = fieldnames or list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def ts(days, hours=0, minutes=0):
    return (START_DATE + timedelta(days=days, hours=hours, minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")


def fake_hash(seed):
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


# ===========================================================================
# CASES
# ===========================================================================

cases = [
    {
        "case_id": "CASE001",
        "case_name": "Operation Nightfall",
        "description": "Suspected smuggling and shell-finance network operating through front trading companies and a rented warehouse.",
        "case_type": "ORGANIZED_CRIME",
        "status": "ACTIVE",
        "start_date": "2026-01-05",
        "end_date": "",
        "lead_investigator": "Insp. Naomi Castellan",
    },
    {
        "case_id": "CASE002",
        "case_name": "Ledger Shadow",
        "description": "Minor suspected invoice-fraud case, largely unconnected to Operation Nightfall.",
        "case_type": "FINANCIAL_FRAUD",
        "status": "ACTIVE",
        "start_date": "2026-02-01",
        "end_date": "",
        "lead_investigator": "Insp. Dorian Achebe",
    },
]

# ===========================================================================
# LOCATIONS  (fictional places, clearly synthetic coordinates)
# ===========================================================================

locations = [
    {"location_id": "L001", "location_name": "Marrow Street Residence", "location_type": "RESIDENCE", "city": "Aldenport", "state": "Faroth Province", "latitude": 21.114, "longitude": 63.902},
    {"location_id": "L002", "location_name": "Kestrel Bay Apartments", "location_type": "RESIDENCE", "city": "Kestrel Bay", "state": "Faroth Province", "latitude": 21.402, "longitude": 63.771},
    {"location_id": "L003", "location_name": "Northgate Trading Office", "location_type": "OFFICE", "city": "Aldenport", "state": "Faroth Province", "latitude": 21.130, "longitude": 63.918},
    {"location_id": "L004", "location_name": "Solace Freight HQ", "location_type": "OFFICE", "city": "Millbrook", "state": "Faroth Province", "latitude": 20.887, "longitude": 64.055},
    {"location_id": "L005", "location_name": "Cinderlot Depot", "location_type": "WAREHOUSE", "city": "Ashgrove", "state": "Faroth Province", "latitude": 21.276, "longitude": 63.640},
    {"location_id": "L006", "location_name": "Harrow's End Storage", "location_type": "WAREHOUSE", "city": "Harrow's End", "state": "Faroth Province", "latitude": 21.550, "longitude": 63.500},
    {"location_id": "L007", "location_name": "Ravensbrook Meeting Hall", "location_type": "MEETING_PLACE", "city": "Ravensbrook", "state": "Faroth Province", "latitude": 21.005, "longitude": 64.200},
    {"location_id": "L008", "location_name": "Cindermere Diner", "location_type": "MEETING_PLACE", "city": "Aldenport", "state": "Faroth Province", "latitude": 21.120, "longitude": 63.910},
    {"location_id": "L009", "location_name": "The Aldermere Inn", "location_type": "HOTEL", "city": "Aldenport", "state": "Faroth Province", "latitude": 21.140, "longitude": 63.930},
    {"location_id": "L010", "location_name": "Portway Financial Plaza", "location_type": "FINANCIAL_LOCATION", "city": "Millbrook", "state": "Faroth Province", "latitude": 20.900, "longitude": 64.070},
    {"location_id": "L011", "location_name": "Aldenport Transit Hub", "location_type": "TRANSPORT_HUB", "city": "Aldenport", "state": "Faroth Province", "latitude": 21.150, "longitude": 63.940},
    {"location_id": "L012", "location_name": "Millbrook Rail Terminal", "location_type": "TRANSPORT_HUB", "city": "Millbrook", "state": "Faroth Province", "latitude": 20.910, "longitude": 64.080},
]
location_ids = [l["location_id"] for l in locations]

# ===========================================================================
# ORGANIZATIONS
# ===========================================================================

organizations = [
    {"organization_id": "O001", "organization_name": "Solace Freight Cooperative", "organization_type": "LOGISTICS", "location_id": "L004", "case_id": "CASE001", "status": "ACTIVE"},
    {"organization_id": "O002", "organization_name": "Northgate Import Traders", "organization_type": "TRADING", "location_id": "L003", "case_id": "CASE001", "status": "UNDER_REVIEW"},
    {"organization_id": "O003", "organization_name": "Millbrook Civic Bank", "organization_type": "FINANCIAL", "location_id": "L010", "case_id": "CASE001", "status": "ACTIVE"},
    {"organization_id": "O004", "organization_name": "Solace Freight Cooperative", "organization_type": "LOGISTICS", "location_id": "L004", "case_id": "CASE001", "status": "ACTIVE"},
    {"organization_id": "O005", "organization_name": "Harrow's End Storage Ltd.", "organization_type": "WAREHOUSING", "location_id": "L006", "case_id": "CASE001", "status": "UNDER_REVIEW"},
    {"organization_id": "O006", "organization_name": "Ravensbrook Consulting Group", "organization_type": "CONSULTING", "location_id": "L007", "case_id": "CASE002", "status": "ACTIVE"},
    {"organization_id": "O007", "organization_name": "Portway Accounting Partners", "organization_type": "FINANCIAL", "location_id": "L010", "case_id": "CASE002", "status": "ACTIVE"},
]
# NOTE: O004 duplicates O001's name/location deliberately -- it represents a
# second, semi-independent "chapter" of the same cooperative brand used by a
# different employee cluster (P002/P020) for the shared-organization hidden
# association, while keeping O001 as the main freight org used elsewhere.
organizations[3]["organization_name"] = "Solace Freight Cooperative (Millbrook Branch)"

# ===========================================================================
# PERSONS
# ===========================================================================

first_names = ["Rikard", "Dahlia", "Oskar", "Ines", "Tomas", "Marek", "Elowen", "Petra",
               "Callan", "Ines", "Soren", "Wren", "Dax", "Liora", "Emeric", "Ysolde",
               "Bram", "Cass", "Niven", "Aurelia", "Joric", "Freya", "Renn", "Sable"]
last_names = ["Solmyr", "Renfrew", "Venn", "Draventa", "Halloway", "Ostrow", "Kestrel", "Amberlyn",
              "Brackwood", "Corvane", "Dellamere", "Eastfield", "Farrow", "Gravenor", "Hargrove",
              "Ivory", "Jarrow", "Kellemont", "Lindqvist", "Marrow", "Norrick", "Ostwind", "Pryce", "Quillon"]

roles = (
    ["suspect"] * 6 + ["associate"] * 5 + ["witness"] * 3 + ["victim"] * 2
    + ["investigator"] * 3 + ["intermediary"] * 3 + ["associate"] * 2
)
random.shuffle(roles)

persons = []
for i in range(1, 25):
    pid = f"P{i:03d}"
    fn, ln = first_names[i - 1], last_names[i - 1]
    name = f"{fn} {ln}"
    role = roles[i - 1] if i - 1 < len(roles) else random.choice(["associate", "witness"])
    persons.append({
        "person_id": pid,
        "name": name,
        "age": random.randint(24, 58),
        "gender": random.choice(["male", "female"]),
        "role": role,
        "phone": f"55501{10000 + i}",
        "email": f"{fn.lower()}.{ln.lower()}@fictmail.example",
        "organization_id": "",  # filled in below for key story persons + random fill
        "location_id": random.choice(location_ids),
        "case_id": "CASE001" if i <= 20 else "CASE002",
    })

person_by_id = {p["person_id"]: p for p in persons}

# ---- Fixed story assignments (organizations / key roles) ----
person_by_id["P001"]["role"] = "suspect"
person_by_id["P001"]["organization_id"] = "O002"       # Northgate Import Traders
person_by_id["P001"]["location_id"] = "L001"

person_by_id["P010"]["role"] = "suspect"
person_by_id["P010"]["organization_id"] = "O005"       # Harrow's End Storage
person_by_id["P010"]["location_id"] = "L002"

person_by_id["P006"]["role"] = "intermediary"
person_by_id["P006"]["organization_id"] = ""
person_by_id["P006"]["location_id"] = "L008"

person_by_id["P002"]["role"] = "associate"
person_by_id["P002"]["organization_id"] = "O001"       # Solace Freight Cooperative
person_by_id["P002"]["location_id"] = "L004"

person_by_id["P020"]["role"] = "associate"
person_by_id["P020"]["organization_id"] = "O004"       # Solace Freight Cooperative (Millbrook Branch)
person_by_id["P020"]["location_id"] = "L004"
person_by_id["P020"]["case_id"] = "CASE001"

person_by_id["P003"]["role"] = "associate"
person_by_id["P003"]["organization_id"] = "O002"
person_by_id["P007"]["role"] = "intermediary"
person_by_id["P015"]["role"] = "witness"

person_by_id["P008"]["role"] = "associate"
person_by_id["P022"]["role"] = "witness"
person_by_id["P022"]["case_id"] = "CASE001"

for pid in ["P011", "P012", "P013"]:
    person_by_id[pid]["role"] = "investigator"

# Fill any remaining blank organization_id randomly among CASE001 persons
# (not investigators/witnesses -- keeps role semantics sane), leaving some
# persons with no organization at all (also realistic).
org_pool = ["O001", "O002", "O003", "O005", ""]
for p in persons:
    if p["organization_id"] == "" and p["role"] in ("suspect", "associate", "intermediary"):
        if random.random() < 0.6:
            p["organization_id"] = random.choice(org_pool)

# ===========================================================================
# COMMUNICATIONS  (target ~70 rows)
# ===========================================================================

comm_types = ["CALL", "MESSAGE", "EMAIL"]
communications = []
comm_counter = 1
evidence_registry = []  # (evidence_id, case_id, evidence_type, source, description, collected_at, related_entity_id)


def add_evidence(case_id, evidence_type, source, description, collected_at, related_entity_id):
    eid = f"E{len(evidence_registry) + 1:03d}"
    evidence_registry.append({
        "evidence_id": eid,
        "case_id": case_id,
        "evidence_type": evidence_type,
        "source": source,
        "description": description,
        "collected_at": collected_at,
        "related_entity_id": related_entity_id,
        "hash": fake_hash(eid + description),
        "status": "VERIFIED",
    })
    return eid


def add_communication(day, hour, minute, src, tgt, ctype, content, case_id="CASE001", device="DEV-GEN", with_evidence=True):
    global comm_counter
    cid = f"C{comm_counter:03d}"
    comm_counter += 1
    timestamp = ts(day, hour, minute)
    eid = ""
    if with_evidence:
        eid = add_evidence(case_id, "PHONE_RECORD" if ctype != "EMAIL" else "EMAIL",
                            "Telecom Provider Log" if ctype != "EMAIL" else "Email Server Log",
                            f"{ctype} record between {src} and {tgt}", timestamp, cid)
    communications.append({
        "communication_id": cid, "case_id": case_id, "timestamp": timestamp,
        "source_person_id": src, "target_person_id": tgt, "communication_type": ctype,
        "duration_or_content": content, "device_id": device, "evidence_id": eid,
    })
    return cid


# ---- Story communications ----
add_communication(1, 9, 12, "P001", "P006", "CALL", "184s")
add_communication(3, 14, 5, "P006", "P010", "CALL", "302s")
add_communication(4, 10, 40, "P002", "P011", "CALL", "88s")  # P011 investigator interview call
add_communication(5, 16, 20, "P003", "P006", "MESSAGE", "Confirming delivery schedule")
add_communication(6, 11, 0, "P006", "P015", "CALL", "210s")
add_communication(2, 8, 30, "P005", "P001", "CALL", "95s")
add_communication(2, 9, 0, "P005", "P015", "CALL", "140s")  # P005 bridges the two clusters
add_communication(7, 13, 45, "P005", "P003", "MESSAGE", "Requesting update")

# ---- Filler communications among remaining persons (padding to ~70) ----
person_ids = [p["person_id"] for p in persons]
while len(communications) < 68:
    day = random.randint(0, 55)
    hour, minute = random.randint(6, 22), random.randint(0, 59)
    src, tgt = random.sample(person_ids, 2)
    ctype = random.choice(comm_types)
    case_for_pair = person_by_id[src]["case_id"] if person_by_id[src]["case_id"] == person_by_id[tgt]["case_id"] else "CASE001"
    add_communication(day, hour, minute, src, tgt, ctype,
                       f"auto-generated {ctype.lower()} content", case_id=case_for_pair,
                       with_evidence=(random.random() < 0.35))

# ===========================================================================
# TRANSACTIONS  (target ~45 rows)
# ===========================================================================

transactions = []
txn_counter = 1
currency = "FCT"  # fictional currency code, avoids real-world currency implication


def add_transaction(day, sender, receiver, amount, ttype, account, case_id="CASE001", suspicious=False, with_evidence=True):
    global txn_counter
    tid = f"T{txn_counter:03d}"
    txn_counter += 1
    timestamp = ts(day)
    eid = ""
    if with_evidence:
        eid = add_evidence(case_id, "TRANSACTION_RECORD", "Bank Ledger Export",
                            f"Transfer {sender}->{receiver} amount {amount} {currency}"
                            + (" (flagged as unusual pattern)" if suspicious else ""),
                            timestamp, tid)
    transactions.append({
        "transaction_id": tid, "case_id": case_id, "timestamp": timestamp,
        "sender_person_id": sender, "receiver_person_id": receiver, "amount": amount,
        "currency": currency, "transaction_type": ttype, "account_id": account,
        "evidence_id": eid,
    })
    return tid


# ---- Story transaction chain: P003 -> P007 -> P015 ----
add_transaction(8, "P003", "P007", 42000, "WIRE_TRANSFER", "ACC-P003-01", suspicious=True)
add_transaction(11, "P007", "P015", 41500, "WIRE_TRANSFER", "ACC-P007-01", suspicious=True)
# NOTE: deliberately no P002<->P020 transaction here -- their only connection
# must be the shared "Solace Freight Cooperative" organization family
# (O001 / O004), never a direct communication or transfer, so it remains a
# genuinely hidden (shared-organization-only) association.

while len(transactions) < 42:
    day = random.randint(0, 55)
    sender, receiver = random.sample(person_ids, 2)
    amount = random.choice([1500, 3000, 7500, 12000, 25000, 41000, 60000])
    ttype = random.choice(["WIRE_TRANSFER", "SALARY_PAYMENT", "CASH_DEPOSIT", "INVOICE_PAYMENT"])
    case_for_pair = person_by_id[sender]["case_id"] if person_by_id[sender]["case_id"] == person_by_id[receiver]["case_id"] else "CASE001"
    add_transaction(day, sender, receiver, amount, ttype, f"ACC-{sender}-01", case_id=case_for_pair,
                     suspicious=(amount >= 25000 and random.random() < 0.4),
                     with_evidence=(random.random() < 0.35))

# ===========================================================================
# EVENTS  (target ~60 rows)
# ===========================================================================

event_types = ["MEETING", "TRAVEL", "VISIT", "EMPLOYMENT", "INCIDENT", "OBSERVATION", "DELIVERY"]
vehicle_phrases = [
    "a grey delivery van", "a black sedan", "a rented white pickup truck",
    "a silver motorcycle", "an unmarked cargo truck",
]
events = []
event_counter = 1


def add_event(day, hour, etype, person, location, org, description, case_id="CASE001", with_evidence=True):
    global event_counter
    evid = f"EV{event_counter:03d}"
    event_counter += 1
    timestamp = ts(day, hour)
    eid = ""
    if with_evidence:
        eid = add_evidence(case_id, "OBSERVATION_LOG" if etype in ("OBSERVATION", "INCIDENT") else "DOCUMENT",
                            "Field Report", description, timestamp, evid)
    events.append({
        "event_id": evid, "case_id": case_id, "timestamp": timestamp, "event_type": etype,
        "person_id": person, "location_id": location, "organization_id": org,
        "description": description, "evidence_id": eid,
    })
    return evid


# ---- Story events for hidden associations ----
add_event(2, 18, "VISIT", "P001", "L005", "", "P001 observed entering Cinderlot Depot warehouse briefly.")
add_event(5, 19, "VISIT", "P010", "L005", "", "P010 observed at Cinderlot Depot loading dock in the evening.")
add_event(9, 20, "VISIT", "P003", "L009", "", "P003 checked into The Aldermere Inn for one night.")
add_event(11, 9, "VISIT", "P015", "L009", "", "P015 seen at The Aldermere Inn breakfast area.")
add_event(3, 8, "EMPLOYMENT", "P002", "L004", "O001", "P002 confirmed as staff at Solace Freight Cooperative HQ.")
add_event(6, 10, "EMPLOYMENT", "P020", "L004", "O004", "P020 confirmed as staff at Solace Freight Cooperative Millbrook Branch.")
add_event(20, 15, "TRAVEL", "P008", "L011", "", "P008 departed Aldenport Transit Hub in a rented white pickup truck.")
add_event(20, 16, "TRAVEL", "P022", "L011", "", "P022 arrived at Aldenport Transit Hub in a black sedan.")
add_event(4, 21, "DELIVERY", "P010", "L006", "O005", "P010 oversaw a delivery at Harrow's End Storage using an unmarked cargo truck.")
add_event(13, 17, "MEETING", "P006", "L008", "", "P006 met an unnamed contact at Cindermere Diner.")
add_event(14, 18, "MEETING", "P001", "L003", "O002", "P001 held a meeting at Northgate Trading Office.")
add_event(16, 12, "INCIDENT", "P005", "L007", "", "P005 involved in a minor dispute reported at Ravensbrook Meeting Hall.")

# ---- Filler events (padding to ~60) ----
while len(events) < 58:
    day = random.randint(0, 55)
    hour = random.randint(6, 22)
    etype = random.choice(event_types)
    person = random.choice(person_ids)
    location = random.choice(location_ids)
    org = random.choice([""] + [o["organization_id"] for o in organizations])
    case_for_person = person_by_id[person]["case_id"]
    desc_extra = ""
    if etype in ("TRAVEL", "DELIVERY") and random.random() < 0.2:
        desc_extra = f" Departed in {random.choice(vehicle_phrases)}."
    add_event(day, hour, etype, person, location, org,
              f"{etype.title()} event logged for {person} at {location}.{desc_extra}",
              case_id=case_for_person, with_evidence=(random.random() < 0.35))

# ===========================================================================
# EVIDENCE  (add standalone records not already tied to comm/txn/event,
# padding to ~55 total including the ones auto-created above)
# ===========================================================================

standalone_evidence_types = ["CCTV", "DOCUMENT", "DEVICE_LOG", "WITNESS_STATEMENT"]
while len(evidence_registry) < 55:
    case_id = random.choice(["CASE001", "CASE002"])
    etype = random.choice(standalone_evidence_types)
    related = random.choice(person_ids)
    day = random.randint(0, 55)
    timestamp = ts(day)
    add_evidence(case_id, etype,
                 "Field Camera" if etype == "CCTV" else "Case File",
                 f"{etype.replace('_', ' ').title()} concerning {related}.",
                 timestamp, related)

evidence = evidence_registry

# ===========================================================================
# CONSISTENCY VALIDATION
# ===========================================================================

person_ids_set = set(p["person_id"] for p in persons)
org_ids_set = set(o["organization_id"] for o in organizations)
loc_ids_set = set(location_ids)
case_ids_set = set(c["case_id"] for c in cases)
evidence_ids_set = set(e["evidence_id"] for e in evidence)

problems = []

for p in persons:
    if p["organization_id"] and p["organization_id"] not in org_ids_set:
        problems.append(f"person {p['person_id']} has invalid organization_id {p['organization_id']}")
    if p["location_id"] not in loc_ids_set:
        problems.append(f"person {p['person_id']} has invalid location_id {p['location_id']}")
    if p["case_id"] not in case_ids_set:
        problems.append(f"person {p['person_id']} has invalid case_id {p['case_id']}")

for o in organizations:
    if o["location_id"] not in loc_ids_set:
        problems.append(f"org {o['organization_id']} has invalid location_id {o['location_id']}")
    if o["case_id"] not in case_ids_set:
        problems.append(f"org {o['organization_id']} has invalid case_id {o['case_id']}")

for c in communications:
    if c["source_person_id"] not in person_ids_set or c["target_person_id"] not in person_ids_set:
        problems.append(f"communication {c['communication_id']} has invalid person reference")
    if c["evidence_id"] and c["evidence_id"] not in evidence_ids_set:
        problems.append(f"communication {c['communication_id']} has invalid evidence_id {c['evidence_id']}")

for t in transactions:
    if t["sender_person_id"] not in person_ids_set or t["receiver_person_id"] not in person_ids_set:
        problems.append(f"transaction {t['transaction_id']} has invalid person reference")
    if t["evidence_id"] and t["evidence_id"] not in evidence_ids_set:
        problems.append(f"transaction {t['transaction_id']} has invalid evidence_id {t['evidence_id']}")

for ev in events:
    if ev["person_id"] and ev["person_id"] not in person_ids_set:
        problems.append(f"event {ev['event_id']} has invalid person_id {ev['person_id']}")
    if ev["location_id"] and ev["location_id"] not in loc_ids_set:
        problems.append(f"event {ev['event_id']} has invalid location_id {ev['location_id']}")
    if ev["organization_id"] and ev["organization_id"] not in org_ids_set:
        problems.append(f"event {ev['event_id']} has invalid organization_id {ev['organization_id']}")
    if ev["evidence_id"] and ev["evidence_id"] not in evidence_ids_set:
        problems.append(f"event {ev['event_id']} has invalid evidence_id {ev['evidence_id']}")

for e in evidence:
    if e["case_id"] not in case_ids_set:
        problems.append(f"evidence {e['evidence_id']} has invalid case_id {e['case_id']}")

# duplicate ID checks
def check_dupes(rows, key, label):
    seen = set()
    for r in rows:
        if r[key] in seen:
            problems.append(f"duplicate {label} id: {r[key]}")
        seen.add(r[key])

check_dupes(persons, "person_id", "person")
check_dupes(organizations, "organization_id", "organization")
check_dupes(locations, "location_id", "location")
check_dupes(cases, "case_id", "case")
check_dupes(communications, "communication_id", "communication")
check_dupes(transactions, "transaction_id", "transaction")
check_dupes(events, "event_id", "event")
check_dupes(evidence, "evidence_id", "evidence")

print(f"Consistency check: {len(problems)} problem(s) found.")
for p in problems[:20]:
    print(" -", p)

# ===========================================================================
# SAVE CSVs
# ===========================================================================

save_csv("cases.csv", cases)
save_csv("persons.csv", persons)
save_csv("organizations.csv", organizations)
save_csv("locations.csv", locations)
save_csv("communications.csv", communications)
save_csv("transactions.csv", transactions)
save_csv("events.csv", events)
save_csv("evidence.csv", evidence)

print("\nRow counts:")
print(f"  cases: {len(cases)}")
print(f"  persons: {len(persons)}")
print(f"  organizations: {len(organizations)}")
print(f"  locations: {len(locations)}")
print(f"  communications: {len(communications)}")
print(f"  transactions: {len(transactions)}")
print(f"  events: {len(events)}")
print(f"  evidence: {len(evidence)}")

# ===========================================================================
# DERIVE graph_data.json FROM THE CSVs (not independently invented)
# ===========================================================================

ALLOWED_ENTITY_TYPES = {"PERSON", "PHONE", "EMAIL", "LOCATION", "ORGANIZATION",
                         "ACCOUNT", "VEHICLE", "CASE", "EVIDENCE"}
ALLOWED_REL_TYPES = {"KNOWS", "CALLED", "CONTACTED", "MET", "TRANSFERRED_MONEY",
                      "WORKS_FOR", "LOCATED_AT", "ASSOCIATED_WITH", "OWNS",
                      "TRAVELED_WITH", "COMMUNICATED_WITH"}

entities = {}
relationships = []


def add_entity(eid, etype, name, confidence, evidence_id=None):
    assert etype in ALLOWED_ENTITY_TYPES
    if eid in entities:
        return  # first occurrence wins; stable ID means later mentions merge automatically
    entities[eid] = {"id": eid, "type": etype, "name": name, "confidence": confidence, "evidence_id": evidence_id}


def add_relationship(source, target, rtype, confidence, evidence_id=None, timestamp=None):
    assert rtype in ALLOWED_REL_TYPES
    relationships.append({
        "source": source, "target": target, "type": rtype,
        "confidence": confidence, "evidence_id": evidence_id, "timestamp": timestamp,
    })


# --- CASE entities ---
for c in cases:
    add_entity(f"CASE:{c['case_id']}", "CASE", c["case_name"], 1.0)

# --- PERSON / PHONE / EMAIL entities + WORKS_FOR / LOCATED_AT relationships ---
for p in persons:
    pid = f"PERSON:{p['person_id']}"
    add_entity(pid, "PERSON", p["name"], 1.0)

    phone_norm = re.sub(r"\D", "", p["phone"])
    if phone_norm:
        phone_id = f"PHONE:{phone_norm}"
        add_entity(phone_id, "PHONE", phone_norm, 1.0)
        add_relationship(pid, phone_id, "ASSOCIATED_WITH", 1.0)

    email_norm = p["email"].strip().lower()
    if email_norm:
        email_id = f"EMAIL:{email_norm}"
        add_entity(email_id, "EMAIL", email_norm, 1.0)
        add_relationship(pid, email_id, "ASSOCIATED_WITH", 1.0)

    if p["organization_id"]:
        org_id = f"ORGANIZATION:{p['organization_id']}"
        add_relationship(pid, org_id, "WORKS_FOR", 1.0)

    if p["location_id"]:
        loc_id = f"LOCATION:{p['location_id']}"
        add_relationship(pid, loc_id, "LOCATED_AT", 1.0)

# --- ORGANIZATION entities + LOCATED_AT ---
for o in organizations:
    org_id = f"ORGANIZATION:{o['organization_id']}"
    add_entity(org_id, "ORGANIZATION", o["organization_name"], 1.0)
    if o["location_id"]:
        add_relationship(org_id, f"LOCATION:{o['location_id']}", "LOCATED_AT", 1.0)

# --- LOCATION entities ---
for l in locations:
    add_entity(f"LOCATION:{l['location_id']}", "LOCATION", l["location_name"], 1.0)

# --- EVIDENCE entities ---
for e in evidence:
    add_entity(f"EVIDENCE:{e['evidence_id']}", "EVIDENCE", e["evidence_id"], 1.0, evidence_id=e["evidence_id"])

# --- Communication relationships ---
COMM_TYPE_MAP = {"CALL": "CALLED", "MESSAGE": "CONTACTED", "EMAIL": "COMMUNICATED_WITH"}
for c in communications:
    rtype = COMM_TYPE_MAP[c["communication_type"]]
    add_relationship(
        f"PERSON:{c['source_person_id']}", f"PERSON:{c['target_person_id']}", rtype,
        1.0, evidence_id=(c["evidence_id"] or None), timestamp=c["timestamp"],
    )

# --- Transaction relationships (TRANSFERRED_MONEY + OWNS on account) ---
for t in transactions:
    add_relationship(
        f"PERSON:{t['sender_person_id']}", f"PERSON:{t['receiver_person_id']}", "TRANSFERRED_MONEY",
        1.0, evidence_id=(t["evidence_id"] or None), timestamp=t["timestamp"],
    )
    acc_id = f"ACCOUNT:{t['account_id']}"
    add_entity(acc_id, "ACCOUNT", t["account_id"], 1.0, evidence_id=(t["evidence_id"] or None))
    add_relationship(f"PERSON:{t['sender_person_id']}", acc_id, "OWNS", 1.0,
                      evidence_id=(t["evidence_id"] or None), timestamp=t["timestamp"])

# --- VEHICLE entities: extracted from event free text only where a vehicle
# phrase actually appears (never fabricated), confidence lowered since this
# is text-derived, not from a dedicated column. ---
vehicle_pattern = re.compile(
    r"\b(a|an)\s+((?:grey|black|white|silver|rented|unmarked)\s+(?:delivery van|sedan|pickup truck|motorcycle|cargo truck))\b",
    re.IGNORECASE,
)
vehicle_hits = 0
for ev in events:
    match = vehicle_pattern.search(ev["description"])
    if match:
        vehicle_text = match.group(2).strip()
        vehicle_key = re.sub(r"\s+", "_", vehicle_text.lower())
        vehicle_id = f"VEHICLE:{vehicle_key}"
        add_entity(vehicle_id, "VEHICLE", vehicle_text, 0.6, evidence_id=ev["evidence_id"])
        if ev["person_id"]:
            add_relationship(f"PERSON:{ev['person_id']}", vehicle_id, "ASSOCIATED_WITH", 0.6,
                              evidence_id=ev["evidence_id"], timestamp=ev["timestamp"])
        vehicle_hits += 1

print(f"\nVEHICLE entities extracted from event free text: {vehicle_hits}")

graph_data = {"entities": list(entities.values()), "relationships": relationships}

with open(os.path.join(OUT_DIR, "graph_data.json"), "w", encoding="utf-8") as f:
    json.dump(graph_data, f, indent=2)

print(f"\ngraph_data.json: {len(graph_data['entities'])} entities, {len(graph_data['relationships'])} relationships")

# Final graph_data.json consistency check: every source/target must resolve
# to an entity id present in the entities list.
entity_ids = set(entities.keys())
bad_rels = [r for r in relationships if r["source"] not in entity_ids or r["target"] not in entity_ids]
print(f"graph_data.json relationships with dangling source/target: {len(bad_rels)}")

# Mock Neo4j service

def get_case_graph(case_id: int):

    return {
        "case_id": case_id,
        "nodes": [
            {"id": "P001", "label": "Suspect A", "type": "Person"},
            {"id": "P002", "label": "Suspect B", "type": "Person"},
            {"id": "P003", "label": "Victim", "type": "Person"}
        ],
        "edges": [
            {"source": "P001", "target": "P002", "relation": "CALL"},
            {"source": "P002", "target": "P003", "relation": "KNOWS"}
        ]
    }


def find_shortest_path(source: str, target: str):

    return {
        "source": source,
        "target": target,
        "path": ["P001", "P002", "P003"],
        "length": 2
    }
from fastapi import APIRouter

router = APIRouter()

# Temporary entity storage
entities = [
    {
        "id": "P001",
        "name": "Suspect A",
        "type": "Person",
        "age": 32
    },
    {
        "id": "P002",
        "name": "Suspect B",
        "type": "Person",
        "age": 28
    },
    {
        "id": "P003",
        "name": "Victim",
        "type": "Person",
        "age": 40
    }
]


# Search entities by name
@router.get("/entities/search-by-name")
def search_entities(q: str):
    result = []

    for entity in entities:
        if q.lower() in entity["name"].lower():
            result.append(entity)

    return result


# Get one entity
@router.get("/entities/{entity_id}")
def get_entity(entity_id: str):
    for entity in entities:
        if entity["id"] == entity_id:
            return entity

    return {"message": "Entity not found"}


# Get connections of an entity
@router.get("/entities/{entity_id}/connections")
def get_connections(entity_id: str):

    connections = {
        "P001": [
            {
                "connected_to": "P002",
                "name": "Suspect B",
                "relation": "CALL"
            }
        ],
        "P002": [
            {
                "connected_to": "P003",
                "name": "Victim",
                "relation": "KNOWS"
            }
        ]
    }

    return connections.get(entity_id, [])
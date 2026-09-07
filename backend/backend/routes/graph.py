from fastapi import APIRouter
from services.neo4j_service import (
    get_case_graph,
    find_shortest_path
)

router = APIRouter()

# STATIC ROUTE FIRST
@router.get("/graph/path")
def shortest_path(source: str, target: str):
    return find_shortest_path(source, target)

# DYNAMIC ROUTE SECOND
@router.get("/graph/{case_id}")
def graph(case_id: int):
    return get_case_graph(case_id)
from typing import Dict, Any
from neo4j import GraphDatabase, Driver

class GraphFeatureExtractor:
    def __init__(self, uri: str = "neo4j://127.0.0.1:7687", auth: tuple = ("neo4j", "password"), database: str = "neo4j"):
        self.driver: Driver = GraphDatabase.driver(uri, auth=auth)
        self.database = database

    def close(self):
        if self.driver:
            self.driver.close()

    def extract_features(self, source_id: str, target_id: str) -> Dict[str, Any]:
        query = """
        MATCH (a:Entity {id: $source_id}), (b:Entity {id: $target_id})
        
        OPTIONAL MATCH (a)-(an:Entity)
        OPTIONAL MATCH (b)-(bn:Entity)
        WITH a, b, collect(DISTINCT an) AS a_neighbors, collect(DISTINCT bn) AS b_neighbors
        
        WITH a, b, a_neighbors, b_neighbors,
             [n IN a_neighbors WHERE n IN b_neighbors] AS common_nodes
             
        OPTIONAL MATCH path = shortestPath((a)-[*..5]-(b))
        OPTIONAL MATCH (a)-[dir_r]-(b)
        
        RETURN 
            size(common_nodes) AS common_neighbors_count,
            [n IN common_nodes | {id: n.id, name: n.name, type: n.type}] AS common_neighbors,
            size(a_neighbors) AS a_count,
            size(b_neighbors) AS b_count,
            [n IN nodes(path) | n.id] AS path_ids,
            length(path) AS hops,
            count(dir_r) > 0 AS is_directly_connected
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query, source_id=source_id, target_id=target_id).single()
            if not result:
                return self._empty_features(source_id, target_id)

            common_cnt = result["common_neighbors_count"] or 0
            a_cnt = result["a_count"] or 0
            b_cnt = result["b_count"] or 0
            union_cnt = a_cnt + b_cnt - common_cnt
            jaccard = float(common_cnt) / union_cnt if union_cnt > 0 else 0.0

            common_nodes = result["common_neighbors"] or []
            shared_locs = [n for n in common_nodes if n.get("type") == "Location"]
            shared_orgs = [n for n in common_nodes if n.get("type") == "Organization"]

            return {
                "source_id": source_id,
                "target_id": target_id,
                "common_neighbors_count": common_cnt,
                "common_neighbors": common_nodes,
                "jaccard_similarity": round(jaccard, 4),
                "shortest_path": result["path_ids"] or [],
                "number_of_hops": result["hops"],
                "shared_locations": shared_locs,
                "shared_organizations": shared_orgs,
                "is_directly_connected": result["is_directly_connected"]
            }

    def _empty_features(self, source_id: str, target_id: str) -> Dict[str, Any]:
        return {
            "source_id": source_id,
            "target_id": target_id,
            "common_neighbors_count": 0,
            "common_neighbors": [],
            "jaccard_similarity": 0.0,
            "shortest_path": [],
            "number_of_hops": None,
            "shared_locations": [],
            "shared_organizations": [],
            "is_directly_connected": False
        }

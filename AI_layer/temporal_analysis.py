from datetime import datetime
from typing import Dict, Any
from neo4j import GraphDatabase, Driver

class TemporalAnalyzer:
    def __init__(self, uri: str = "neo4j://127.0.0.1:7687", auth: tuple = ("neo4j", "password"), database: str = "neo4j"):
        self.driver: Driver = GraphDatabase.driver(uri, auth=auth)
        self.database = database

    def close(self):
        if self.driver:
            self.driver.close()

    def analyze_temporal_proximity(self, source_id: str, target_id: str) -> Dict[str, Any]:
        query = """
        MATCH (a:Entity {id: $source_id})-[r1]-(intermediate:Entity)-[r2]-(b:Entity {id: $target_id})
        WHERE r1.timestamp IS NOT NULL AND r2.timestamp IS NOT NULL
        RETURN 
            r1.timestamp AS t1,
            r2.timestamp AS t2,
            r1.evidence_id AS ev1,
            r2.evidence_id AS ev2
        """
        timestamps = []
        evidence_ids = set()
        time_diffs_days = []

        with self.driver.session(database=self.database) as session:
            results = session.run(query, source_id=source_id, target_id=target_id)
            for record in results:
                if record["ev1"]: evidence_ids.add(str(record["ev1"]))
                if record["ev2"]: evidence_ids.add(str(record["ev2"]))

                t1_str = str(record["t1"])
                t2_str = str(record["t2"])
                timestamps.extend([t1_str, t2_str])

                try:
                    dt1 = datetime.fromisoformat(t1_str.replace("Z", "+00:00"))
                    dt2 = datetime.fromisoformat(t2_str.replace("Z", "+00:00"))
                    diff = abs((dt2 - dt1).total_seconds()) / 86400.0
                    time_diffs_days.append(diff)
                except Exception:
                    continue

        min_diff = min(time_diffs_days) if time_diffs_days else None
        
        if min_diff is None:
            temporal_score = 0.1
        elif min_diff <= 1.0:
            temporal_score = 0.95
        elif min_diff <= 7.0:
            temporal_score = 0.80
        elif min_diff <= 30.0:
            temporal_score = 0.50
        else:
            temporal_score = 0.20

        return {
            "min_day_gap": round(min_diff, 2) if min_diff is not None else None,
            "temporal_proximity_score": temporal_score,
            "timestamps": sorted(list(set(timestamps))),
            "evidence_ids": sorted(list(evidence_ids))
        }

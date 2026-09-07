from typing import Dict, Any
from ai.graph_features import GraphFeatureExtractor
from ai.temporal_analysis import TemporalAnalyzer
from ai.link_prediction import LinkPredictor
from ai.explanation import ExplainableAI

class AIService:
    def __init__(self, uri: str = "neo4j://127.0.0.1:7687", auth: tuple = ("neo4j", "password"), database: str = "neo4j"):
        self.uri = uri
        self.auth = auth
        self.database = database
        self.feature_extractor = GraphFeatureExtractor(uri, auth, database)
        self.temporal_analyzer = TemporalAnalyzer(uri, auth, database)
        self.link_predictor = LinkPredictor()
        self.explainer = ExplainableAI()

    def close(self):
        self.feature_extractor.close()
        self.temporal_analyzer.close()

    def predict_link_between_entities(self, source_id: str, target_id: str) -> Dict[str, Any]:
        graph_feats = self.feature_extractor.extract_features(source_id, target_id)
        temp_info = self.temporal_analyzer.analyze_temporal_proximity(source_id, target_id)
        prediction_res = self.link_predictor.predict_link(graph_feats, temp_info)
        reasons = self.explainer.generate_explanation(graph_feats, temp_info, prediction_res)

        return {
            "source": source_id,
            "target": target_id,
            "prediction": prediction_res["prediction"],
            "confidence": prediction_res["confidence"],
            "reasons": reasons,
            "supporting_path": graph_feats.get("shortest_path", []),
            "evidence_ids": temp_info.get("evidence_ids", [])
        }

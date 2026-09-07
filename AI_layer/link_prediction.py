import math
from typing import Dict, Any

class LinkPredictor:
    def predict_link(self, features: Dict[str, Any], temporal_info: Dict[str, Any]) -> Dict[str, Any]:
        common_cnt = features.get("common_neighbors_count", 0)
        jaccard = features.get("jaccard_similarity", 0.0)
        hops = features.get("number_of_hops")
        shared_orgs = len(features.get("shared_organizations", []))
        shared_locs = len(features.get("shared_locations", []))
        temp_score = temporal_info.get("temporal_proximity_score", 0.1)

        if hops is None:
            hop_score = 0.0
        elif hops == 1:
            hop_score = 1.0
        elif hops == 2:
            hop_score = 0.8
        elif hops == 3:
            hop_score = 0.4
        else:
            hop_score = 0.1

        logit = (
            -2.5 +
            (1.2 * min(common_cnt, 5)) +
            (2.5 * jaccard) +
            (1.8 * hop_score) +
            (1.5 * shared_orgs) +
            (1.2 * shared_locs) +
            (1.4 * temp_score)
        )

        probability = 1.0 / (1.0 + math.exp(-logit))
        confidence = round(probability, 4)

        if confidence >= 0.70:
            prediction = "HIGH_PROBABILITY_ASSOCIATION"
        elif confidence >= 0.40:
            prediction = "POTENTIAL_ASSOCIATION"
        else:
            prediction = "LOW_PROBABILITY_ASSOCIATION"

        return {
            "prediction": prediction,
            "confidence": confidence,
            "raw_signals": {
                "common_neighbors_count": common_cnt,
                "jaccard_similarity": jaccard,
                "hop_score": hop_score,
                "shared_orgs_count": shared_orgs,
                "shared_locs_count": shared_locs,
                "temporal_proximity_score": temp_score
            }
        }

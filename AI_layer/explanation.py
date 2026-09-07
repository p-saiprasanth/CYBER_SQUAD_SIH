from typing import Dict, List, Any

class ExplainableAI:
    def generate_explanation(self, features: Dict[str, Any], temporal_info: Dict[str, Any], prediction: Dict[str, Any]) -> List[str]:
        reasons = []

        common_cnt = features.get("common_neighbors_count", 0)
        if common_cnt > 0:
            reasons.append(f"{common_cnt} common connection(s) identified in the network")

        shared_orgs = features.get("shared_organizations", [])
        if shared_orgs:
            org_names = ", ".join([o.get("name", "Unknown") for o in shared_orgs])
            reasons.append(f"Shared organization affiliation: {org_names}")

        shared_locs = features.get("shared_locations", [])
        if shared_locs:
            loc_names = ", ".join([l.get("name", "Unknown") for l in shared_locs])
            reasons.append(f"Mutual presence at location(s): {loc_names}")

        hops = features.get("number_of_hops")
        if hops is not None:
            reasons.append(f"{hops}-hop connection path detected in graph structure")

        day_gap = temporal_info.get("min_day_gap")
        if day_gap is not None:
            if day_gap <= 1.0:
                reasons.append("High temporal proximity: Interactions occurred within 24 hours of each other")
            elif day_gap <= 7.0:
                reasons.append(f"Temporal proximity: Activity window spans {day_gap} days")

        jaccard = features.get("jaccard_similarity", 0.0)
        if jaccard > 0.3:
            reasons.append(f"Strong network similarity index ({jaccard * 100:.1f}% neighborhood overlap)")

        if not reasons:
            reasons.append("Low overall structural and temporal correlation detected between entities")

        return reasons

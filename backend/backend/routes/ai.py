from fastapi import APIRouter

router = APIRouter()


@router.post("/ai/predict-link")
def predict_link(data: dict):

    source = data.get("source_entity")
    target = data.get("target_entity")

    return {
        "source_entity": source,
        "target_entity": target,
        "prediction": "POTENTIAL_ASSOCIATION",
        "confidence": 0.87,
        "reasons": [
            "Frequent phone communication",
            "Shared location history"
        ],
        "supporting_paths": [
            ["P001", "P002", "P003"]
        ],
        "supporting_evidence": [
            "EV001",
            "EV014"
        ]
    }


@router.post("/ai/explain")
def explain_prediction(data: dict):

    source = data.get("source_entity")
    target = data.get("target_entity")

    return {
        "source_entity": source,
        "target_entity": target,
        "explanation": "The entities are likely connected because of repeated phone calls, common location visits, and shared evidence collected during investigation.",
        "confidence_reason": "High confidence due to multiple supporting relationships in the graph."
    }
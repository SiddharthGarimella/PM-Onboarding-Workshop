import os
import json

PREDICTIONS_DIR = "predictions"
CONF_THRESHOLD = 0.90  # predictions at or above this confidence are trusted automatically


def top_prediction(prediction_file_data):
    """Each scene's prediction file lists every possible item with a confidence
    score. The classifier's actual "guess" for what's on the shelf is whichever
    item has the highest confidence -- that's what the threshold policy judges."""
    return max(prediction_file_data["predictions"], key=lambda p: p["confidence"])


def main():
    accepted = []
    uncertain = []
    audit_events = []

    for filename in sorted(os.listdir(PREDICTIONS_DIR)):
        with open(os.path.join(PREDICTIONS_DIR, filename)) as f:
            data = json.load(f)

        scene_id = data["scene_id"]
        top = top_prediction(data)

        record = {
            "scene_id": scene_id,
            "name": top["name"],
            "confidence": top["confidence"],
        }

        if top["confidence"] >= CONF_THRESHOLD:
            accepted.append(record)
        else:
            uncertain.append(record)
            audit_events.append({
                "scene_id": scene_id,
                "item": top["name"],
                "confidence": top["confidence"],
                "event_type": "UNCERTAIN",
                "recommended_action": "Manual review required — confidence below threshold",
            })

    # Save outputs so Deliverable 3 (reconciliation) can read them without
    # re-running the classifier.
    with open("accepted_predictions.json", "w") as f:
        json.dump(accepted, f, indent=2)

    with open("uncertain_predictions.json", "w") as f:
        json.dump(uncertain, f, indent=2)

    print(f"Accepted predictions: {len(accepted)}")
    print(f"Uncertain predictions: {len(uncertain)}")

    print("\nUncertain items per scene:")
    for record in uncertain:
        print(f"  {record['scene_id']}: {record['name']} (confidence {record['confidence']})")

    print(f"\nAudit events generated: {len(audit_events)}")
    for event in audit_events:
        print(f"  {event}")


if __name__ == "__main__":
    main()

import json
import requests
from datetime import datetime, timezone

API_URL = "http://localhost:3001/inventory"
AUDIT_LOG_PATH = "audit_log.jsonl"


def load_predictions(path):
    with open(path) as f:
        return json.load(f)


def get_inventory_snapshot():
    """Pull the current declared truth (the database) via the same GET /inventory
    endpoint the React dashboard uses. Build a lookup by item name so predictions
    can be matched against it."""
    response = requests.get(API_URL)
    items = response.json()
    return {item["name"]: item for item in items}


def reconcile(accepted, uncertain, inventory_by_name):
    events = []
    now = datetime.now(timezone.utc).isoformat()

    # Accepted predictions get compared against declared inventory truth.
    for pred in accepted:
        item_name = pred["name"]
        db_item = inventory_by_name.get(item_name)

        if db_item is not None and db_item["quantity"] > 0:
            event_type = "VERIFIED"
            recommended_action = "No action needed — matches declared inventory"
        else:
            # Either the item isn't in the database at all, or the database
            # says it's out of stock (quantity 0) -- but the image says otherwise.
            event_type = "DISCREPANCY"
            recommended_action = "Review and update inventory record — image shows item present but database disagrees"

        events.append({
            "timestamp": now,
            "scene_id": pred["scene_id"],
            "item": item_name,
            "event_type": event_type,
            "confidence": pred["confidence"],
            "recommended_action": recommended_action,
        })

    # Uncertain predictions were already flagged in Deliverable 2 -- carry
    # them through to the same audit log with a consistent shape.
    for pred in uncertain:
        events.append({
            "timestamp": now,
            "scene_id": pred["scene_id"],
            "item": pred["name"],
            "event_type": "UNCERTAIN",
            "confidence": pred["confidence"],
            "recommended_action": "Manual review required — confidence below threshold",
        })

    return events


def main():
    accepted = load_predictions("accepted_predictions.json")
    uncertain = load_predictions("uncertain_predictions.json")
    inventory_by_name = get_inventory_snapshot()

    events = reconcile(accepted, uncertain, inventory_by_name)

    with open(AUDIT_LOG_PATH, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    verified = [e for e in events if e["event_type"] == "VERIFIED"]
    discrepancies = [e for e in events if e["event_type"] == "DISCREPANCY"]
    uncertain_events = [e for e in events if e["event_type"] == "UNCERTAIN"]

    print(f"VERIFIED: {len(verified)}")
    print(f"DISCREPANCY: {len(discrepancies)}")
    print(f"UNCERTAIN: {len(uncertain_events)}")

    if discrepancies:
        print("\nDiscrepancies flagged:")
        for e in discrepancies:
            print(f"  {e['scene_id']}: {e['item']} (confidence {e['confidence']})")

    print(f"\nAudit log written to {AUDIT_LOG_PATH} ({len(events)} events)")


if __name__ == "__main__":
    main()

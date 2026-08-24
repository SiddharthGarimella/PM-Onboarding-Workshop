import os
import json
import numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression

DATASET_DIR = "shelf_dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_DIR = os.path.join(DATASET_DIR, "labels")
PREDICTIONS_DIR = "predictions"
IMG_SIZE = (32, 32)  # small + fixed size keeps feature extraction simple


def extract_features(image_path):
    """Resize to a fixed small size and flatten pixels into a 1D feature vector.
    This is intentionally simple -- the goal is a working pipeline, not accuracy:
    read image -> extract simple features -> train model -> output predictions."""
    img = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
    return np.array(img).flatten() / 255.0  # normalize pixel values to 0-1


def main():
    os.makedirs(PREDICTIONS_DIR, exist_ok=True)

    scene_ids = []
    X = []
    y_labels = []

    for filename in sorted(os.listdir(IMAGES_DIR)):
        scene_id = os.path.splitext(filename)[0]
        label_path = os.path.join(LABELS_DIR, f"{scene_id}.json")
        if not os.path.exists(label_path):
            continue  # skip images without a matching label file

        with open(label_path) as f:
            label_data = json.load(f)

        scene_ids.append(scene_id)
        X.append(extract_features(os.path.join(IMAGES_DIR, filename)))
        # This dataset labels each scene with a single item ("item_type"),
        # not a list -- one item per shelf photo.
        y_labels.append(label_data["item_type"])

    X = np.array(X)

    # Single-label classification: predict_proba naturally returns a
    # confidence score for every possible item, not just the top pick.
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y_labels)

    probs = model.predict_proba(X)

    for scene_id, prob_row in zip(scene_ids, probs):
        predictions = [
            {"name": item, "confidence": round(float(p), 2)}
            for item, p in zip(model.classes_, prob_row)
        ]
        predictions.sort(key=lambda p: p["confidence"], reverse=True)

        output = {"scene_id": scene_id, "predictions": predictions}

        out_path = os.path.join(PREDICTIONS_DIR, f"{scene_id}.json")
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2)

    print(f"Wrote {len(scene_ids)} prediction files to {PREDICTIONS_DIR}/")


if __name__ == "__main__":
    main()

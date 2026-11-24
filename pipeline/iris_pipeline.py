import json
from pathlib import Path
import joblib
from kfp import compiler, dsl
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["scikit-learn", "joblib"],
)
def load_and_preprocess(dataset_out: dsl.Output[dsl.Artifact]):
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    out_dir = Path(dataset_out.path)
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "X_train": X_train_scaled,
            "X_test": X_test_scaled,
            "y_train": y_train,
            "y_test": y_test,
        },
        out_dir / "iris_data.joblib",
    )


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["scikit-learn", "joblib"],
)
def train_model(
    dataset_in: dsl.Input[dsl.Artifact],
    model_out: dsl.Output[dsl.Model],
):
    data = joblib.load(Path(dataset_in.path) / "iris_data.joblib")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(data["X_train"], data["y_train"])

    out_dir = Path(model_out.path)
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, out_dir / "iris_model.joblib")


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["scikit-learn", "joblib"],
)
def evaluate_model(
    dataset_in: dsl.Input[dsl.Artifact],
    model_in: dsl.Input[dsl.Model],
    metrics_out: dsl.Output[dsl.Metrics],
):
    data = joblib.load(Path(dataset_in.path) / "iris_data.joblib")
    clf = joblib.load(Path(model_in.path) / "iris_model.joblib")
    preds = clf.predict(data["X_test"])
    acc = float(accuracy_score(data["y_test"], preds))

    metrics_out.log_metric("accuracy", acc)
    Path(metrics_out.path).write_text(json.dumps({"accuracy": acc}, indent=2))


@dsl.pipeline(
    name="iris-classification-pipeline",
    description="Load/preprocess Iris data, train model, and evaluate accuracy.",
)
def iris_pipeline():
    prep = load_and_preprocess()
    train = train_model(dataset_in=prep.outputs["dataset_out"])
    evaluate_model(
        dataset_in=prep.outputs["dataset_out"],
        model_in=train.outputs["model_out"],
    )


if __name__ == "__main__":
    out_yaml = Path(__file__).resolve().parent / "iris_pipeline.yaml"
    compiler.Compiler().compile(pipeline_func=iris_pipeline, package_path=str(out_yaml))
    print(f"Compiled pipeline to {out_yaml}")

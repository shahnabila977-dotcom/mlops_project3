import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("iris-k8s-deployment")

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

model_name = "iris-classifier"

with mlflow.start_run():
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = float(accuracy_score(y_test, clf.predict(X_test)))

    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(
        clf,
        name="model",
        registered_model_name=model_name,
        skops_trusted_types=["sklearn.tree._tree.Tree"],
    )

client = MlflowClient()
versions = client.search_model_versions(f"name='{model_name}'")
latest_version = max(int(v.version) for v in versions)

client.transition_model_version_stage(
    name=model_name,
    version=str(latest_version),
    stage="Staging",
    archive_existing_versions=False,
)
client.transition_model_version_stage(
    name=model_name,
    version=str(latest_version),
    stage="Production",
    archive_existing_versions=True,
)
print(f"Registered {model_name} v{latest_version} and transitioned Staging -> Production (acc={acc:.4f})")

pipeline {
    agent any
    stages {
        stage('Compile ML Pipeline') {
            steps {
                sh 'python3 pipeline/iris_pipeline.py'
            }
        }
        stage('Register Model in MLflow') {
            steps {
                sh 'cd pipeline && python3 register_model.py'
            }
        }
        stage('Validate Kustomize Manifests') {
            steps {
                sh 'kubectl kustomize manifests'
            }
        }
    }
}

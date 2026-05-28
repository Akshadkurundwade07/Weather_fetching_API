pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python packages...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v
                '''
            }
        }

        stage('Start App') {
            steps {
                echo 'Starting FastAPI server...'
                sh '''
                    . venv/bin/activate
                    nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
                    sleep 3
                    echo "App started on port 8000"
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Checking if app is running...'
                sh 'curl -f http://localhost:8000/health'
            }
        }
    }

    post {
        success {
            echo 'Pipeline passed! App is live at http://localhost:8000'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}

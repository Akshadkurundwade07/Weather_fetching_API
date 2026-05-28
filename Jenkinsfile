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
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat '''
                    call venv\\Scripts\\activate
                    pytest test_main.py -v
                '''
            }
        }

        stage('Start App') {
            steps {
                echo 'Starting FastAPI server...'
                bat '''
                    call venv\\Scripts\\activate
                    start /B uvicorn main:app --host 0.0.0.0 --port 8000
                    timeout /t 3
                    echo App started on port 8000
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Checking if app is running...'
                bat 'curl -f http://localhost:8000/health'
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
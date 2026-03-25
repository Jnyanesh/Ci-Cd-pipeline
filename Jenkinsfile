pipeline {
    agent any 

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-flask-app:${env.BUILD_ID} .'
            }
        }
        stage('Test') {
            steps {
                // Example: simple check to see if the container starts
                sh 'docker run -d --name test-container -p 5000:5000 my-flask-app:${env.BUILD_ID}'
                sh 'sleep 5 && curl http://localhost:5000'
                sh 'docker rm -f test-container'
            }
        }
        stage('Push to Registry') {
            steps {
                // You would typically login and push to Docker Hub here
                echo 'Pushing image to repository...'
            }
        }
    }
}

pipeline {
    agent any 

    // This tells Jenkins to look for GitHub Webhooks
    triggers {
        githubPush()
    }

    environment {
        DOCKER_USER  = 'jnyanesh1' 
        IMAGE_NAME   = 'simple-ci-cd-pipeline-app'
        DOCKER_CREDS  = 'docker-hub-credentials' 
    }

    stages {
        stage('Checkout') {
            steps {
                // 'scm' ensures it pulls the exact commit that triggered the webhook
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building version: ${env.BUILD_ID}"
                    sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${env.BUILD_ID} ."
                    sh "docker tag ${DOCKER_USER}/${IMAGE_NAME}:${env.BUILD_ID} ${DOCKER_USER}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh "docker rm -f test-container || true"
                    sh "docker run -d --name test-container -p 5000:5000 ${DOCKER_USER}/${IMAGE_NAME}:${env.BUILD_ID}"
                    try {
                        // Health check: wait for Flask to boot
                        sh 'sleep 5 && curl http://localhost:5000'
                    } finally {
                        sh 'docker rm -f test-container'
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // This is the "Automated Push" part
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER_ENV')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER_ENV --password-stdin"
                    sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${env.BUILD_ID}"
                    sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        always {
            // Housekeeping: remove local images so the lab machine doesn't get full
            sh "docker rmi -f ${DOCKER_USER}/${IMAGE_NAME}:${env.BUILD_ID} ${DOCKER_USER}/${IMAGE_NAME}:latest || true"
        }
    }
}

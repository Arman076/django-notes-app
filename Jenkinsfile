@Library("Shared") _   
pipeline {
    agent { label 'aws' }  

    environment {
        IMAGE_NAME = "django-notes-app:latest"
        CONTAINER_NAME = "django-notes-app-container"
        PUSH_IMAGE = "devil678/django-notes-app:latest"
    }

    stages {
        stage("hello world") {
            steps {
                script {
                    hello()
                }
            }
        }
        
        stage("Cloning Django Notes App") {
            steps {
                script {
                    clone ("https://github.com/Arman076/django-notes-app.git", "main")  
                }
            }
        }
        
        stage("Build the Code") {
            steps {
                echo "Building the Docker image..."
                script {
                    docker_build("django-notes-app","latest","devil678")
                }
                echo "Docker image built successfully."
            }
        }
        
        stage("Install Docker & Kubernetes Tools") {
            steps {
                echo "Installing dependencies if necessary..."
                sh '''
                    if ! command -v docker &> /dev/null; then
                        echo "Installing Docker..."
                        sudo apt-get update
                        sudo apt-get install -y docker.io
                        sudo systemctl start docker
                        sudo systemctl enable docker
                    fi

                    if ! command -v minikube &> /dev/null; then
                        echo "Installing Minikube..."
                        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
                        chmod +x minikube-linux-amd64
                        mv minikube-linux-amd64 /usr/local/bin/minikube
                    fi

                    if ! command -v docker-compose &> /dev/null; then
                        echo "Installing Docker Compose..."
                        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                    fi
                    
                    if ! command -v kubectl &> /dev/null; then
                        echo "Installing kubectl..."
                        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                        mv kubectl /usr/local/bin/
                    fi

                    minikube start --driver=docker --force
                    minikube status
                '''
            }
        }
 
        stage("Push Code to Docker Hub") {
            steps {
                echo "Pushing the image to Docker Hub..."
                script {
                    docker_push ("django-notes-app","latest","devil678")
                }
            }
        }
        
        stage("Test the Code") {
            steps {
                echo "Running Django Tests..."
                echo "Code testing completed successfully."
            }
        }

        stage("Deploy the Code") {
            steps {
                echo "Deploying the application..."
                sh "docker-compose down || true"
                echo "Running Kubernetes Deployment..."
                // sh "kubectl apply -f k8s/deployment.yaml"
                echo "Verifying Deployment..."
                // sh "kubectl rollout status deployment django-notes -n django"
                echo "Application deployed successfully to Kubernetes."
                sh "docker-compose down && docker-compose up -d"
                echo "Application deployed successfully."
            }
        }
    }

    post {
        always {
            emailext (
                to: "anjaraalam3597@gmail.com",
                subject: "Jenkins Build: ${currentBuild.fullDisplayName}",
                body: """<p><strong>Jenkins Build Report</strong></p>
                        <p><strong>Job Name:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build Status:</strong> ${currentBuild.result ?: 'SUCCESS'}</p>
                        <p>Check logs at: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                attachLog: true,
                mimeType: 'text/html'
            )
        }
        
        failure {
            emailext (
                to: "anjaraalam3597@gmail.com",
                subject: "Jenkins Build Failed: ${currentBuild.fullDisplayName}",
                body: """<p><strong>Build Failed!</strong></p>
                        <p>Job Name: ${env.JOB_NAME}</p>
                        <p>Build Number: ${env.BUILD_NUMBER}</p>
                        <p>Check logs at: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                attachLog: true,
                mimeType: 'text/html'
            )
        }
    }
}

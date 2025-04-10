@Library("Shared") _   
pipeline {
    agent any

    environment {
        IMAGE_NAME = "django-notes-app:latest"
        CONTAINER_NAME = "django-notes-app-container"
        PUSH_IMAGE = "devil678/django-notes-app:latest"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"  // Add this line
        SONAR_TOKEN = credentials('sonar-token')
        SONAR_PROJECT_KEY = "django-notes-app"
        
    }

    stages {
        stage("Hello World") {
            steps {
                script {
                    hello()
                }
            }
        }

        stage("Cleanup WorkSpace") {
            steps {
                cleanWs()
            }
        }
        
       stage("SonarQube Code Quality Analysis") {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_HOST_URL \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        
        stage("Cloning Django Notes App") {
            steps {
                script {
                    clone("https://github.com/Arman076/django-notes-app.git", "main")
                }
            }
        }

        stage("Build the Code") {
            steps {
                script {
                    docker_build("django-notes-app", "latest", "devil678")
                }
            }
        }

        stage("Trivy Scan") {
            steps {
                sh '''
                echo "Running Trivy vulnerability scan..."
                trivy image --exit-code 0 --severity CRITICAL,HIGH devil678/django-notes-app:latest
                '''
            }
        }

        stage("Install Docker & Kubernetes Tools") {
            steps {
                sh '''
                    if ! command -v docker &> /dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y docker.io
                    fi

                    if ! command -v docker-compose &> /dev/null; then
                        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                    fi
                '''
            }
        }

        stage("Push Code to Docker Hub") {
            steps {
                script {
                    docker_push("django-notes-app", "latest", "devil678")
                }
            }
        }

        stage("Test the Code") {
            steps {
                echo "Running Django Tests..."
            }
        }

       stage("Deploy the Code") {
    steps {
        script {
            sh '''
            echo "Checking Minikube status..."
            if ! minikube status | grep -q "host: Running"; then
                echo "Starting Minikube..."
                minikube start
            else
                echo "Minikube is already running."
            fi

            echo "Deploying to Kubernetes..."

            kubectl apply -f k8s/django-ns.yaml
            kubectl apply -f k8s/mysql-namespace.yaml
            kubectl apply -f k8s/mysql-pvc.yaml
            kubectl apply -f k8s/django-secrets.yaml
            kubectl apply -f k8s/service.yaml
            kubectl apply -f k8s/mysql-deployment.yaml

            kubectl apply -f k8s/django-configmap.yaml
            kubectl apply -f k8s/django-secretss.yaml
            kubectl apply -f k8s/django-deployment.yaml
            kubectl apply -f k8s/django-service.yaml

            kubectl apply -f k8s/nginx-configmap.yaml
            kubectl apply -f k8s/nginx.yaml
            kubectl apply -f k8s/nginx-service.yaml

            kubectl apply -f k8s/django-hpa.yaml

            echo "Getting Django service URL..."
            MINIKUBE_IP=$(minikube ip)
            PORT=$(kubectl get svc djangoservice -n django -o jsonpath="{.spec.ports[0].nodePort}")
            echo "Django App is available at: http://$MINIKUBE_IP:$PORT"

            NGINX_PORT=$(kubectl get svc nginx -n django -o jsonpath="{.spec.ports[0].nodePort}")
            echo "NGINX is available at: http://$MINIKUBE_IP:$NGINX_PORT"
            '''
        }
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

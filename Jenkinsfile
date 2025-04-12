pipeline {
    agent any

    environment {
        IMAGE_NAME = "django-notes-app:latest"
        CONTAINER_NAME = "django-notes-app-container"
        PUSH_IMAGE = "devil678/django-notes-app:latest"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
        SCANNER_HOME = "/opt/sonar-scanner"
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

        stage("Cloning Django Notes App") {
            steps {
                script {
                    clone("https://github.com/Arman076/django-notes-app.git", "main")
                }
            }
        }

        stage("Install SonarScanner if missing") {
            steps {
                sh '''
                if [ ! -d "/opt/sonar-scanner" ]; then
                    echo "Installing SonarScanner..."
                    cd /opt
                    sudo curl -O https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                    sudo apt-get install unzip -y
                    sudo unzip sonar-scanner-cli-5.0.1.3006-linux.zip
                    sudo mv sonar-scanner-5.0.1.3006-linux sonar-scanner
                    echo 'export PATH=$PATH:/opt/sonar-scanner/bin' >> ~/.bashrc
                    source ~/.bashrc
                else
                    echo "SonarScanner already installed."
                fi
                '''
            }
        }

        stage("SonarQube Analysis") {
            steps {
                withSonarQubeEnv('sonarserver') {
                    withCredentials([string(credentialsId: 'django-sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                        ${SCANNER_HOME}/bin/sonar-scanner \
                          -Dsonar.projectKey=django-notes-app \
                          -Dsonar.projectName="Django Notes App" \
                          -Dsonar.sources=. \
                          -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
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
                trivy image --format table --output trivy-report.txt \
                    --severity CRITICAL,HIGH --exit-code 0 devil678/django-notes-app:latest
                '''
            }
        }

        stage("Install Docker & Kubernetes Tools") {
            steps {
                sh '''
                if ! command -v docker &> /dev/null; then
                    echo "Installing Docker..."
                    sudo apt-get update
                    sudo apt-get install -y docker.io
                fi

                if ! command -v docker-compose &> /dev/null; then
                    echo "Installing Docker Compose..."
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
                // You can plug in pytest or Django tests here
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
                    fi

                    echo "Deploying to Kubernetes..."
                    kubectl apply -f k8s/
                    
                    MINIKUBE_IP=$(minikube ip)
                    PORT=$(kubectl get svc djangoservice -n django -o jsonpath="{.spec.ports[0].nodePort}")
                    NGINX_PORT=$(kubectl get svc nginx -n django -o jsonpath="{.spec.ports[0].nodePort}")

                    echo "Django App: http://$MINIKUBE_IP:$PORT"
                    echo "NGINX: http://$MINIKUBE_IP:$NGINX_PORT"
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
                body: """<p><strong>Job:</strong> ${env.JOB_NAME}</p>
                         <p><strong>Build #:</strong> ${env.BUILD_NUMBER}</p>
                         <p><strong>Status:</strong> ${currentBuild.result ?: 'SUCCESS'}</p>
                         <p><a href="${env.BUILD_URL}">View Full Logs</a></p>""",
                attachmentsPattern: 'trivy-report.txt',
                attachLog: true,
                mimeType: 'text/html'
            )
        }
    }
}

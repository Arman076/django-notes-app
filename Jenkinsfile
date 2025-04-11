@Library("Shared") _    
pipeline {
    agent any

    environment {
        IMAGE_NAME = "django-notes-app:latest"
        CONTAINER_NAME = "django-notes-app-container"
        PUSH_IMAGE = "devil678/django-notes-app:latest"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
        SCANNER_HOME = '/opt/sonar-scanner'
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

        stage("Sonarqube Analysis") {
            steps {
                withSonarQubeEnv('sonarserver') {
                    withCredentials([string(credentialsId: 'django-sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''${SCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=django-notes-app \
                            -Dsonar.projectName="Django Notes App" \
                            -Dsonar.sources=. \
                            -Dsonar.login=$SONAR_TOKEN'''
                    }
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
                trivy image --severity CRITICAL,HIGH devil678/django-notes-app:latest
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
            script {

                def trivySummary = ''
                if (fileExists('trivy-report.txt')) {
                    trivySummary = readFile('trivy-report.txt').split('\n').take(20).join('<br>')
                }

                emailext (
                    to: "anjaraalam3597@gmail.com",
                    subject: "Jenkins Build Report: ${currentBuild.fullDisplayName}",
                    body: """
                        <h2>✅ Jenkins Build Report</h2>
                        <p><strong>Job Name:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Status:</strong> ${currentBuild.result ?: 'SUCCESS'}</p>
                        <p><a href="${env.BUILD_URL}">🔗 View Build Logs</a></p>
                        <hr>
                        <h3>🔍 Trivy Scan (Top 20 Results)</h3>
                        <pre>${trivySummary}</pre>
                        <p>📎 Full report attached: <strong>trivy-report.txt</strong></p>
                        <hr>
                        <h3>📊 SonarQube Analysis</h3>
                        <p>Code quality analysis completed via SonarQube for <strong>Django Notes App</strong>.</p>
                        <p>Visit SonarQube Dashboard: <a href="http://<YOUR-SONARQUBE-IP>:9000/dashboard?id=django-notes-app">SonarQube Report</a></p>
                    """,
                    attachmentsPattern: 'trivy-report.txt',
                    attachLog: true,
                    mimeType: 'text/html'
                )
            }
        }
    }
}

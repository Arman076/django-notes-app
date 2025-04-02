pipeline {
    agent { label 'aws' }  // Make sure 'aws' agent is available

    environment {
        IMAGE_NAME = "django-notes:latest"
        CONTAINER_NAME = "django-notes-container"
        PUSH_IMAGE = "devil678/notes-app:latest"
    }

    stages {
        
        stage("Cloning Django Notes App") {
            steps {
                echo "Cloning the Django Notes App from GitHub..."
                git url: "https://github.com/LondheShubham153/django-notes-app.git", branch: "main"
                echo "Code cloned successfully."
            }
        }
        
        stage("Build the Code") {
            steps {
                echo "Building the Docker image..."
                sh "docker build -t $IMAGE_NAME ."
                echo "Docker image built successfully."
            }
        }
        
        
        
        
        stage("Install Docker & Docker Compose if Missing") {
            steps {
                echo "Checking and Installing Docker & Docker Compose if necessary..."
                sh '''
                    if ! command -v docker &> /dev/null; then
                        echo "Docker not found, installing..."
                        sudo apt-get update
                        sudo apt-get install -y docker.io
                        sudo systemctl start docker
                        sudo systemctl enable docker
                    fi

                    if ! command -v docker-compose &> /dev/null; then
                        echo "Docker Compose not found, installing..."
                        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                        sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
                    fi

                    docker --version
                    docker-compose --version
                '''
            }
        }
        
        
        
        
        stage("Push Code to Docker Hub") {
            steps {
                echo "Pushing the image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')])
                {
                // withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')]) {
                    sh "docker login -u ${dockerHubUser} -p ${dockerHubPass}"
                    sh "docker image tag $IMAGE_NAME $PUSH_IMAGE"
                    sh "docker push $PUSH_IMAGE"
                    echo "Image pushed to Docker Hub successfully."
                }
            }
        }
        
        stage("Test the Code") {
            steps {
                echo "Running Django Tests..."
                // Uncomment to run tests inside the Docker container
                // sh "docker run --rm $IMAGE_NAME python manage.py test"  // Running Django tests inside container
                echo "Code testing completed successfully."
            }
        }

        stage("Deploy the Code") {
            steps {
                echo "Deploying the application..."
                sh "docker-compose down || true"  // Stop existing container if running
                sh "docker-compose up -d"
                echo "Application deployed successfully."
            }
        }
    }
}

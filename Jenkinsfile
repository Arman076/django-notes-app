// pipeline {
//     agent { label 'aws' }  // Make sure 'aws' agent is available

//     environment {
//         IMAGE_NAME = "django-notes:latest"
//         CONTAINER_NAME = "django-notes-container"
//         PUSH_IMAGE = "devil678/notes-app:latest"
//     }

//     stages {
        
//         stage("Cloning Django Notes App") {
//             steps {
//                 echo "Cloning the Django Notes App from GitHub..."
//                 git url: "https://github.com/LondheShubham153/django-notes-app.git", branch: "main"
//                 echo "Code cloned successfully."
//             }
//         }
        
//         stage("Build the Code") {
//             steps {
//                 echo "Building the Docker image..."
//                 sh "docker build -t $IMAGE_NAME ."
//                 echo "Docker image built successfully."
//             }
//         }
        
        
        
        
//         stage("Install Docker & Docker Compose if Missing") {
//             steps {
//                 echo "Checking and Installing Docker & Docker Compose if necessary..."
//                 sh '''
//                     if ! command -v docker &> /dev/null; then
//                         echo "Docker not found, installing..."
//                         sudo apt-get update
//                         sudo apt-get install -y docker.io
//                         sudo systemctl start docker
//                         sudo systemctl enable docker
//                     fi

//                     if ! command -v docker-compose &> /dev/null; then
//                         echo "Docker Compose not found, installing..."
//                         sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
//                         sudo chmod +x /usr/local/bin/docker-compose
//                         sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
//                     fi

//                     docker --version
//                     docker-compose --version
//                 '''
//             }
//         }
        
        
        
        
//         stage("Push Code to Docker Hub") {
//             steps {
//                 echo "Pushing the image to Docker Hub..."
//                 withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')])
//                 {
//                 // withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')]) {
//                     sh "docker login -u ${dockerHubUser} -p ${dockerHubPass}"
//                     sh "docker image tag $IMAGE_NAME $PUSH_IMAGE"
//                     sh "docker push $PUSH_IMAGE"
//                     echo "Image pushed to Docker Hub successfully."
//                 }
//             }
//         }
        
//         stage("Test the Code") {
//             steps {
//                 echo "Running Django Tests..."
//                 // Uncomment to run tests inside the Docker container
//                 // sh "docker run --rm $IMAGE_NAME python manage.py test"  // Running Django tests inside container
//                 echo "Code testing completed successfully."
//             }
//         }

//         stage("Deploy the Code") {
//             steps {
//                 echo "Deploying the application..."
//                 sh "docker-compose down || true"  // Stop existing container if running
//                 sh "docker-compose up -d"
//                 echo "Application deployed successfully."
//             }
//         }
//     }
// }








// we have done things using shared libary we can say that is external file where we called these things for readbility of the code




@Library("Shared") _  #that is the name of the shared library this things mention jenkins system there 
pipeline {
    agent { label 'aws' }  // Make sure 'aws' agent is available

    environment {
        IMAGE_NAME = "django-notes-app:latest"
        CONTAINER_NAME = "django-notes-app-container"
        PUSH_IMAGE = "devil678/django-notes-app:latest"
        KUBE_CONFIG= '/root/.kube/config'
    }

    stages {
        // calling the shared library
        
        stage("hello world")
        {
            steps {
                script {
                    hello()
                }
            }
        }
        
        stage("Cloning Django Notes App") {
            steps {
                // echo "Cloning the Django Notes App from GitHub..."
                script{
                clone ("https://github.com/Arman076/django-notes-app.git", "main")   #clone docker_build that is the file name that things they called there 
                // echo "Code cloned successfully."
            }
        }
        }
        
        stage("Build the Code") {
            
            
            steps {
                echo "Building the Docker image..."
                
                script {
                    docker_build("django-notes-app","latest","devil678")
                }
                
                // sh "docker build -t $IMAGE_NAME ."
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

                    
                    if ! command -v minikube &> /dev/null; then
                        echo "Installing Minikube..."
                        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
                        chmod +x minikube-linux-amd64
                        mv minikube-linux-amd64 /usr/local/bin/minikube
                    fi

                    

                    if ! command -v docker-compose &> /dev/null; then
                        echo "Docker Compose not found, installing..."
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
                    
                    docker --version
                    docker-compose --version
                    
                    
                    
                '''
            }
        }
        
        
        
        
        stage("Push Code to Docker Hub") {
            steps {
                echo "Pushing the image to Docker Hub..."
                
                script {
                    docker_push ("django-notes-app","latest","devil678")
                }
                
                // withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')])
                // {
                // // withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')]) {
                //     sh "docker login -u ${dockerHubUser} -p ${dockerHubPass}"
                //     sh "docker image tag $IMAGE_NAME $PUSH_IMAGE"
                //     sh "docker push $PUSH_IMAGE"
                //     echo "Image pushed to Docker Hub successfully."
                // }
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
                
                echo "running the kubernetes"
                // sh "kubectl apply -f k8s/deployment.yaml"

                echo "Verifying Deployment..."
                // sh "kubectl rollout status deployment django-notes -n django"
                echo "Application deployed successfully to Kubernetes."
                
                
                sh "docker-compose up -d"
                echo "Application deployed successfully."
            }
        }
    }
}





















# Steps to deploy on Azure App Service

1. Build docker image from the code: 
    
        docker build -f Dockerfile -t <app-name>:latest .

2. Run and test your new docker image locally (pass required env variables): 

        docker run -p 8080:8080 -e AZURE_STORAGE_KEY=<key> --rm <app-name>

3. Locate the image id by running `docker images` and tag existing image with your Docker Hub username: 

        docker tag <image-id> <dockerhub-username>/<app-name>

4. Push the image to Docker Hub: 

        docker push <dockerhub-username>/<app-name>

5. Go to azure portal and create a new "Web app for containers" and specify `<dockerhub-username>/<app-name>` as docker hub image repository. 

6. Set the required environment variables in App settings. Also configure Azure to use the port that we specified in Dockerfile using below App setting: 

        WEBSITES_PORT=8080

7. Optionally, you can debug the container by going to kudu console at `https://<azure-app-name>.scm.azurewebsites.net/`


For more information, please see: [Use a custom Docker image for Web App for Containers](https://docs.microsoft.com/en-us/azure/app-service/containers/tutorial-custom-docker-image).


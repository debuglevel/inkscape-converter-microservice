echo "Building Docker image..."
docker build -t inkscape-rest -f Dockerfile .

echo "Running Docker image..."
docker run -ti -p 8080:8080 inkscape-rest

pause
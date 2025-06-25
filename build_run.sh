docker build -t mercadona:latest .
docker run --rm -it --mount type=bind,source=./secrets.json,target=/secrets.json,readonly mercadona:latest 
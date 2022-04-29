cd ina_flask
docker build --tag skyppy .
docker run --rm -p 8080:8080 skyppy
# Setup
## To run locally:
- Install Python
- Enter `pip install flask` in CLI
- Enter `flask run` or `python -m flask run` in CLI (whichever works)

To run with docker container, run: `./run-docker.sh`

# Helpful Resources
You can view Swagger by accessing `<host>:5000/docs`

Postman Collection: https://www.getpostman.com/collections/a8493c1ce129a98bc554

A metrics endpoint is available as well. Just GET to `<host>:5000/metrics/<endpoint>`

# Workflow Engine API (DigitalOcean)
This repository is for create container that get data of DigitalOcean API, creating local copies for accelerate requests and changing with style for rundeck fields for example.

# Execute Python
## Necessary secrets
For execute the python locally you need create file in /run/secrets/do_token the same way that docker will to do into the container.
```sh
echo "[YOUR_DOCKER_TOKEN]" > /run/secrets/do_token
```
Then you just need execute the next code in the directory of the repo cloned for up the aplication locally.

```sh
export FLASK_APP=get_data
export FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=5500
```
You can verify the service via http://localhost:5500/digitalocean

# Execute Container

## Necessary secrets
For use this container you need use a docker secret for DigitalOcean token, the name of the secret will be do_token:
```sh
DO_TOKEN=[YOUR_DOCKER_TOKEN]
printf $DO_TOKEN | docker secret create do_token -
```
>If you want know how create a token in your DigitalOcean account you can read [this documentation](https://docs.digitalocean.com/reference/api/create-personal-access-token/).

## Generate Image

## Run Container Locally

## Run Container with Swarm



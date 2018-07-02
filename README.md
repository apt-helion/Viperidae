# Viperidae2.0 API
API and main application for viperidae2.0

Main site [`viperidae.app`](https://viperidae.app)
Developer docs/api [`developer.viperidae.app`](https://developer.viperidae.app)

## Setting up on a development environment 
```
# Clone it
git clone https://github.com/apt-helion/viperidae2.0
cd viperidae2.0

# Using the python virtual environment module (venv), create a python
# environment into "./env"
python3.6 -m venv env

# Setup your shell for this project
source env/bin/activate

# Install requirements for this project
pip install -r requirements.txt

# Start the server
./main.py
```

Go to `0.0.0.0:8080` and you should be able to see the message `api.viperidae.app is up`.

## Testing the api
### GET requests
If your web browser allows for viewing JSON just the requests into there. e.g.
```
0.0.0.0:8080/index?u=https://blog.justinduch.com
```

### POST requests
Use the script (coming soon) or cURL. e.g.
```
> curl --headers "Authorization: Basic {base64string}" --data "q=test" 0.0.0.0:8080/devSearch
```


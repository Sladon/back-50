# QComparator Backend
## Getting started

### Install Python 3
```
sudo apt-get update
sudo apt-get install python3
sudo apt install python3-pip     
```

### Create Virtual Enviroment
```
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies
```
pip3 install -r requirements.txt
```

### Starting Server
```
cd qcomparator
python3 manage.py runserver
```
> To start the server make sure that you use *source .venv/bin/activate*

## Protocol
Any changes made should be in their own branch and the merged to main after review. Never push to main.
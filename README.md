# Tieto
A simple file sharing website created using flask.

## Installation
1. Clone this repo and enter the folder.
2. (Optional) Create a python virtual environment with ```python -m venv (name of your venv)``` and then activate the venv with ```source (direction of venv activate file)```. For example ```source venv/bin/activate```
3. Install required python packages with ```pip install -m requirements.txt```
4. Initiate the database with ```flask db init```
5. Migrate the database with ```flask db migrate -m "Init migration"```
6. Upgrade the database with ```flask db upgrade```
7. Now you can run ```flask run``` and it should work and you can access the webpage in the URL displayed in the console.
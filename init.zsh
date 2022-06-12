#!/bin/zsh

virtualenv -p python3 venv
source activate
pip install flask flask-sqlalchemy flask-marshmallow flask-cors marshmallow marshmallow-sqlalchemy haversine

cd backend
echo "from ordering import db\ndb.create_all()" | python
cd -

cd frontend
npm install
cd -

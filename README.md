# pygit-demo

Sample project demonstrates work with pygit, flask, celery, redis

## installation

`$ git clone git@github.com:andrewnsk/pygit-demo.git`

`$ cd ./pygit-demo`

`$ virtualenv venv`

`$ source venv/bin/activate`

`(venv) $ pip install -r requirements.txt`

**install Redis:**

`$ install-redis.sh`

## running


`FLASK_APP = main.py`

`FLASK_ENV = development`

`FLASK_DEBUG = 1`

`./venv/bin/python -m flask run`

**in other console:**

`$ cd ./pygit-demo`

`$ source venv/bin/activate`

`./venv/bin/celery worker -A main.celery --loglevel=info`


## external requirements
  - redis 
  - git
  
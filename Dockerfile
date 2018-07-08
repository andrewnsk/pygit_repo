FROM python:3.4-alpine
ADD . /code
ADD /root/projects/counter-app /git-repo
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt-get install git
CMD ["python", "app.py"]

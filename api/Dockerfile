FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

### While running docker compose dont have stest code line activated
### Once the docker image is build make available again the test code lines 

FROM base as test
RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["gunicorn", "--workers=8", "--bind", "0.0.0.0:3316", "app:app"]

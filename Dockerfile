FROM python:3-onbuild
MAINTAINER Grant David Bachman (gbachman@rentjungle.com)
ONBUILD COPY . /usr/src/app
WORKDIR /usr/src/app
ONBUILD RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]


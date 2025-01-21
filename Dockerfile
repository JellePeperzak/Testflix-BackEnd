FROM python:3.13-alpine
# Copy all the files from the project to the container and install the dependencies. Serve the API from /api/app.py

RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    libgomp

WORKDIR /opt/app

COPY requirements.txt /opt/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /opt/app

CMD ["python", "index.py"]
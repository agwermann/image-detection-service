FROM python:3.9-slim-bullseye

# Setup venv
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y python3-opencv

# Config virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel
RUN pip install torch==1.12.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r requirements.txt

# Setup and start app
EXPOSE 8080
ENTRYPOINT [ "python", "main.py" ]
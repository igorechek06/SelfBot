FROM python:3.10-bullseye

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install ffmpeg -y
RUN pip install pip -U

WORKDIR /app

COPY pip.txt .
RUN pip install -r pip.txt -U

COPY . .
CMD ["python", "main.py"]

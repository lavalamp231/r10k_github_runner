FROM python:3.8

WORKDIR /app

COPY git_runner.py git_runner.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "git_runner.py"]
FROM python:3.9

RUN apt-get update && apt-get install -y \
    wget unzip && apt-get clean

RUN pip install --upgrade pip
RUN pip install selenium

COPY . .

CMD [ "python3", "run_tests.py"]

FROM python:3.12

WORKDIR /client

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SERVER_URL=http://app:8000

CMD ["sleep", "infinity"]


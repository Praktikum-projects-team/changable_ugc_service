FROM python:3.10

WORKDIR /tests

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD wait-for-it -s "${API_HOST}:${API_PORT}" --timeout 60 && pytest -s /tests/functional/src
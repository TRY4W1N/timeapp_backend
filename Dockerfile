FROM python:3.10 as builder

RUN apt-get update && apt-get upgrade

WORKDIR /app

RUN python3 -m venv /venv
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /src /src


FROM builder as app
WORKDIR /app
COPY --from=builder /venv /venv
COPY --from=builder /app .

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
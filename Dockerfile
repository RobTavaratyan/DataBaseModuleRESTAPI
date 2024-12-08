FROM postgres:latest

ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=my_database

EXPOSE 5432

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN python3 -m venv /app/venv

RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt --no-deps

RUN chmod +x /app/script.sh

CMD ["bash", "/app/script.sh"]

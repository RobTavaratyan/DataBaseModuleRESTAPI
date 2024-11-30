FROM postgres:latest

ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=my_database

EXPOSE 5432

RUN apt-get update && apt-get install -y ntpdate && ntpdate -u time.google.com \
    && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r ./Stuff/requirements.txt

RUN chmod +x /app/script.sh

CMD ["bash", "/app/script.sh"]

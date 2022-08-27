FROM python:3.9-slim

# DECLARE ENV VARIABLES

ENV DAGSTER_VERSION=1.0.5

# Main Dependencies for container with pipeline code. Do not repeat these in the setup.py `install_requires` list.

RUN pip install \
    dagster==${DAGSTER_VERSION} \
    dagster-postgres==${DAGSTER_VERSION} \
    dagster-docker==${DAGSTER_VERSION}
# Add bash and nano
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "nano"]
# Set Slack and API Request Config
ENV API_KEY="10c0c76dfaabef8d2ba52d1fb7e5bf8d"
ENV SLACK_CH='C03VBDF4DHT'
ENV SLACK_BOT_API="xoxb-3855764521027-3997431744533-85uJ2S3oSD0DjlNX2sTzrHax"
# Set Production Database to Environment
ENV PROD_HOST="host.docker.internal"
#ENV PROD_HOST="database-postgresql"
ENV PROD_DATABASE="postgres"
ENV PROD_PORT="6000"
ENV PROD_USER="postgres"
ENV PROD_PW="postgrespw"
# Set $DAGSTER_HOME and copy dagster instance there
ENV DAGSTER_HOME=/opt/dagster/dagster_home

RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml $DAGSTER_HOME

# Add repository code

WORKDIR /opt/dagster/etl

# Copy the etl repo
COPY  pipeline .

# RUN install pip requirements
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirement.txt

# Run dagster gRPC server on port 4000

EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "./main.py"]
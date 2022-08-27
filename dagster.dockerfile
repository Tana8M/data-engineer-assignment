FROM python:3.9-slim

# DECLARE ENV VARIABLES

ENV DAGSTER_VERSION=1.0.5

RUN pip install \
    dagster==${DAGSTER_VERSION} \
    dagster-graphql==${DAGSTER_VERSION} \
    dagit==${DAGSTER_VERSION} \
    dagster-postgres==${DAGSTER_VERSION} \
    dagster-docker==${DAGSTER_VERSION} 

# Set the $DAGSTER_HOME env variable
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml workspace.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME
FROM python:3.12-slim
RUN pip install --no-cache-dir mlflow==3.17.0 boto3==1.43.109 psycopg2-binary==2.9.13 \
 && useradd --create-home --uid 1000 mlflow
USER mlflow
WORKDIR /home/mlflow
EXPOSE 5000

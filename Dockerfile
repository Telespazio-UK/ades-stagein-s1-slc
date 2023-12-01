FROM python:3

RUN pip install boto3 requests
COPY run.py /run.py
ENTRYPOINT ["python", "/run.py"]
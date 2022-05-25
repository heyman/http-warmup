FROM python:3.10
ADD . /warmup
RUN pip install -r /warmup/requirements.txt
WORKDIR /warmup
ENTRYPOINT ["python", "warmup.py"]

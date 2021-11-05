FROM python:3.8-alpine

RUN pip install -r requirements.txt

ADD run_pybryt.py /run_pybryt.py

ENTRYPOINT [ "python3", "/run_pybryt.py" ]

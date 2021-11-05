FROM python:3.8-alpine

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD run_pybryt.py /run_pybryt.py

ENTRYPOINT [ "python3", "/run_pybryt.py" ]

FROM python:3.9

WORKDIR /check_status_my_works

COPY requirements.txt .
RUN pip install -r /requirements.txt
COPY *.py .
CMD ["python", "main.py"]

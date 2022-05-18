FROM python:3.9

WORKDIR /check_status_my_works

COPY requirements.txt .
RUN pip install --upgrade pip -r requirements.txt
COPY *.py .
CMD ["python", "main.py"]

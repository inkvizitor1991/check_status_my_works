FROM python:3.9

WORKDIR /check_status_my_works
ENV DEVMAN_TOKEN=""
ENV TG_BOT_TOKEN=""
ENV TG_CHAT_ID=""

RUN pip install -U pip python-telegram-bot python-dotenv requests
COPY *.py .
CMD ["python", "main.py"]

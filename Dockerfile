FROM python:3.8


EXPOSE 80

COPY ./app /app

RUN pip install -r requirements.txt

CMD ["python", "run.py"]


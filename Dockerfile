FROM python:3.10

WORKDIR /opt/app

COPY . .

RUN pip install flask --no-cache-dir

RUN pip install requests --no-cache-dir

EXPOSE 5000

ENV FLASK_APP=get_data

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

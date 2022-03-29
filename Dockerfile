FROM python:3.9-slim
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . /app
ENTRYPOINT [ "gunicorn", "-w", "5", "--bind", "0.0.0.0:8888", "main:app" ]
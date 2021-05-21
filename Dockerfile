FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/department_db
ENV FLASK_APP=wsgi.py
WORKDIR /department_app
COPY requirements.txt /department_app/
RUN pip install -r requirements.txt
COPY . /department_app/
EXPOSE 5000
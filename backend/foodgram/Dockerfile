FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
#CMD ["python3", "manage.py", "runserver", "0:8000"]
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
LABEL author='Nikolai Orlov' version=194573024328
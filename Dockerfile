FROM python:3.9.0

RUN python -m pip install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install gunicorn==20.1.0

ENV ENVIRONMENT prod

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c" , "python manage.py collectstatic --noinput --settings=seeyaArchive.settings.production && python manage.py migrate --settings=seeyaArchive.settings.production && gunicorn seeyaArchive.wsgi:application --bind 0.0.0.0:8000"]

FROM python:3.10-slim-bullseye

EXPOSE 5000

WORKDIR /app

RUN python3 -m pip install --upgrade pip

RUN groupadd -g 1000 hassan && useradd -g 1000 -r hassan

RUN apt-get update

RUN apt-get install -y default-libmysqlclient-dev libssl-dev tk && \
    apt-get install -y --no-install-recommends gcc python-dev

COPY requirements.txt /app

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt

VOLUME /app

USER hassan

COPY app.py /app

COPY templates /app/templates

COPY attendance_files /app/attendance_files

CMD ["flask", "run", "--host=0.0.0.0"]


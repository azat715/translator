FROM python:3.8
LABEL maintainer="azat715@gmail.com"
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["/code/entrypoint.sh"]
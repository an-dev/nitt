FROM python:3.9

WORKDIR /nitt

COPY ./requirements.txt /nitt/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /nitt/requirements.txt

COPY ./docker-entrypoint.sh /nitt/docker-entrypoint.sh

USER root
RUN chmod +x /nitt/docker-entrypoint.sh

COPY ./app /nitt/app

EXPOSE 8001

CMD ["bash", "-c", "/nitt/docker-entrypoint.sh"]

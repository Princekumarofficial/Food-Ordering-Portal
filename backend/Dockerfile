FROM python:3.11-slim

WORKDIR /backend

COPY requirements.txt /backend/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /backend

EXPOSE 8000

RUN chmod +x /backend/build.sh
RUN /backend/build.sh

RUN chmod +x /backend/entrypoint.sh

ENTRYPOINT ["/bin/sh", "/backend/entrypoint.sh"]

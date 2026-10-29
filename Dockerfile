FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY migrations migrations
COPY flask-fileshare.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP flask-fileshare.py
RUN flask translate compile

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
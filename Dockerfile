FROM python:3.7.4

RUN pip install flask && pip install configparser && pip install pytz

EXPOSE 8080

COPY app.py .

CMD python app.py

FROM python:3.8
WORKDIR /app

ADD scrapper_pirate /app/scrapper_pirate/
ADD app.py /app/app.py
ADD requirements.txt /app/requirements.txt
RUN mkdir -p /app/scrapper_pirate/files
RUN mkdir -p /app/scrapper_pirate/logs
RUN pip install -r requirements.txt

VOLUME /app/scrapper_pirate/files
VOLUME /app/scrapper_pirate/logs
CMD python app.py $UF $ITEMS
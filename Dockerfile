FROM python:3

ADD . .

RUN pip install -r requirements.txt

RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt

CMD [ "assignment1.py" ]
ENTRYPOINT [ "python3" ]
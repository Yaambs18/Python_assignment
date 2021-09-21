FROM python:3

ADD . .

RUN pip install requests
RUN pip install bs4
RUN pip install lxml
RUN pip install nltk

RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt

CMD [ "assignment1_unit_test.py" ]
ENTRYPOINT [ "python3" ]
FROM python:3.10
VOLUME /contact_book
COPY . /try
WORKDIR /try
RUN pip install contact_book/.
CMD ["bash"]
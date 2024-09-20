FROM python

RUN adduser static
USER static
WORKDIR /gx/gx_volume/data_docs

CMD ["python", "-m", "http.server", "3000"]
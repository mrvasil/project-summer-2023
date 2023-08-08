FROM alpine:latest
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip          
COPY . /
WORKDIR /
RUN pip3 install --no-cache --upgrade pip flask
ENTRYPOINT ["python3"]
CMD ["main.py"]
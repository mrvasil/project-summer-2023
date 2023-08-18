FROM alpine:latest
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip          
COPY . /eng-silaeder
WORKDIR /eng-silaeder
RUN pip3 install --no-cache --upgrade pip flask
CMD ["python3 main.py >> logs.txt 2>&1"]
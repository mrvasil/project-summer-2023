FROM mrvasil/eng-silaeder:latest
COPY . /eng-silaeder
WORKDIR /eng-silaeder

CMD python3 main.py >> data/logs.txt 2>&1
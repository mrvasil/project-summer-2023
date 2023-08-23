FROM mrvasil/eng-silaeder:latest
COPY . /eng-silaeder
WORKDIR /eng-silaeder

CMD python3 main.py >> logs.txt 2>&1
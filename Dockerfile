FROM alpine:3.22.2

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    bash 

RUN ln -sf python3 /usr/bin/python

WORKDIR /app

COPY . /app

RUN python3 -m venv bandit-env && \
    . bandit-env/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


RUN chmod +x run_sast.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["/bin/bash"]
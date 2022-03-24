FROM docker.elastic.co/logstash/logstash:7.17.1
WORKDIR /usr/share/logstash/
ENV XPACK_MONITORING_ENABLED false
USER root

RUN apt update && apt install -y python3-pip \
    && pip3 install pyyaml==6.0

COPY configure-logstash-script.py /usr/share/logstash/configure-logstash-script.py
COPY /pipeline/logstash.conf /usr/share/logstash/pipeline/logstash.conf

CMD ["python3", "configure-logstash-script.py"]

FROM docker.elastic.co/logstash/logstash:7.8.0
WORKDIR /usr/share/logstash/
ENV XPACK_MONITORING_ENABLED false
USER root
RUN yum update -y \
    && yum -y install epel-release \
    && yum install -y --enablerepo="epel" python-pip \
    && pip install ruamel.yaml==0.16.5

COPY configure-logstash-script.py /usr/share/logstash/configure-logstash-script.py
COPY logstash.conf /usr/share/logstash/pipeline/logstash.conf

CMD ["python", "configure-logstash-script.py"]

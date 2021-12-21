FROM docker.elastic.co/logstash/logstash:7.16.1
WORKDIR /usr/share/logstash/
ENV XPACK_MONITORING_ENABLED false
USER root
RUN yum update -y \
	&& yum -y install epel-release \
	&& yum install -y --enablerepo="epel" python3-pip \
	&& pip3 install pyyaml==6.0

COPY configure-logstash-script.py /usr/share/logstash/configure-logstash-script.py
COPY /pipeline/logstash.conf /usr/share/logstash/pipeline/logstash.conf

CMD ["python3", "configure-logstash-script.py"]

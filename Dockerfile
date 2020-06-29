FROM python:3.7-slim AS python_path
WORKDIR /usr/share/logstash/

COPY chain-logstah-conf-script.py /usr/share/logstash/chain-logstah-conf-script.py
COPY tenants-credentials.yml /usr/share/logstash/tenants-credentials.yml
COPY logstash.conf /usr/share/logstash/pipeline/logstash.conf
RUN pip install ruamel.yaml==0.16.5
RUN python chain-logstah-conf-script.py

FROM docker.elastic.co/logstash/logstash:7.4.2
ENV XPACK_MONITORING_ENABLED false
RUN logstash-plugin install --no-verify \
    logstash-input-okta_system_log
COPY --from=python_path /usr/share/logstash /usr/share/logstash
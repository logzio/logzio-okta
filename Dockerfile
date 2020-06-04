ARG LOGSTASH_VERSION=7.4.2
FROM docker.elastic.co/logstash/logstash:${LOGSTASH_VERSION}
ENV XPACK_MONITORING_ENABLED false
RUN logstash-plugin install --no-verify \
    logstash-input-okta_system_log
COPY logstash.conf /usr/share/logstash/pipeline/logstash.conf
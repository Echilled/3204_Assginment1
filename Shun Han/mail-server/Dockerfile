FROM marcopas/docker-mailslurper

#######################################
#            INSTALLATION
#######################################

ENV FILEBEAT_VERSION 8.4.2

RUN apt-get update -qq \
&& apt-get upgrade -qqy \
&& apt install wget -qqy \
&& apt install gnupg -qqy \
&& apt-get install apt-transport-https -qqy \
&& apt install systemd -qqy\
&& apt-get clean


RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
&& echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list \
&& apt-get update \
&& apt-get install filebeat \
&& systemctl enable filebeat


######################################
#          CONFIGURATION
######################################
ADD filebeat/filebeat.yml /etc/filebeat/filebeat.yml

RUN service filebeat start \
&& cd /etc/filebeat \
&& filebeat setup --index-management -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["192.168.1.3:9200"]'


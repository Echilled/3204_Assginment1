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
&& apt-get install libpcap0.8 \
&& apt-get clean


RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
&& echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list \
&& apt-get update \
&& apt-get install packetbeat -qqy \
&& systemctl enable packetbeat



######################################
#          CONFIGURATION
######################################
ADD packetbeat/packetbeat.yml /etc/packetbeat/packetbeat.yml

RUN packetbeat setup \
&& service packetbeat start



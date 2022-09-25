FROM marcopas/docker-mailslurper

#######################################
#            INSTALLATION
#######################################

ENV FILEBEAT_VERSION 8.4.2

RUN apt-get update -qq \
&& apt-get upgrade -qqy \
&& apt-get clean \
&& apt install curl -qqy

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${FILEBEAT_VERSION}-linux-x86_64.tar.gz \
&& tar xzvf filebeat-${FILEBEAT_VERSION}-linux-x86_64.tar.gz \
&& rm filebeat-${FILEBEAT_VERSION}-linux-x86_64.tar.gz


######################################
#          CONFIGURATION
######################################
#ADD filebeat/filebeat.yml /${FILEBEAT_DIRECTORY}/filebeat.yml
ADD filebeat/filebeat.yml /filebeat-${FILEBEAT_VERSION}-linux-x86_64/filebeat.yml


RUN cd filebeat-${FILEBEAT_VERSION}-linux-x86_64
#&& ./filebeat setup -e \
#&& chown root filebeat.yml \
#&& ./filebeat -e

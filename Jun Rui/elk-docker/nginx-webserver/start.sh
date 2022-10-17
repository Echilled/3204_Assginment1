#!/bin/bash

curl -XPUT -H "Content-Type: application/json" 'http://elk:9200/_template/filebeat?pretty' -d@/etc/filebeat/filebeat.template.json
/etc/init.d/filebeat start
nginx
tail -f /var/log/nginx/access.log -f /var/log/nginx/error.log



### Packetbeat
curl -XPUT -H "Content-Type: application/json" 'http://elk:9200/_template/packetbeat?pretty' -d@/etc/packetbeat/packetbeat.template.json
/etc/init.d/packetbeat start
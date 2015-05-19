#!/bin/bash
cd /var/www/html
unzip -q -o /tmp/DSP2043_0.96.0a.zip
mkdir -p redfish
cd redfish
ln -sf .. v1
cd ..
ip a
#sed -i -e 's/Listen 80/Listen 8000/' /etc/apache2/ports.conf
echo "Launching apache2 in foreground with /usr/sbin/apache2ctl -DFOREGROUND -k start"
/usr/sbin/apache2ctl -DFOREGROUND -k start

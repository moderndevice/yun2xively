curl -k https://codeload.github.com/xively/xively-python/zip/master > master.zip
opkg update && opkg install unzip setuptools python-ssl
unzip master.zip
cd xively-python-master
python setup.py install
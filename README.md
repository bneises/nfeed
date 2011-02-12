nFeed
=====

INSTALL
--------------
For now, all the install does is copy etc/nfeed to /etc/nfeed so there is
atleast a central configuration file.


Dependancies you must work out on your own:

*    Redis server version 2.0.4
*    Tornado python web server

####For Fedora 14:####

    yum install git redis python-setuptools -y
    easy_install tornado
    easy_install redis

    git clone git://github.com/petekalo/nfeed.git
    cd nfeed
    ./install.sh

CONFIGURE
----------
After installation, edit /etc/nfeed/nfeed.conf

Make sure you update the installation directory/path, otherwise
nothing will work.


USAGE
----------
With redis server running:

    chkconfig nfeed-cron on     <-- sets up job as a service in runlevels 2345
    service nfeed-cron start
    logs to /var/log/nfeed.log

    ./nfeed-server& 	    <-- will run tornado http server in background


TODO
-----
*    Write web programming for WSGI, tornado is temporary
*    Write an upstart script for nfeed-cron


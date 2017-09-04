Script to gather system CPU, Memory and Network stats.

PreInstall for openSUSE:
    sudo -i
    zypper refresh
    zypper update
    zypper install gcc
    sudo zypper install python-pip python-setuptools python-wheel
    zypper install apache2-devel
    pip install mod_wsgi

Install:
    git clone ...
    cd sysinfo
    pip install -r requirements.txt
 
Run:
    mod_wsgi-express start-server sysinfo.wsgi —port=5000
#!/usr/bin/env bash
#!/usr/bin/env bash

apt-get update
apt-get install -y python-virtualenv gcc pkg-config python graphviz libgraphviz-dev


# work from vagrant home
cd /home/vagrant/

virtualenv venv
source ./venv/bin/activate
pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"
pip install -r /vagrant/requirements.txt


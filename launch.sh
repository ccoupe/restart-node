#!/bin/bash
cd /usr/local/lib/restart-node
nm-online
source PYENV/bin/activate
node=`hostname`
python3 restart-node.py -c ${node}.json

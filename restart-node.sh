#!/bin/bash
cd /usr/local/lib/restart-node
nm-online
source /usr/local/lib/restart-node/rs-env/bin/activate
node=`hostname`
python3 restart-node.py -c ${node}.json

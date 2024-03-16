# Makefile for restart-node
PRJ=restart-node
DESTDIR=/usr/local/lib/$(PRJ)
SRCDIR=$(HOME)/Projects/iot/$(PRJ)
LAUNCH=$(PRJ).sh
SERVICE=$(PRJ).service
PYENV ?= ${DESTDIR}/rs-env

NODE := $(shell hostname)
SHELL := /bin/bash 

${PYENV}:
	sudo mkdir -p ${PYENV}
	sudo chown ${USER} ${PYENV}
	python3 -m venv ${PYENV}
	( \
	set -e ;\
	source ${PYENV}/bin/activate; \
	pip install -r $(SRCDIR)/requirements.txt; \
	)

setup_launch:
	sudo systemctl enable ${SERVICE}
	sudo systemctl daemon-reload
	sudo systemctl restart ${SERVICE}

setup_dir:
	sudo mkdir -p ${DESTDIR}
	sudo mkdir -p ${DESTDIR}/lib	
	sudo cp ${SRCDIR}/lib/Settings.py ${DESTDIR}/lib
	sudo cp ${SRCDIR}/restart-node.py ${DESTDIR}
	sudo cp -a ${SRCDIR}/template.json ${DESTDIR}
	sudo cp -a ${SRCDIR}/Makefile ${DESTDIR}
	sudo cp -a ${SRCDIR}/requirements.txt ${DESTDIR}
	sudo cp -a ${SRCDIR}/${SERVICE} ${DESTDIR}
	sudo chown -R ${USER} ${DESTDIR}
	sed  s!PYENV!${PYENV}! <${SRCDIR}/launch.sh >$(DESTDIR)/$(LAUNCH)
	sudo chmod +x ${DESTDIR}/${LAUNCH}
	sed  s/{NODE}/$(NODE)/ <$(SRCDIR)/template.json >$(DESTDIR)/$(NODE).json
	sudo cp ${DESTDIR}/${SERVICE} /etc/systemd/system
	
update: 
	cp ${SRCDIR}/restart-node.py ${DESTDIR}
	cp ${SRCDIR}/lib/Settings.py ${DESTDIR}/lib

install: ${PYENV} setup_dir update setup_launch

clean: 
	sudo systemctl stop ${SERVICE}
	sudo systemctl disable ${SERVICE}
	sudo rm -f /etc/systemd/system/${SERVICE}
	sudo rm -rf ${DESTDIR}

realclean: clean
	rm -rf ${PYENV}

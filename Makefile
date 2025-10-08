install:
	pip install -r requirements.txt

help:
	cd src && python classify_incidents.py --help
	cd src && python classify_incidents.py from-dir --help
	cd src && python classify_incidents.py from-snow --help

file-test:
	cd src && python classify_incidents.py from-dir ./test-data/

install:
	pip install -r requirements.txt

help:
	cd src && python classify_incidents.py --help
	cd src && python classify_incidents.py from-dir --help
	cd src && python classify_incidents.py from-file --help
	cd src && python classify_incidents.py from-snow --help

clean:
	rm -rf ./target/

run-dir: clean
	cd src && python classify_incidents.py from-dir ../test-data/ ../target/

install:
	pip install -r requirements.txt
	pip install -r automate-agent/requirements.txt

help:
	cd src && python cli.py --help
	cd src && python cli.py from-dir --help
	cd src && python cli.py from-file --help
	cd src && python cli.py from-snow --help

lint:
	pylint --fail-under=0 ./automate-agent/src
	pylint --fail-under=0 ./src

clean:
	rm -rf ./target/

run-web:
	cd src && streamlit run web.py --server.port=8080 --server.address=0.0.0.0

run-dir: clean
	cd src && python cli.py from-dir ../test-data/ ../target/

run-small: 
	rm -f ./target/small.csv
	cd src && python cli.py from-file ../test-data/small.csv ../target/small.csv

run-automate-agent:
	cd automate-agent/src && python app.py

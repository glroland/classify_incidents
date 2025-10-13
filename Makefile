install:
	pip install -r requirements.txt

help:
	cd src && python cli.py --help
	cd src && python cli.py from-dir --help
	cd src && python cli.py from-file --help
	cd src && python cli.py from-snow --help

lint:
	pylint ./src

clean:
	rm -rf ./target/

run-web:
	cd src && streamlit run web.py --server.port=8080 --server.address=0.0.0.0

run-dir: clean
	cd src && python cli.py from-dir ../test-data/ ../target/

run-small: 
	rm -f ./target/small.csv
	cd src && python cli.py from-file ../test-data/small.csv ../target/small.csv

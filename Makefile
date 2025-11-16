install:
	pip install -r webapp/requirements.txt
	pip install -r automate-agent/requirements.txt

lint:
	pylint --fail-under=0 ./automate-agent/src
	pylint --fail-under=0 ./webapp/src

clean:
	rm -rf ./target/

run-web:
	cd webapp/src && streamlit run web.py --server.port=8080 --server.address=0.0.0.0

run-automate-agent:
	cd automate-agent/src && python app.py

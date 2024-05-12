default:
	virtualenv -p python3 venv
	. venv/bin/activate

venv2:
	python3 -m venv venv
	. venv/bin/activate

activate:
	. venv/bin/activate

install:
	pip3 install -r requirements.txt

clean:
	rm -rf venv .venv
.PHONY: run install uninstall deps status

run:
	python3 redmine_hours.py

install:
	python3 redmine_hours.py --install

uninstall:
	python3 redmine_hours.py --uninstall

deps:
	pip install python-dotenv selenium webdriver-manager

status:
	crontab -l

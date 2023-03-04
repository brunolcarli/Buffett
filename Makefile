install:
	pip install -r requirements.txt

shell:
	python manage.py shell

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:9988

forex_daemon:
	python manage.py forex_usdbrl_collector

target: forex_daemon run

pipe:
	make install
	make migrate
	make -j2 target

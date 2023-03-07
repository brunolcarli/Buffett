install:
	pip install -r requirements.txt

shell:
	python manage.py shell

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:9988

usdbrl_daemon:
	python manage.py usdbrl_collector

target: usdbrl_daemon run

pipe:
	make install
	make migrate
	make -j2 target

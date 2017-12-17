init:
	sudo pip3 install -r requirements.txt

test:

exec:
	python3 main.py

clean:
	rm data/pickle_files/*.pickle
	rm b_*

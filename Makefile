init:
	sudo pip3 install -r requirements.txt

test:

exec:
	python3 main.py

clean:
	rm -rf data/pickle_files/*.pickle
	rm -rf data/pickle_files/b_*
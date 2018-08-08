run:
	pipenv run python elevatorcat.py

update:
	# --pre because of "black" package
	# which doesn't offer stable builds yet
	pipenv lock --pre
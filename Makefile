
install:
	conda env create -f environment.yml --use-index-cache --solver libmamba 

fix:
	ruff check --fix .
	black .

lint:
	ruff check .
	black --check .

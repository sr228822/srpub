
install:
	conda env create -f environment.yml --use-index-cache --solver libmamba 

fmt:
	ruff check --fix .
	black .

lint:
	ruff check .
	black --check .

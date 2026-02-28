
install:
	conda env create -f environment.yml --use-index-cache --solver libmamba

update:
	conda env update -f environment.yml --prune --solver libmamba

fix:
	ruff check --fix .
	black .

lint:
	ruff check .
	black --check .

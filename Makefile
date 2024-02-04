
install:
	conda env create -f environment.yml --use-index-cache --solver libmamba 

fmt:
	black .

lint:
	black --check .

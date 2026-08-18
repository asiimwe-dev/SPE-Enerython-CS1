.PHONY: install profiles pue sizing mvp test all clean

install:
	pip install -r requirements.txt

profiles:
	python -m src.load_profiling.generate

pue:
	python -m src.pue_analysis.analyze

sizing:
	python -m src.it_sizing.calculate

mvp:
	python -m src.mvp.dashboard

test:
	python -m pytest tests/ -v

all: install profiles pue sizing mvp test

clean:
	rm -rf data/output/figures/* data/output/csv/*


# Variables
.psql := _build/psql

python_files := \
	$(wildcard src/*.py) \
	$(wildcard src/**/*.py)

# Targets

psql: $(.psql)
web:
	python server.py

# Rules

$(.psql): sql/dump.sql
	dropdb arcadetrail
	createdb arcadetrail
	pg_restore -F c -O -x -d arcadetrail sql/dump.sql
	psql -c "\i sql/ArcadeTrail.sql" -d arcadetrail
	touch $(.psql)

src/cli/R.npy: $(.psql) src/genR.py
	python src/genR.py

src/cli/Theta.npy src/cli/X.npy: src/cli/train_svd.py
	PYTHONPATH=src python src/cli/train_svd.py

format: $(python_files)
	env/bin/autopep8 --in-place --aggressive --aggressive $^
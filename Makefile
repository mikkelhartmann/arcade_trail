
# Variables
.psql := _build/psql

# Targets

psql: $(.psql)
web:
	python src/server.py
genR: src/cli/R.npy
train_svd: src/cli/Theta.npy src/cli/X.npy
# Rules

$(.psql): sql/dump.sql
	dropdb arcadetrail
	createdb arcadetrail
	pg_restore -F c -O -x -d arcadetrail sql/dump.sql
	psql -c "\i sql/ArcadeTrail.sql" -d arcadetrail
	touch $(.psql)

src/cli/R.npy: $(.psql)
	python src/generatingR.py

src/cli/Theta.npy src/cli/X.npy:
	python src/train_svd.py

set -x

PYTHONPATH="./:$PYTHONPATH" py.test

pep8 ./eureka

pylint  --reports=n ./eureka

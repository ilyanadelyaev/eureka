set -x

PYTHONPATH="./:$PYTHONPATH" CONFIGFILE="./dev/config.yaml" python ./eureka/run.py

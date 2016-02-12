set -x

PYTHONPATH="./:$PYTHONPATH" python ./eureka/run.py --config ./dev/config.yaml

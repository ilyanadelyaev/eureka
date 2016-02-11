set -x

PYTHONPATH="./:$PYTHONPATH" python ./eureka/application.py --config ./dev/config.yaml

set -x

rm -rf ./dev/venv/
rm -rf ./dev/logs/

find ./eureka -name "*.pyc" -exec rm -rf {} \;
find ./eureka -name "__pycache__" -exec rm -rf {} \;

set -x

virtualenv ./dev/venv
source ./dev/venv/bin/activate

pip install -r ./dev/requirements.txt

mkdir dev/logs

echo type: \"source ./dev/venv/bin/activate\"

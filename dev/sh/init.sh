set -x

virtualenv ./dev/venv
source ./dev/venv/bin/activate

pip install -r ./dev/requirements.txt

mkdir dev/logs

npm install --save-dev babel-cli
npm install --save-dev babel-preset-react

echo type: \"source ./dev/venv/bin/activate\"

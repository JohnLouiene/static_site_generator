set -a
. ./.env
set +a

cd src
python3 main.py
cd ../docs && python3 -m http.server 8888
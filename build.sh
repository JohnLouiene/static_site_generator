set -a
. ./.env
set +a

cd src
python3 main.py $DESTINATION_REPOSITORY
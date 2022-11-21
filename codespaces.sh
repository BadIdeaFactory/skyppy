sudo apt get update && apt get install -y gcc libpq-dev libsndfile-dev ffmpeg
curl -sSL https://install.python-poetry.org | python3 -
poetry shell
python run_local.py
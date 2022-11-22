sudo apt update && sudo apt install -y gcc libpq-dev libsndfile-dev ffmpeg
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry shell
python run_local.py

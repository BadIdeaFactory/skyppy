# Skyppy
## Speech is overrated - skyp it

Everyone's talking and nobody's listening. What if we could reduce conversations to the gaps in between and while we're at it perhaps remove that pesky intro music. No music, no speaking - life would be so much better - this is the promise of Skyppy - a new app to let you concentrate on the good parts of YouTube videos.

We use a number of open source libraries to do the tricky bits, such as ...

1. the fabulous [inaspeechsegmenter](https://github.com/ina-foss/inaSpeechSegmenter) a segmenter that uses tensorflow to split audio tracks up into supposed male, female, music and noenergy catagories.

2. the legendary [youtube-dl](https://github.com/ytdl-org/youtube-dl) for which we have so much love. ♥️

## Uses

- skypping the annoying male voices in videos (we appreciate that gender is fluid but you can assign genders yourself)
- skypping all the speech in videos (let's face it - we can understand a lot just from gestures and facial expressions)
- skypping the music (let's get to the point shall we)
- skypping the noise (life is too noisy already)
- skypping the silence (who needs pregnant pauses - life is too short)

## Installation (Docker)

Required : [Docker Compose](https://docs.docker.com/compose/install/)

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Run Docker
3. Open a terminal and running the following commands

``` bash
docker build --tag skyppy .
docker run --rm -p 8080:8080 skyppy
``` 

4. Navigate to `http://0.0.0.0:8080/` in your browser.
5. No hot reload yet. You need to close (`ctrl+c`) and restart with
 ``` bash
 docker build --tag skyppy .
 docker run --rm -p 8080:8080 skyppy
 ```
 or alternatively run `sh active_docker.sh`

7. If you want to maintain any downloaded data, use `docker run -p 8080:8080 skyppy` instead of `docker run --rm -p 8080:8080 skyppy`

## Installation for Developers – Poetry Version (Linux only for now, we're working on Mac)

1. Install Poetry 

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. If you receive a certificate error try:

```bash
 python3 -m pip install --upgrade certifi
```
On MacOS you may also need to
```
open /Applications/Python\ 3.9/Install\ Certificates.command
```

Note – 3.9 is used above but your version may vary.

If you are using zsh You may also need to alter your `.zshrc` to include something like:

```bash
export PATH="$HOME/.poetry/bin:$PATH"
```
or wherever it installed poetry.

3. Install Skyppy

In your chosen directory...

```bash
poetry install
poetry shell
python run_local.py
```


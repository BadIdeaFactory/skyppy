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

## Installation

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Run Docker
3. Open a terminal and running the following commands

``` bash
cd ina_flask
docker build --tag skyppy .
docker run --rm -p 8080:8080 skyppy
``` 

4. Navigate to `http://0.0.0.0:8080/` in your browser.
5. No hot reload yet. You need to close (`ctrl+c`) and restart with
 ``` bash
 docker build --tag skyppy .
 docker run --rm -p 8080:8080 skyppy
 ```
7. If you want to maintain the data, subsitute `docker run -p 8080:8080 skyppy`

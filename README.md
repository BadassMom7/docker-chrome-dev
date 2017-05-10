# Chrome Dev in Docker

## Setup

* `docker build -t chrome-dev .`

## Example script: Snapshotting pages

(Thanks to @pakastin for the initial command line :) )

```
python snapshot.py -p test.pdf https://google.com/
python snapshot.py -s test.png -w 800 -h 600 https://google.com/
```

## Prior Art

Also see [Jess Frazelle's Chrome Dockerfile][jessfraz], it's probably better and more secure.

[jessfraz]: https://github.com/jessfraz/dockerfiles/blob/master/chrome/stable/Dockerfile
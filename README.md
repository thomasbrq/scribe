# Scribe

The aim of the project is to transcribe audios via a Telegram bot.

![gif](https://github.com/thomasbrq/audio_transcriber/assets/71637888/e6c0620b-70a5-428c-b69f-1db6ca5fdd52)

[Source audio](https://audio-lingua.ac-versailles.fr/spip.php?article8774)

## Dependencies

- [Python 3.10](https://www.python.org/downloads/release/python-31011/)
- [ffmpeg](https://www.ffmpeg.org/download.html)

## Setup

Install [Python 3.10](https://www.python.org/downloads/release/python-31011/) and [ffmpeg](https://www.ffmpeg.org/download.html) on your machine.

### Python

Create a Python virtual environment

```sh
python3 -m venv .venv
```

and activate it

```sh
# on Linux/MacOS
source .venv/bin/activate

# on Windows:
.venv\Scripts\activate
```

Install the Python dependencies

```sh
python3 -m pip install -r requirements.txt
```

### Telegram

- Connect with [BotFather](https://telegram.me/BotFather) on Telegram.
- Select the "New Bot" option to start creating your new bot or type `/newbot`.
- Provide a bot name
- Then `BotFather` will send you a token. Keep it safe, we'll need it later.

### VOSK

Scribe uses [VOSK](https://alphacephei.com/vosk/), a speech recognition toolkit.
It works offline and the models are lightweight.

- [Download a model](https://alphacephei.com/vosk/models), I personnally use `vosk-model-en-us-daanzu-20200905`
- Unzip the archive in the root folder and rename it `model`.

#### Environments variables

Create a `.env` file in the root folder and write this

```js
API_KEY=<YOUR_TELEGRAM_BOT_API_KEY>
```

## How to use

Run

```sh
python3 src/transcribe.py
```

and send an audio file to your bot and he will reply with the transcript.

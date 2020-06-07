# Mute Microphone Stream Deck Plugin

[Stream Deck](https://www.elgato.com/en/gaming/stream-deck) plugin
to allow users to mute their microphone on MacOS.

## Design

- connect to Elgato Stream Deck software using Websockets
- plugin uses asyncio's event loop to coordinate communication with Stream Deck software and manage system sound

## Installation Instructions

1. Download repo
1. Create a virtual environment with Python 3.7+
1. `pip install -r requirements.txt`
1. Update [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) at top of `mic_control/app.py` with the Python Path from your virtual evironment above
1. Link folder `ln -s [path-to-file] /Users/[username]/Library/Application Support/com.elgato.StreamDeck/Plugins/com.alysivji.mutemic-mac.sdPlugin`
1. Restart StreamDeck software

## Resources

- [`websockets` documentation](https://websockets.readthedocs.io/en/stable/intro.html)
- Medium: [How to create a Web Socket client](https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549)

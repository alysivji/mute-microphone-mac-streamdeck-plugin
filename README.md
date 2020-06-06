# Mute Microphone Stream Deck Plugin

[Stream Deck](https://www.elgato.com/en/gaming/stream-deck) plugin
to allow users to mute their microphone.

## Todo

- move to [websockets](https://github.com/aaugustin/websockets)
  - with `asyncio`, we can have a job that gets volume and updates what we need to do
  - https://websockets.readthedocs.io/en/stable/intro.html
  - https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549
- https://www.youtube.com/watch?v=vOa2r1ybiuk

## Use Cases

- States: `muted`, `not_muted`
- if we mute, we need to get the volume and store it
- when we unmute, we need to use last volume (if volume is not 0)
- always checking volume to update volume (every second)

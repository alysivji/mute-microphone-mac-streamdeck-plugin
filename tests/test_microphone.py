from mic_control.microphone import MacMicrophoneClient


def test_get_input_volume():
    m = MacMicrophoneClient()
    vol = m.get_input_volume()

    assert isinstance(vol, int)
    assert 0 <= vol <= 100

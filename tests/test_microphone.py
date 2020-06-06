from mic_control.microphone_client import MacMicrophoneClient


def test_get_input_volume():
    m = MacMicrophoneClient()
    vol = m.volume

    assert isinstance(vol, int)
    assert 0 <= vol <= 100

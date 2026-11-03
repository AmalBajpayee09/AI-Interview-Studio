"""v0.11 WAV inspection checks: NOT device tests or speech recognition tests."""
from array import array
import io
import wave
import pytest
from app import audio_offline

def wav_bytes(rate=16000,channels=1):
    samples=array('h')
    for i in range(rate*2):
        active=rate//4<=i<3*rate//4 or 5*rate//4<=i<7*rate//4
        value=7000 if active and i%16<8 else -7000 if active else 0
        samples.extend([value]*channels)
    f=io.BytesIO()
    with wave.open(f,'wb') as w:
        w.setnchannels(channels);w.setsampwidth(2);w.setframerate(rate);w.writeframes(samples.tobytes())
    return f.getvalue()

@pytest.mark.parametrize('rate,channels',[(8000,1),(16000,2),(44100,1)])
def test_pcm_sound_activity_no_speaker_identity(rate,channels):
    report=audio_offline.analyze_wav(wav_bytes(rate,channels))
    assert report['sample_rate']==rate and report['channels']==channels
    assert report['duration_seconds']==2 and len(report['segments'])==2
    assert all(x['speaker']=='unknown' for x in report['segments'])
    assert not report['transcription_performed'] and not report['raw_audio_stored']

def test_wav_endpoint_requires_uploaded_wave(client):
    good=client.post('/api/audio/analyze-wav',files={'file':('source.wav',wav_bytes(),'audio/wav')})
    assert good.status_code==200 and len(good.json()['segments'])==2
    assert client.post('/api/audio/analyze-wav',files={'file':('broken.wav',b'not-wave','audio/wav')}).status_code==422
    assert client.post('/api/audio/analyze-wav',files={'file':('huge.wav',b'X'*(8*1024*1024+1),'audio/wav')}).status_code==413

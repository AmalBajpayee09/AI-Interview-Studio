"""Bounded, explicit-upload PCM WAV waveform inspection.

Detects sound activity only; this is NOT speech recognition or speaker diarization.
No audio files are retained.
"""
from __future__ import annotations
from array import array
import io
import math
import sys
import wave

MAX_WAV_BYTES=8*1024*1024
MAX_SECONDS=120
class InvalidAudio(ValueError):pass

def analyze_wav(data:bytes,*,threshold:float=.015,frame_ms:int=100)->dict:
    if not isinstance(data,bytes) or len(data)>MAX_WAV_BYTES or len(data)<44:
        raise InvalidAudio('WAV file must be 44 bytes–8 MB')
    if not (.001<=threshold<=.3) or frame_ms not in (50,100,200):
        raise InvalidAudio('Unsupported activity threshold or frame size')
    try:
        with wave.open(io.BytesIO(data),'rb') as wav:
            rate=wav.getframerate();channels=wav.getnchannels();width=wav.getsampwidth();count=wav.getnframes()
            if wav.getcomptype()!='NONE' or channels not in (1,2) or width!=2 or rate<8000 or rate>48000:
                raise InvalidAudio('Supported WAV: uncompressed 16-bit PCM, mono/stereo, 8–48 kHz')
            if count>rate*MAX_SECONDS or count*width*channels>MAX_WAV_BYTES:
                raise InvalidAudio('Audio duration or decoded size exceeds limit')
            step=max(1,int(rate*frame_ms/1000))
            segments=[];active=False;start=0;last_voiced=0;total=0;peaks=0
            while total<count:
                raw=wav.readframes(min(step,count-total))
                if not raw:break
                pcm=array('h');pcm.frombytes(raw)
                if sys.byteorder!='little':pcm.byteswap()
                volume=0.0;sample_count=len(pcm)//channels
                for index in range(0,len(pcm),channels):
                    mono=sum(pcm[index:index+channels])/(channels*32768.0)
                    volume+=mono*mono
                rms=math.sqrt(volume/max(1,sample_count))
                loud=rms>=threshold
                if loud:
                    peaks+=1
                    if not active:active=True;start=total/rate
                    last_voiced=(total+sample_count)/rate
                elif active and total/rate-last_voiced>=.3:
                    if last_voiced-start>=.15:
                        segments.append({'start_seconds':round(start,3),'end_seconds':round(last_voiced,3),'speaker':'unknown','kind':'sound_activity'})
                    active=False
                total+=sample_count
            if active and last_voiced-start>=.15:
                segments.append({'start_seconds':round(start,3),'end_seconds':round(last_voiced,3),'speaker':'unknown','kind':'sound_activity'})
    except (wave.Error,EOFError,OSError) as exc:raise InvalidAudio('Invalid or unsupported WAV file') from exc
    return {'sample_rate':rate,'channels':channels,'sample_width_bits':16,'duration_seconds':round(total/rate,3),
            'segments':segments[:120],'voiced_frame_count':peaks,'raw_audio_stored':False,
            'transcription_performed':False,'speaker_diarization_performed':False,
            'note':'Waveform activity is not speech detection or speaker identity. Use consented STT for text.'}

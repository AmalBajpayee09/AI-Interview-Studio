"""Opt-in local continuous source-separated audio capture.

Requires SoundCard + NumPy + faster-whisper. Source identification is not speaker
identity: all transcripts remain 'unknown' without verified diarization. Audio is
kept in short bounded memory buffers, never stored as raw recordings.
"""
from __future__ import annotations
import collections
import queue
import threading
import time
from dataclasses import dataclass, field

SAMPLE_RATE = 16000
FRAME_SAMPLES = 4000
MAX_SPEECH_SECONDS = 16


def rms(samples) -> float:
    if len(samples) == 0: return 0.0
    return (sum(float(x)*float(x) for x in samples)/len(samples))**0.5


@dataclass
class VoiceGate:
    threshold: float = 0.012
    silence_seconds: float = 0.8
    chunk_seconds: float = 0.25
    frames: list = field(default_factory=list)
    silences: float = 0
    voiced: bool = False
    audio_seconds: float = 0

    def push(self, samples):
        """Returns completed speech as a list of frames; None while collecting."""
        loud = rms(samples) >= self.threshold
        if loud: self.voiced = True
        if not self.voiced: return None
        self.frames.append(samples)
        self.audio_seconds += self.chunk_seconds
        self.silences = 0 if loud else self.silences+self.chunk_seconds
        if self.silences >= self.silence_seconds or self.audio_seconds >= MAX_SPEECH_SECONDS:
            utterance = self.frames
            self.frames=[]; self.silences=0; self.voiced=False; self.audio_seconds=0
            return utterance
        return None


class LiveAudio:
    def __init__(self):
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._pause = threading.Event()
        self._threads = []
        self._events = collections.deque(maxlen=128)
        self._seq = 0
        self._source_ids: list[str] = []
        self._status = 'idle'
        self._language = 'auto'
        self._errors: list[str] = []
        self._queue: queue.Queue = queue.Queue(maxsize=4)
        self._recognizer = None

    def emit(self, kind, **data):
        with self._lock:
            self._seq += 1
            self._events.append({'id':self._seq, 'kind':kind, 'at':time.time(), **data})

    @staticmethod
    def device_list():
        try:
            import soundcard as sc
            microphones=sc.all_microphones(include_loopback=True)
            return {'available':True,'devices':[
                {'id':str(device.id),'name':device.name,'source_type':'system' if getattr(device,'isloopback',False) else 'microphone'}
                for device in microphones]}
        except (ImportError,OSError,RuntimeError) as exc:
            return {'available':False,'devices':[],'reason':f'Audio device backend unavailable: {type(exc).__name__}. Install optional audio dependencies.'}

    def status(self):
        with self._lock:
            return {'status':self._status,'source_ids':list(self._source_ids),
                    'events_last_id':self._seq,'errors':self._errors[-3:],
                    'speaker_identification':'unknown (source tracking only)',
                    'raw_audio_stored':False,'paused':self._pause.is_set(),
                    'queue_depth':self._queue.qsize()}

    def events(self, since=0):
        with self._lock:
            return [x.copy() for x in self._events if x['id'] > since]

    def start(self, source_ids, language='auto'):
        if language not in ('auto','en','hi'): raise ValueError('Choose auto, en or hi')
        if not source_ids or len(source_ids)>2 or len(set(source_ids))!=len(source_ids):
            raise ValueError('Select one or two distinct audio sources')
        try:
            import numpy
            import soundcard as sc
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError('Optional audio packages missing (soundcard, numpy, faster-whisper)') from exc
        devices={str(x.id):x for x in sc.all_microphones(include_loopback=True)}
        if any(str(x) not in devices for x in source_ids): raise ValueError('A selected audio device is no longer available')
        with self._lock:
            if self._status=='running': raise ValueError('Audio capture already running; stop before restarting')
            self._queue=queue.Queue(maxsize=4)
            self._stop.clear(); self._pause.clear(); self._status='running'; self._errors=[]
            self._source_ids=list(source_ids); self._language=language
            self._threads=[threading.Thread(target=self._capture,args=(devices[sid],sid),daemon=True,name='studio-capture') for sid in source_ids]
            self._threads.append(threading.Thread(target=self._transcribe,daemon=True,name='studio-stt'))
            for t in self._threads: t.start()
        self.emit('capture_started',source_ids=list(source_ids),language=language)
        return self.status()

    def stop(self):
        self._stop.set(); self._pause.clear()
        for thread in list(self._threads): thread.join(timeout=1.2)
        with self._lock:
            self._status='idle'; self._threads=[];self._source_ids=[]
        self.emit('capture_stopped')
        return self.status()

    def pause(self):
        with self._lock:
            if self._status!='running': raise ValueError('Audio capture is not running')
            self._pause.set()
        self.emit('capture_paused')
        return self.status()

    def resume(self):
        with self._lock:
            if self._status!='running': raise ValueError('Audio capture is not running')
            self._pause.clear()
        self.emit('capture_resumed')
        return self.status()

    def _capture(self,device,source_id):
        try:
            import numpy as np
            gate=VoiceGate()
            with device.recorder(samplerate=SAMPLE_RATE,blocksize=FRAME_SAMPLES) as recorder:
                while not self._stop.is_set():
                    audio=recorder.record(numframes=FRAME_SAMPLES)
                    if audio is None: continue
                    if self._pause.is_set():
                        gate=VoiceGate()  # Discard partial utterances, no audio retained while paused.
                        continue
                    mono=np.asarray(audio,dtype='float32')
                    if mono.ndim==2: mono=mono.mean(axis=1)
                    if len(mono)==0: continue
                    complete=gate.push(mono)
                    if complete:
                        try:self._queue.put_nowait((source_id,np.concatenate(complete),time.time()))
                        except queue.Full:self.emit('dropped_utterance',source_id=source_id,reason='STT busy')
        except Exception as exc:
            self.emit('audio_error',source_id=source_id,error=f'Capture disconnected: {type(exc).__name__}')
            with self._lock:
                self._errors.append(f'{source_id}: {type(exc).__name__}')
                self._status='error'
            self._stop.set()

    def _transcribe(self):
        try:
            from faster_whisper import WhisperModel
            while not self._stop.is_set() or not self._queue.empty():
                try: source_id,audio,ended_at=self._queue.get(timeout=0.2)
                except queue.Empty: continue
                start=time.perf_counter()
                if self._recognizer is None:
                    import os
                    self._recognizer=WhisperModel(os.environ.get('STT_MODEL','tiny'),device='cpu',compute_type='int8')
                segments,info=self._recognizer.transcribe(audio,beam_size=1,
                    language=None if self._language=='auto' else self._language,vad_filter=True)
                text=' '.join(s.text.strip() for s in segments).strip()
                if text:
                    duration=round(len(audio)/SAMPLE_RATE,3)
                    self.emit('transcript_final',source_id=source_id,text=text,
                        start_at=round(ended_at-duration,3),end_at=round(ended_at,3),
                        speaker='unknown',language=info.language,confidence=None,
                        latency_ms=round((time.perf_counter()-start)*1000,1))
        except Exception as exc:
            self.emit('stt_error',error=f'{type(exc).__name__}: speech engine unavailable or failed')
            with self._lock: self._errors.append('Speech engine unavailable or failed')
            self._stop.set()

live_audio=LiveAudio()

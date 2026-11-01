"""Measured host-resource reporting and conservative inference recommendations.

This is advisory: actual model unloading and GPU execution are backend-controlled.
"""
import psutil

MODES=('battery-saver','balanced','performance')

def snapshot(mode='balanced'):
    if mode not in MODES: raise ValueError('Unsupported resource mode')
    memory=psutil.virtual_memory()
    available_gb=memory.available/2**30
    rss_mb=psutil.Process().memory_info().rss/2**20
    cpu=psutil.cpu_percent(interval=0.02)
    if available_gb<2 or memory.percent>88:
        pressure='high'
    elif available_gb<4 or memory.percent>72:
        pressure='moderate'
    else:
        pressure='low'
    # Recommendations are not a claim that a configured model fits or executes on GPU.
    max_parallel=1 if mode=='battery-saver' or pressure=='high' else 2
    guidance=('Close large applications or choose a smaller local model; cloud is opt-in only.'
              if pressure=='high' else 'Use a small quantized model when battery or RAM is limited.'
              if mode=='battery-saver' else 'Measure response latency before increasing model size.')
    return {'mode':mode,'memory_available_gb':round(available_gb,2),
            'memory_pressure':pressure,'cpu_percent_sample':cpu,'worker_rss_mb':round(rss_mb,1),
            'recommended_max_parallel_requests':max_parallel,
            'recommendation':guidance,
            'gpu_execution':'unverified; no GPU acceleration inferred'}

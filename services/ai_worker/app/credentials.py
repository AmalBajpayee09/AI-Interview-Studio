"""Windows Credential Manager for cloud keys. No secrets in SQLite or exports.

A legacy environment key is still supported for development, but never returned over HTTP.
Windows is the only platform with an in-app write/delete implementation; fail closed
elsewhere rather than pretending an environment file is a secure credential vault.
"""
import ctypes
import os
import sys
from ctypes import wintypes

TARGET = 'AIInterviewStudio/OpenAI'

class CredentialUnavailable(RuntimeError):
    pass


def _api():
    if sys.platform != 'win32':
        raise CredentialUnavailable('Secure in-app key storage requires Windows Credential Manager. Use a development environment variable on other systems.')
    return ctypes.WinDLL('Advapi32.dll', use_last_error=True)


class _FILETIME(ctypes.Structure):
    _fields_ = [('low', wintypes.DWORD), ('high', wintypes.DWORD)]


class _CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD), ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR), ('Comment', wintypes.LPWSTR),
        ('LastWritten', _FILETIME), ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_ubyte)),
        ('Persist', wintypes.DWORD), ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.c_void_p), ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR),
    ]


def save_api_key(value: str) -> None:
    if not isinstance(value, str) or not (12 <= len(value) <= 1024) or any(c in value for c in '\r\n\x00'):
        raise ValueError('Enter a valid API key (12–1024 characters, no newlines).')
    api = _api()
    payload = bytearray(value.encode('utf-16-le'))
    blob = (ctypes.c_ubyte * len(payload)).from_buffer(payload)
    cred = _CREDENTIAL()
    cred.Type = 1  # CRED_TYPE_GENERIC
    cred.TargetName = TARGET
    cred.CredentialBlobSize = len(payload)
    cred.CredentialBlob = ctypes.cast(blob, ctypes.POINTER(ctypes.c_ubyte))
    cred.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE (per-user OS account vault)
    cred.UserName = 'AIInterviewStudio'
    api.CredWriteW.argtypes = [ctypes.POINTER(_CREDENTIAL), wintypes.DWORD]
    api.CredWriteW.restype = wintypes.BOOL
    try:
        if not api.CredWriteW(ctypes.byref(cred), 0):
            raise CredentialUnavailable(f'Windows credential write failed ({ctypes.get_last_error()}).')
    finally:
        for i in range(len(payload)): payload[i] = 0
        for i in range(len(blob)): blob[i] = 0


def _read_windows_key() -> str | None:
    api = _api()
    ptr = ctypes.POINTER(_CREDENTIAL)()
    api.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(_CREDENTIAL))]
    api.CredReadW.restype = wintypes.BOOL
    if not api.CredReadW(TARGET, 1, 0, ctypes.byref(ptr)):
        if ctypes.get_last_error() == 1168: return None  # ERROR_NOT_FOUND
        raise CredentialUnavailable(f'Windows credential read failed ({ctypes.get_last_error()}).')
    api.CredFree.argtypes = [ctypes.c_void_p]
    api.CredFree.restype = None
    try:
        entry = ptr.contents
        if not entry.CredentialBlobSize: return None
        data = ctypes.string_at(entry.CredentialBlob, entry.CredentialBlobSize)
        return data.decode('utf-16-le')
    finally:
        api.CredFree(ctypes.cast(ptr, ctypes.c_void_p))


def read_api_key() -> str | None:
    # Existing opt-in env setup remains compatible; never print/read it through the API.
    if sys.platform == 'win32':
        key = _read_windows_key()
        if key: return key
    return os.getenv('OPENAI_API_KEY') or None


def has_api_key() -> bool:
    return bool(read_api_key())


def delete_api_key() -> bool:
    api = _api()
    api.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
    api.CredDeleteW.restype = wintypes.BOOL
    if api.CredDeleteW(TARGET, 1, 0): return True
    if ctypes.get_last_error() == 1168: return False
    raise CredentialUnavailable(f'Windows credential deletion failed ({ctypes.get_last_error()}).')

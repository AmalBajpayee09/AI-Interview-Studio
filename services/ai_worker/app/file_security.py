"""Small resource-bound admission checks for untrusted DOCX (ZIP) uploads.

This is defense-in-depth around python-docx, not a claim that parsing arbitrary
Office files is completely sandboxed. The bytes are never extracted to disk.
"""
from io import BytesIO
from pathlib import PurePosixPath
from zipfile import BadZipFile, ZipFile


class UnsafeDocument(ValueError):
    """A document exceeds parser resource/security limits."""


MAX_ENTRIES = 250
MAX_UNCOMPRESSED = 24_000_000
MAX_MEMBER = 10_000_000
MAX_RATIO = 200
REQUIRED = {'[Content_Types].xml', 'word/document.xml'}


def validate_docx(data: bytes) -> None:
    """Validate DOCX container before handing it to the third-party parser.

    Allow only ordinary ZIP entries, reject traversal, encrypted members, macro
    payloads and absurd expansion sizes. Not a filesystem extractor.
    """
    try:
        with ZipFile(BytesIO(data), mode='r') as archive:
            entries = archive.infolist()
            if not entries or len(entries) > MAX_ENTRIES:
                raise UnsafeDocument('DOCX has too many ZIP entries')
            seen: set[str] = set()
            total = 0
            for item in entries:
                name = item.filename
                path = PurePosixPath(name)
                if not name or name.startswith('/') or '\\' in name or ':' in name or '..' in path.parts:
                    raise UnsafeDocument('DOCX has an unsafe member path')
                if name in seen:
                    raise UnsafeDocument('DOCX contains duplicate archive entries')
                seen.add(name)
                if item.flag_bits & 1:
                    raise UnsafeDocument('Encrypted DOCX is not supported')
                # Block symlinks and non-regular ZIP entries that have no place in DOCX.
                mode = (item.external_attr >> 16) & 0o170000
                if mode not in (0, 0o100000, 0o040000):
                    raise UnsafeDocument('Unsupported DOCX archive member type')
                if item.is_dir():
                    continue
                total += item.file_size
                if item.file_size > MAX_MEMBER or total > MAX_UNCOMPRESSED:
                    raise UnsafeDocument('DOCX expands beyond document processing limit')
                if item.file_size and (not item.compress_size or
                    item.file_size > item.compress_size * MAX_RATIO):
                    raise UnsafeDocument('DOCX compression ratio exceeds safe limit')
                if name.lower().endswith('vbaproject.bin'):
                    raise UnsafeDocument('Macro-enabled documents are not supported')
            if not REQUIRED.issubset(seen):
                raise UnsafeDocument('DOCX is missing required document parts')
    except BadZipFile as exc:
        raise UnsafeDocument('Invalid DOCX ZIP container') from exc

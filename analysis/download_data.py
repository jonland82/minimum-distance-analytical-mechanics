"""Fetch the public LHAASO archive, verify it, and extract safely."""
from pathlib import Path
import hashlib
import json
import zipfile
import requests

OUT=Path(__file__).resolve().parent
URL='https://www.nhepsdc.cn/api/resource/detail/file/download/283/1352'
SHA='9f694d18c5e2f65562c6f841c500361385bee6351e45544c5a368d7e79c10644'
p=OUT/'lhaaso_data.zip'
if not p.exists():
    with requests.get(URL,stream=True,timeout=(30,60)) as r:
        r.raise_for_status()
        with p.open('wb') as dest:
            for chunk in r.iter_content(1024*1024):
                dest.write(chunk)
digest=hashlib.sha256(p.read_bytes()).hexdigest()
if digest!=SHA:
    raise RuntimeError(f'Archive checksum changed: {digest}; inspect before proceeding')
root=(OUT/'lhaaso_data').resolve()
with zipfile.ZipFile(p) as z:
    assert all((root/n).resolve().is_relative_to(root) for n in z.namelist())
    z.extractall(root)
    files=[dict(name=i.filename,bytes=i.file_size) for i in z.infolist()]
metadata=dict(url=URL,
    landing_page='https://www.nhepsdc.cn/resource/astro/lhaaso/paper-PRL2024-133071501',
    dataset_doi='10.12402/opendata/LHAASO/20240829100037',
    retrieved_date='2026-11-13',sha256=digest,bytes=p.stat().st_size,files=files)
(OUT/'archive_manifest.json').write_text(json.dumps(metadata,indent=2))
print('Verified archive:',p.stat().st_size,'bytes;',len(files),'entries')

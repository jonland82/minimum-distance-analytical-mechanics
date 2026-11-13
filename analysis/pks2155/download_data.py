"""Fetch and verify the HESS public test archive; retain all original terms."""
from pathlib import Path
import hashlib,tarfile
import requests

OUT=Path(__file__).resolve().parent
URL='https://www.mpi-hd.mpg.de/hfm/HESS/pages/dl3-dr1/hess_dl3_dr1.tar'
EXPECTED='cb0439101300d072e084c255225a863c8dafe1fbf76814ab6188f9b112d7f354'
p=OUT/'hess_dl3_dr1.tar'
if not p.exists():
    with requests.get(URL,stream=True,timeout=(20,60)) as r:
        r.raise_for_status()
        with p.open('wb') as f:
            for chunk in r.iter_content(1024*1024):f.write(chunk)
digest=hashlib.sha256(p.read_bytes()).hexdigest()
if digest!=EXPECTED:raise RuntimeError('Archive changed; inspect its provenance and terms before using it')
root=(OUT/'dl3').resolve()
with tarfile.open(p) as z:
    assert all((root/i.name).resolve().is_relative_to(root) and not i.issym() and not i.islnk() for i in z.getmembers())
    z.extractall(root,filter='data')
print((root/'README.txt').read_text())

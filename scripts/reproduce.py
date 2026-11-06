"""Repeat tests and generate a deterministic, transparent local receipt."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
run=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
tracked=['src/gaugerail.py','tests/test_gaugerail.py','THEOREM.md','PRIOR_ART.md']
receipt={
    'project':'AXEZENT GaugeRail-001',
    'exit_code':run.returncode,
    'test_stderr':run.stderr,
    'verified_with':sys.version,
    'file_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in tracked},
    'labels':{'mathematics':'PROVED_EXACT_BY_TEXT_PROOF','test_suite':'PASS' if run.returncode==0 else 'FAIL',
              'novelty':'NOT_ESTABLISHED','economic_value':'NOT_ESTABLISHED'}
}
(ROOT/'REPRODUCIBILITY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n',encoding='utf8')
print(json.dumps({'exit_code':run.returncode,'test_line':next((x for x in run.stderr.splitlines() if x.startswith('Ran ')),'none'),
                 'receipt':'REPRODUCIBILITY_RECEIPT.json'},indent=2))
if run.returncode:
    sys.exit(run.returncode)

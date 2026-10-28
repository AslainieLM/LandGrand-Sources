from pathlib import Path
import hashlib,importlib.util,json,shutil,sys
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent
REFERENCE=ROOT/'reference.docx'
FINAL=Path(r'D:\Projects\LandGrand-Sources\LandGrand\Manuscript\Drafts\Land Grand - Chapter I - Revised - v7.docx')
assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest()=='ac0d6c09f6b092c824132d351c0035d663afda281cba5505700e7c65981f4f55'
SCRIPT=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1025.11240\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('packaged_docx_diff',SCRIPT)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def native_render(render_py,docx,outdir):
    source={REFERENCE.resolve():ROOT.parent/'chapter1-openings-2026-10-28/render',FINAL.resolve():ROOT/'render-1'}[Path(docx).resolve()]
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for page in source.glob('page-*.png'):shutil.copyfile(page,Path(outdir)/page.name)
module._run_render=native_render
sys.argv=[str(SCRIPT),str(REFERENCE),str(FINAL),'--outdir',str(ROOT/'fidelity-1')]
module.main()
old=Image.open(ROOT/'fidelity-1/a_render/page-1.png').convert('RGB')
new=Image.open(ROOT/'fidelity-1/b_render/page-1.png').convert('RGB')
assert old.size==new.size and ImageChops.difference(old,new).getbbox() is None
print('Entire first page is pixel-identical; intended changes begin in the local survey discussion.')

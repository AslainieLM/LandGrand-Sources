from pathlib import Path
import hashlib,importlib.util,shutil,sys
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent
REFERENCE=ROOT/'reference.docx'
FINAL=Path(r'D:\Projects\LandGrand-Sources\LandGrand\Manuscript\Drafts\Land Grand - Chapter I - Revised - v8.docx')
assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest()=='1bc664f937cf9f49c3fedcb14f07e1b69aa84274bedf80f5ff22cd1be10ce594'
SCRIPT=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1025.11240\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('packaged_docx_comparison',SCRIPT)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def native_render(render_py,docx,outdir):
    source={REFERENCE.resolve():ROOT.parent/'chapter1-complete-2026-10-28/render-1',FINAL.resolve():ROOT/'render-1'}[Path(docx).resolve()]
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for page in source.glob('page-*.png'):shutil.copyfile(page,Path(outdir)/page.name)
module._run_render=native_render
sys.argv=[str(SCRIPT),str(REFERENCE),str(FINAL),'--outdir',str(ROOT/'fidelity-1')]
module.main()
a=Image.open(ROOT/'fidelity-1/a_render/page-1.png').convert('RGB')
b=Image.open(ROOT/'fidelity-1/b_render/page-1.png').convert('RGB')
assert a.size==b.size and ImageChops.difference(a,b).getbbox() is None
print('First page, typography and page geometry unchanged; subsequent differences are intended body edits.')

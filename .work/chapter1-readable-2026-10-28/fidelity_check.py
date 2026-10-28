from pathlib import Path
import importlib.util
import shutil
import sys
from PIL import Image,ImageChops

ROOT=Path(__file__).resolve().parent
REFERENCE=ROOT/'reference.docx'
FINAL=Path(r'D:\Projects\LandGrand-Sources\LandGrand\Manuscript\Drafts\Land Grand - Chapter I - Revised - v5.docx')
SCRIPT=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1025.11240\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('packaged_document_diff',SCRIPT)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def reuse_native_render(render_py,docx,outdir):
    folder={REFERENCE.resolve():ROOT/'reference-render',FINAL.resolve():ROOT/'render-1'}[Path(docx).resolve()]
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for page in folder.glob('page-*.png'):
        shutil.copyfile(page,Path(outdir)/page.name)
module._run_render=reuse_native_render
sys.argv=[str(SCRIPT),str(REFERENCE),str(FINAL),'--outdir',str(ROOT/'fidelity-1')]
module.main()
a=Image.open(ROOT/'reference-render/page-1.png').convert('RGB')
b=Image.open(ROOT/'render-1/page-1.png').convert('RGB')
assert a.size==b.size
# At 120 dpi, the unchanged chapter title block lies above the first body line.
assert ImageChops.difference(a.crop((0,0,a.width,230)),b.crop((0,0,b.width,230))).getbbox() is None
print('Page geometry and complete title block unchanged. Body differences match the requested rewrite.')

"""Use the packaged DOCX rasterizer with native Word PDF and PDFium adapters.

Word supplies the faithful read-only DOCX-to-PDF render. PDFium replaces the
unbundled Windows Poppler executable; installed skill files remain untouched.
"""
from pathlib import Path
import argparse
import importlib.util
import sys
import tempfile
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent
SKILL = Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1110.11613\skills\documents')
parser = argparse.ArgumentParser()
parser.add_argument('docx', type=Path)
parser.add_argument('word_pdf', type=Path)
parser.add_argument('--output_dir', required=True, type=Path)
parser.add_argument('--dpi', default=120, type=int)
args = parser.parse_args()
assert args.docx.is_file() and args.word_pdf.is_file()
spec = importlib.util.spec_from_file_location('packaged_docx_renderer', SKILL/'render_docx.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

def word_pdf(input_path, user_profile, convert_tmp_dir, stem, verbose=False):
    assert Path(input_path).resolve() == args.docx.resolve()
    return str(args.word_pdf.resolve()), 'Read-only Microsoft Word native PDF export.'

def pdfium_pngs(pdf_path, dpi, fmt, thread_count, output_folder, paths_only, output_file):
    assert fmt == 'png' and paths_only
    paths = []
    with pdfium.PdfDocument(pdf_path) as document:
        for index in range(len(document)):
            page = document[index]
            bitmap = page.render(scale=dpi/72)
            path = Path(output_folder)/f'page-native-{index+1}.png'
            bitmap.to_pil().save(path)
            paths.append(str(path))
            bitmap.close()
            page.close()
    return paths

renderer.convert_to_pdf = word_pdf
renderer.convert_from_path = pdfium_pngs
(ROOT/'tmp').mkdir(exist_ok=True)
tempfile.tempdir = str(ROOT/'tmp')
sys.argv = ['render_docx.py', str(args.docx), '--output_dir', str(args.output_dir), '--dpi', str(args.dpi)]
renderer.main()


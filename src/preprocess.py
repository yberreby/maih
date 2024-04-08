from .common import *

# Folder with all the source files (which may actually not be PDFs).
src_pdf_path = Path("data") / "src-pdfs"

def path_to_row(p):
    _trunk, ext = os.path.splitext(p)
    
    # Filename including extension, without leading path
    name = p.name
    
    ext = ext[1:]
    return (name, ext, p)

# Create dataframe from list of file paths.
entries = pd.DataFrame(
    columns=["file", "ext", "path"],
    data=map(path_to_row, src_pdf_path.glob("*"))
)
entries.set_index("file", inplace=True)
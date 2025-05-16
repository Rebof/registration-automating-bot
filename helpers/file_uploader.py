import os
from PIL import Image
from pathlib import Path

def ensure_dummy_file_exists():
    file_path = Path(__file__).parent.parent / "dummy.png"
    if not os.path.exists(file_path):
        img = Image.new('RGB', (100, 100), color=(255, 255, 255))
        img.save(file_path)
        print(f"📄 Created dummy file: {file_path}")
    else:
        print(f"📂 Dummy file already exists.")
    return str(file_path)

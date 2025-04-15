import os
from datetime import datetime

def extract_basic_metadata(file_path: str) -> dict:
    stat = os.stat(file_path)
    return {
        "filename": os.path.basename(file_path),
        "size_kb": round(stat.st_size / 1024, 2),
        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
    }
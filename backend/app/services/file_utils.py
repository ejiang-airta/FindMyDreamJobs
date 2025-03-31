import os
from app.config.settings import UPLOAD_DIR
import logging

# Setup the logger
logger = logging.getLogger("app")

def generate_resume_file(resume_id: int, content: str, is_optimized: bool = False) -> tuple[str, str]:
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"resume_{resume_id}_{'optimized' if is_optimized else 'original'}.txt"
    filepath = os.path.join(UPLOAD_DIR, filename)

    logger.info(f"✅ Writing optimized resume to: {filepath}")

    # Write the resume content to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath, filename

# clean-up function to delete the file after processing:
def cleanup_file(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"🧹 Deleted temporary file: {filepath}")
        else:
            logger.warning(f"⚠️ Tried to delete non-existent file: {filepath}")
    except Exception as e:
        logger.error(f"❌ Error deleting file {filepath}: {e}")


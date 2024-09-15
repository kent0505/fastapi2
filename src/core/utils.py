from fastapi                   import FastAPI, UploadFile
from dotenv                    import load_dotenv
from contextlib                import asynccontextmanager
from datetime                  import datetime
from src.core.config           import settings
from src.core.models.db_helper import db_helper
from src.core.models.base      import Base
import logging
import time
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()

    logging.basicConfig(
        level    = settings.log_level, 
        format   = settings.log_format,
        datefmt  = settings.log_datefmt,
    )
    logging.info("STARTUP")

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # shutdown
    logging.info("SHUTDOWN")
    await db_helper.dispose()

def get_current_timestamp() -> int:
   return int(time.time())


def format_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime(settings.date_format)


def remove_dash(data: str) -> str:
    return data.replace("-", " ")


def check_picked_file(file:  UploadFile) -> bool:
    if file.filename and str(file.content_type).startswith("image/"):
        return True
    else:
        return False


def remove_image(title: str) -> None:
    try:
        os.remove(f"{settings.static}/{title}")
        logging.warning("IMAGE REMOVED")
    except:
        logging.warning("IMAGE NOT FOUND")


def add_image(file: UploadFile) -> str:
    try:
        timestamp   = get_current_timestamp()           # 1706520261
        format      = str(file.filename).split('.')[-1] # jpg/jpeg/png
        unique_name = f"{timestamp}.{format}"           # 1706520261.png
        file_name   = os.path.join(settings.static, unique_name)

        with open(file_name, "wb") as image_file:
            image_file.write(file.file.read())

        logging.warning("IMAGE ADDED")
        return unique_name
    except Exception as e:
        try:
            logging.warning(e)
        finally:
            logging.warning("IMAGE NOT ADDED")
            return ""
from typing   import List, Any
from pydantic import BaseModel
import logging
import time
import os


class Settings(BaseModel):
    protocol:       str   = os.getenv("PROTOCOL", "http")
    host:           str   = os.getenv("HOST", "localhost:8000")
    url:            str   = protocol + "://" + host
    # cors
    allow_origins:  List  = ["https://" + host, "https://www." + host]
    allow_creds:    bool  = True
    allow_methods:  List  = ["*"]
    allow_headers:  List  = ["*"]
    # folders path
    static:         str   = "static"
    templates:      str   = "templates"
    static_path:    str   = "/" + static
    templates_path: str   = "/" + templates
    # logging
    log_filename:   str   = "logfile.log"
    log_level:      Any   = logging.INFO
    log_format:     str   = "%(asctime)s - %(levelname)s - %(message)s"
    log_datefmt:    str   = "%d-%m-%Y %H:%M:%S" # 29-01-2024 14:19:28
    # jwt
    jwt_key:        str   = os.getenv("KEY", "xyz")
    jwt_algorithm:  str   = "HS256"
    jwt_expiry:     float = time.time() + 60 * 60 * 168 # 168 hours = 1 week
    # db
    db_url:         str   = "sqlite+aiosqlite:///sqlite.db"
    db_echo:        bool  = False
    # others
    date_format:    str   = "%d.%m.%Y"                           # 29.01.2024
    swagger_ui:     dict  = {"defaultModelsExpandDepth": -1}     # hide schemas from swagger
    bot_token:      str   = os.getenv("BOT_TOKEN", "")

settings = Settings()
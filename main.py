from fastapi import FastAPI
from routers import webpageParser
import logging

app = FastAPI()
app.include_router(webpageParser.router)

logger = logging.getLogger(__name__)

def initialiseLogger():
    logging.basicConfig(filename='recipe-randomizer-website-parser.log', level=logging.WARNING)
    logger.warning('Logger initialised')

initialiseLogger()
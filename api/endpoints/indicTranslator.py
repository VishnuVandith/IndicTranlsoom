from fastapi import APIRouter
import time
from api.middleware.logging import logger
from api.utils.inidic_translator_helper import translate_text, lores_codes_inverted  # Adjust the import according to your project structure
from indicnlp.tokenize.sentence_tokenize import sentence_split
from fastapi.responses import JSONResponse
from indicnlp import common

router = APIRouter()

common.set_resources_path(r"indic_nlp_resources")

@router.post("/heyy")
async def log_hello():
    logger.info("This is a message")
    return {"Messg" : "Hello"}

@router.post("/translate/{src}/{tgt}")
async def translate(src: str, tgt: str, text: str):
    logger.info("Starting the translation function")  # This should now log correctly
    st = time.perf_counter()


    src_lang = lores_codes_inverted[src]
    tgt_lang = lores_codes_inverted[tgt]

    sentences = sentence_split(text, lang=src)

    translation = translate_text(src_lang=src_lang, tgt_lang=tgt_lang, input_sentences=sentences)

    et = time.perf_counter()
    tt = et - st  # Adjusted timing calculation

    logger.info("Total time elapsed: %s seconds", tt)  # Log total time elapsed

    return JSONResponse({"Translation": "".join(translation)})
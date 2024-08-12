import torch
import os
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from IndicTransTokenizer.IndicTransTokenizer.processor import IndicProcessor

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


lores_codes_inverted = {
    "asm": "asm_Beng", 
    "awa": "awa_Deva",
    "ben": "ben_Beng",
    "bho": "bho_Deva",
    "brx": "brx_Deva",
    "doi": "doi_Deva",
    "eng": "eng_Latn",
    "gom": "gom_Deva",
    "guj": "guj_Gujr",
    "hin": "hin_Deva",
    "hne": "hne_Deva",  
    "kan": "kan_Knda",  
    "kas": "kas_Arab",  
    "kha": "kha_Latn", 
    "lus": "lus_Latn", 
    "mag": "mag_Deva", 
    "mai": "mai_Deva", 
    "mal": "mal_Mlym",  
    "mar": "mar_Deva",  
    "mni": "mni_Mtei", 
    "nep": "npi_Deva",   
    "ori": "ory_Orya",   
    "pan": "pan_Guru",   
    "san": "san_Deva",   
    "sat": "sat_Olck",   
    "snd": "snd_Arab",   
    "tam": "tam_Taml",   
    "tel": "tel_Telu",   
    "urd": "urd_Arab", 
}

ip = IndicProcessor(inference=True)

def get_model(src: str, tgt: str):
    if src == "eng_Latn":
        return "ai4bharat/indictrans2-en-indic-1B"
    if tgt == "eng_Latn":
        return "ai4bharat/indictrans2-indic-en-1B"
    return "ai4bharat/indictrans2-indic-indic-1B"

def translate_text(src_lang: str, tgt_lang: str, input_sentences: list):
    model_name = get_model(src=src_lang, tgt=tgt_lang)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # Set to GPU if available

    model.to(DEVICE)  # Move the model to the GPU

    batch = ip.preprocess_batch(
        input_sentences,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
    )

    # Tokenize the sentences and generate input encodings
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        return_attention_mask=True,
    ).to(DEVICE)

    # Generate translations using the model
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1,
        )

    # Decode the generated tokens into text
    generated_tokens = generated_tokens.detach().to("cpu")  # Move generated tokens back to CPU
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(
            generated_tokens.tolist(),
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

    # Postprocess the translations, including entity replacement
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

    del tokenizer, model, model_name

    return translations

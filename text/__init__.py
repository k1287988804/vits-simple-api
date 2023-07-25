""" from https://github.com/keithito/tacotron """
import config
from text import cleaners


def text_to_sequence(text, symbols, cleaner_names, bert_embedding=False):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
      Args:
        text: string to convert to a sequence
        cleaner_names: names of the cleaner functions to run the text through
      Returns:
        List of integers corresponding to the symbols in the text
    '''

    _symbol_to_id = {s: i for i, s in enumerate(symbols)}

    if bert_embedding:
        cleaned_text, char_embeds = bert_chinese_clean_text(text)
        sequence = [_symbol_to_id[symbol] for symbol in cleaned_text.split()]
    else:
        cleaned_text = _clean_text(text, cleaner_names)
        sequence = [_symbol_to_id[symbol] for symbol in cleaned_text if symbol in _symbol_to_id.keys()]

    if bert_embedding:
        return sequence, char_embeds
    else:
        return sequence


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception('Unknown cleaner: %s' % name)
        text = cleaner(text)
    return text


def bert_chinese_clean_text(text):
    import torch
    from vits_pinyin import VITS_PinYin
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # pinyin
    tts_front = VITS_PinYin(f"{config.ABS_PATH}/bert", device)
    cleaner = getattr(cleaners, "bert_chinese_cleaners")
    cleaned_text = cleaner(text)
    phonemes, char_embeds = tts_front.chinese_to_phonemes(cleaned_text)
    return phonemes, char_embeds

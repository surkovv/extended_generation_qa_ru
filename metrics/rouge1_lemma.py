from typing import List, Tuple, Any
from nltk.tokenize import word_tokenize
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def rouge1_lemma(y_true: List[str], y_predicted: List[str]) -> float:
    rouge_sum = 0
    for answer_true, answer_pred in zip(y_true, y_predicted):
        rouge_sum += rouge1_lemma_count_one(answer_true, answer_pred)
    return rouge_sum / len(y_true)


def lemma_tokenize(string: str):
    tokens = word_tokenize(string)
    result = []
    for token in tokens:
        parsed = morph.parse(token)
        if not parsed:
            continue
        parsed = parsed[0]
        if 'PNCT' in parsed.tag:
            continue
        result.append(parsed.normal_form)
    return result
    

def rouge1_lemma_count_one(answer_true: str, answer_pred: str) -> float:
    tokens_true, tokens_pred = lemma_tokenize(answer_true), lemma_tokenize(answer_pred)
    matched = 0
    for token in tokens_true:
        if token in tokens_pred:
            matched += 1
    if len(tokens_true) == 0:
        return 0
    return matched / len(tokens_true)

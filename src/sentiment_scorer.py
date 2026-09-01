"""
Scores text using the Loughran-McDonald financial sentiment dictionary.

Unlike general-purpose sentiment tools (built for movie reviews, tweets,
etc.), LM was built specifically from SEC filing text — so words like
"liability," "tax," and "cost" are correctly treated as neutral financial
terms rather than flagged as negative.
"""
import re
import pandas as pd


def load_lm_dictionary(csv_path: str) -> dict:
    """
    Load the LM Master Dictionary CSV and return a dict mapping each
    sentiment category to a set of words belonging to it.

    Note: category columns (Negative, Positive, etc.) store a non-zero
    YEAR the word was added to that category, not a simple 1/0 flag —
    so membership means "value != 0", not "value == 1".
    """
    df = pd.read_csv(csv_path)

    categories = [
        "Negative", "Positive", "Uncertainty",
        "Litigious", "Strong_Modal", "Weak_Modal", "Constraining",
    ]

    word_sets = {}
    for category in categories:
        words_in_category = df.loc[df[category] != 0, "Word"]
        # LM words are uppercase; we'll match against uppercased tokens
        word_sets[category] = set(words_in_category.str.upper())

    return word_sets


def tokenize(text: str) -> list[str]:
    """
    Split text into uppercase word tokens, matching how the LM
    dictionary itself is cased. Strips punctuation/numbers.
    """
    words = re.findall(r"[A-Za-z]+", text)
    return [w.upper() for w in words]


def score_text(text: str, word_sets: dict) -> dict:
    """
    Score a piece of text against the LM dictionary.

    Returns raw counts per category, total word count, and each
    category's proportion of total words (the standard way LM scores
    are reported, since raw counts aren't comparable across documents
    of different lengths).
    """
    tokens = tokenize(text)
    total_words = len(tokens)

    result = {"total_words": total_words}

    for category, word_set in word_sets.items():
        count = sum(1 for token in tokens if token in word_set)
        result[f"{category.lower()}_count"] = count
        result[f"{category.lower()}_pct"] = (
            count / total_words if total_words > 0 else 0.0
        )

    return result


if __name__ == "__main__":
    from text_extractor import extract_text_from_html, extract_mdna_section

    word_sets = load_lm_dictionary("data/raw/LM_MasterDictionary.csv")
    print("Loaded LM dictionary:")
    for category, words in word_sets.items():
        print(f"  {category}: {len(words)} words")

    text = extract_text_from_html("data/raw/aapl_2026-07-31.htm")
    mdna = extract_mdna_section(text)

    scores = score_text(mdna, word_sets)
    print("\nMD&A sentiment scores:")
    for key, value in scores.items():
        print(f"  {key}: {value}")

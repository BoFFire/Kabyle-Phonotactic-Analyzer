import re
import random
import unicodedata
import argparse
from nltk import FreqDist, word_tokenize

# Set a fixed seed for reproducible random selection
random.seed(42)

# Kabyle official alphabet, including "o" and "v" used in borrowed words
kabyle_letters = "abcčdḍeɛfgǧɣhḥijklmnpqrṛsṣtṭuwxyzẓov"
# Define vowels: official vowels are a, e, i, u and we add "o"
vowels = "aeiuo"

def robust_clean_word(word):
    """
    Clean the input word robustly:
      - Normalize Unicode to NFC.
      - Convert to lowercase.
      - Strip punctuation from the boundaries.
      - Remove internal hyphens.
      - Remove any characters not in the Kabyle alphabet.
    """
    # Normalize Unicode (ensuring consistency for characters with diacritics)
    word = unicodedata.normalize("NFC", word)
    # Convert to lowercase
    word = word.lower()
    # Remove punctuation from the beginning and end of the word
    word = word.strip(".,;:!?\"'()[]{}«»")
    # Remove internal hyphens (merging segments)
    word = re.sub(r"-", "", word)
    # Remove any character not in the defined Kabyle alphabet
    word = re.sub(f"[^{kabyle_letters}]", "", word)
    return word

def word_to_cv(word):
    """
    Convert a cleaned word into its CV pattern based on the Kabyle alphabet.
    Each letter is mapped to 'V' if it is in 'vowels', else 'C'.
    """
    return "".join("V" if letter in vowels else "C" for letter in word)

def process_corpus(file_path):
    """
    Reads the corpus file, tokenizes the text, cleans tokens,
    converts them to CV patterns, and returns both the frequency distribution
    of the patterns and a mapping from patterns to lists of example words.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None, None

    # Tokenize using NLTK's word_tokenize
    tokens = word_tokenize(text)

    cleaned_words = []
    for token in tokens:
        cleaned = robust_clean_word(token)
        # Keep only tokens that are non-empty and contain only letters
        if cleaned and cleaned.isalpha():
            cleaned_words.append(cleaned)

    # Convert each word to its CV pattern
    cv_patterns = [word_to_cv(word) for word in cleaned_words]

    # Map each pattern to a list of corresponding words for random selection
    pattern_examples = {}
    for word, pattern in zip(cleaned_words, cv_patterns):
        pattern_examples.setdefault(pattern, []).append(word)

    # Calculate frequency distribution of the CV patterns
    fdist = FreqDist(cv_patterns)
    return fdist, pattern_examples

def main():
    parser = argparse.ArgumentParser(
        description="Kabyle Phonotactic Analyzer: computes CV patterns from a text corpus."
    )
    parser.add_argument("file", help="Path to the .txt file to analyze")
    parser.add_argument("-n", type=int, default=22, help="Number of top patterns to display (default: 22)")
    args = parser.parse_args()

    fdist, pattern_examples = process_corpus(args.file)
    if fdist is None:
        return

    print(f"\nAnalysis of file: {args.file}\n")
    for pattern, freq in fdist.most_common(args.n):
        # Select a random example word for this pattern
        example = random.choice(pattern_examples.get(pattern, ["No example"]))
        print(f"{pattern}: {freq}    (e.g., '{example}')")

if __name__ == '__main__':
    main()

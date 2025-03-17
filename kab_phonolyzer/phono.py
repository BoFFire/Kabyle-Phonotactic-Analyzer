import re
import random
import unicodedata
import csv
from collections import defaultdict
from nltk import FreqDist, word_tokenize

# Import dependency checks
from .dependencies import install_nltk, ensure_punkt

install_nltk()
ensure_punkt()

hyphen_pattern = re.compile(r"-")
kabyle_letters = "abcčdḍeɛfgǧɣhḥijklmnpqrṛsṣtṭuwxyzẓov"
non_kabyle_pattern = re.compile(f"[^{re.escape(kabyle_letters)}]")

random.seed(42)
vowels = "aeiuo"

def robust_clean_word(word: str) -> str:
    word = unicodedata.normalize("NFC", word)
    word = word.lower().strip(".,;:!?\"'()[]{}«»")
    word = hyphen_pattern.sub("", word)
    return non_kabyle_pattern.sub("", word)

def word_to_cv(word: str) -> str:
    return "".join("V" if c in vowels else "C" for c in word)

def process_corpus(file_path: str, batch_size: int = None) -> tuple[FreqDist, dict]:
    fdist = FreqDist()
    pattern_examples = defaultdict(list)
    current_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                current_lines.append(line)

                if (batch_size and len(current_lines) >= batch_size) or line.endswith('\n'):
                    text_chunk = ' '.join(current_lines)
                    tokens = word_tokenize(text_chunk)
                    cleaned = [robust_clean_word(t) for t in tokens if robust_clean_word(t)]
                    for word in cleaned:
                        pattern = word_to_cv(word)
                        fdist[pattern] += 1
                        pattern_examples[pattern].append(word)
                    current_lines = []
            if current_lines:
                text_chunk = ' '.join(current_lines)
                tokens = word_tokenize(text_chunk)
                cleaned = [robust_clean_word(t) for t in tokens if robust_clean_word(t)]
                for word in cleaned:
                    pattern = word_to_cv(word)
                    fdist[pattern] += 1
                    pattern_examples[pattern].append(word)
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return None, None
    return fdist, pattern_examples

def print_results(fdist: FreqDist, pattern_examples: dict, top_n: int) -> None:
    print(f"\nAnalysis of file:\n")
    for pattern, freq in fdist.most_common(top_n):
        examples = pattern_examples.get(pattern, ["No example"])
        example = random.choice(examples)
        print(f"{pattern}: {freq} (e.g., '{example}')")

def write_to_csv(output_path: str, fdist: FreqDist, pattern_examples: dict, top_n: int) -> None:
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Pattern', 'Frequency', 'Example'])
        for pattern, freq in fdist.most_common(top_n):
            examples = pattern_examples.get(pattern, ["No example"])
            example = random.choice(examples)
            writer.writerow([pattern, freq, example])

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Kabyle Phonotactic Analyzer")
    parser.add_argument("file", help="Path to text file")
    parser.add_argument("-n", type=int, default=22, help="Number of top patterns to display")
    parser.add_argument("--batch-size", type=int, help="Number of lines per batch")
    parser.add_argument("--output", type=str, help="Path to save results as CSV")
    args = parser.parse_args()

    fdist, pattern_examples = process_corpus(args.file, args.batch_size)
    if not fdist:
        return

    if args.output:
        write_to_csv(args.output, fdist, pattern_examples, args.n)
        print(f"Results saved to: {args.output}")
    else:
        print_results(fdist, pattern_examples, args.n)

if __name__ == "__main__":
    main()

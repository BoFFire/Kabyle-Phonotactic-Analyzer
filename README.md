# Kabyle Phonotactic Analyzer

Kabyle Phonotactic Analyzer: computes CV patterns from a text corpus.

## Usage

```bash
git clone https://github.com/BoFFire/Kabyle-Phonotactic-Analyzer.git
```
Installation :

```bash
cd Kabyle-Phonotactic-Analyzer
```

```bash
pip install .
```

How to use it ?

```bash
kab-phonolyzer <file_path> [options]
```
```bash
kab-phonolyzer kab.txt -n 20 --batch-size 1000
```
```bash
kab-phonolyzer kab.txt --output results.csv --n 20
```
For large corpus :

```bash
kab-phonolyzer large_corpus.txt --batch-size 5000 --output analysis.csv
```

Example :

```bash
$ kab-phonolyzer kab.txt --n 3
Analysis of file:

CVC: 68339 (e.g., 'seg')
CVCCVC: 66497 (e.g., 'werǧin')
CVCCV: 37473 (e.g., 'dinna')
```

Pragmatic usage :

You can use

```python
from kab_phonolyzer.phono import process_corpus, analyze_corpus
```

Process a Corpus :

```python
from kab_phonolyzer.phono import process_corpus

# Process a file and get raw data
fdist, examples = process_corpus("kab.txt", batch_size=1000)

# Access frequency distribution and examples
print(fdist.most_common(5))  # Top 5 patterns
print(examples["CVC"])  # Example words for pattern "CVC"
```

Analyze and save results :

```python
from kab_phonolyzer.phono import analyze_corpus

# Analyze and save to CSV
analyze_corpus("kab.txt", top_n=10, batch_size=500, output="results.csv")
```

Pragmatic usage :

```python
from kab_phonolyzer.phono import process_corpus

# Process a corpus and save results
fdist, examples = process_corpus("kab.txt", batch_size=1000)

# Save to CSV manually
with open("custom_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Pattern", "Frequency", "Example"])
    for pattern, freq in fdist.most_common(20):
        ex = random.choice(examples.get(pattern, ["No example"]))
        writer.writerow([pattern, freq, ex])
```

Convert a Single Word to CV Pattern :

```python
from kab_phonolyzer.phono import word_to_cv

word = "aselkim"
cv_pattern = word_to_cv(word)
print(f"'{word}' → {cv_pattern}")  # Output: 'vcvccvc'
```

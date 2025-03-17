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
kab-phonolyzer kab.txt -n 20 --batch-size 1000
```
```bash
kab-phonolyzer kab.txt --output results.csv --n 20
```

For large corpus :

```bash
kab-phonolyzer large_corpus.txt --batch-size 5000 --output analysis.csv
```

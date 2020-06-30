
# File-Stat-Analyzer

- Analyze files
- Parse PDF files, find ISBN, keywords, etc.

Python (Django) program that parses files with millions of rows representing files descriptions and fast insert in PostgresQL DB directly from buffer. The purpose is fast lookup, report analyses, classification. Also analyzes PDF files: image OCR, parse content, find keywords, etc.

# Prerequisites

- `stat` command in linux
- [PostgreSQL](https://www.postgresql.org/)
- `python3.8`
- [pipenv](https://pypi.org/project/pipenv/)

# Installation

Linux terminal:
```bash
# get the latest snapshot
git clone https://github.com/CosminEugenDinu/File-Stat-Analyzer.git
cd File-Stat-Analyzer

# Ubuntu 18.04 LTS prerequisites for building psycopg2 - Python PostgreSQL Connector
sudo apt update && sudo apt install -y libpq-dev python3.8-dev

# install python dependencies
pipenv install --python=$(which python3.8) --dev

```



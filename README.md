# jml

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**jml** is a lightweight, fast, and efficient **JSON ↔ YAML converter CLI**. It allows you to convert, validate, and pretty-print files. Perfect for developers, CI/CD pipelines, and quick command-line conversions.

---

## 💡 Key Features

* **Convert between JSON and YAML**
* **Pretty-print JSON** (human-readable format)
* **Subcommand**: `validate` to check file validity
* **stdin/stdout support** – can read from pipes
* **Write output to file** using `-o/--output`
* Fully **flag-based CLI**, order of flags is flexible

---

## ⚙️ Installation

```bash
# Local development installation
pip install -e .

# From PyPI (once published)
pip install jml
```

---

## 🏃 Usage

### 1. File-based conversion

```bash
# YAML → JSON (single-line)
jml -j -i config.yaml

# JSON → YAML
jml -y --input data.json

# JSON → Pretty JSON
jml -jpi config.yaml

# Write output to a file
jml -y -i data.json -o data.yml
```

### 2. Pipe / stdin usage

```bash
# Using pipe
cat a.json | jml -y

# Using redirect
jml -j < config.yaml > config.json
```

### 3. Subcommand – validate file

```bash
jml validate config.yaml
# output: ✓ config.yaml is valid
```

---

## 🔹 Flags Overview

| Flag                | Description                          |
| ------------------- | ------------------------------------ |
| `-j, --json`        | Output JSON                          |
| `-y, --yaml`        | Output YAML                          |
| `-p, --pretty`      | Pretty JSON output (only for JSON)   |
| `-o, --output PATH` | Output file                          |
| `-i, --input PATH`  | Input file (optional, can use stdin) |

---

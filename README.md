# Program Python Course 26

Small Python course project with two homework modules:

- 📊 **Homework 01 Sort**: external merge sort for a large file with 32-bit numbers.
- ⌚ **Homework 02 Django**: a Django web app for a personal watch catalog.

This repository is written for teachers, classmates, and other developers who
want to review or run the homework quickly.

## 🧰 Tech Stack

- Python `>= 3.12`
- [uv](https://docs.astral.sh/uv/) for project and package management
- Django for homework 02

## ⚙️ Install uv

`uv` is a fast Python package and project manager.

Download links:

- [uv for Windows](https://github.com/astral-sh/uv/releases/latest)
- [uv for macOS](https://github.com/astral-sh/uv/releases/latest)
- [Official uv install guide](https://docs.astral.sh/uv/getting-started/installation/)

Simple install commands:

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS Terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, check it:

```bash
uv --version
```

## 🚀 Quick Start

Clone the project:

```bash
git clone <repository-url>
cd program-python-course-26
```

Install project dependencies:

```bash
uv sync
```

### Homework 01: External Sort

Run from the project root:

```bash
uv run --package homework-01-sort python -m homework_01_Sort.main src/homework_01_Sort/random_numbers.txt 100000
```

The program reads numbers from `random_numbers.txt`, sorts them with external
merge sort, and creates sorted output files near the input file.

### Homework 02: Django Watch Catalog

Run from the project root:

```bash
uv run python src/homework_02_Django/manage.py runserver
```

Open the local website:

```text
http://127.0.0.1:8000/
```

## 📁 Project Structure

```text
program-python-course-26/
|-- README.md
|-- pyproject.toml
|-- uv.lock
|-- main.py
`-- src/
    |-- homework_01_Sort/
    `-- homework_02_Django/
```

## 📝 Project Notes

- The repository uses a `uv` workspace with two homework projects under `src/`.
- Homework 01 focuses on file processing, binary data, multiprocessing, and
  external sorting.
- Homework 02 focuses on Django models, views, forms, templates, static files,
  search, create, edit, delete, and a small SQLite database.

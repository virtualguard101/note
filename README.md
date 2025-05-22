# virtualguard's note

Personal notebook written in Chinese, use for recording my self learing process of **C**omputer **S**cience.

## Read Locally

Use [MkDocs](https://github.com/mkdocs/mkdocs) & [Material](https://github.com/squidfunk/mkdocs-material) to construct in localhost.

- Clone the repository

```bash
git clone -b main https://github.com/virtualguard101/note.git
```

- Create a Python virtual environment by `uv` and install dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements
```

- Deploy by `mkdocs` locally

```bash
uv run mkdocs serve
```

Then access [localhost:8000](http://127.0.0.1:8000/) in browser.

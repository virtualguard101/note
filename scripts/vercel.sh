# Install dependencies
python3.12 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Build
source env/bin/activate
mkdocs build --strict -d public

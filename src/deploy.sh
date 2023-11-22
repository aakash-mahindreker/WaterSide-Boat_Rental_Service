exec > >(tee -i deploy.log)
exec 2>&1

/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
/opt/render/project/src/.venv/bin/python -m pip install --upgrade python
/opt/render/project/src/.venv/bin/python app.py

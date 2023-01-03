# Connexion/Flask patch for FOCA

This addresses the issue described in [FOCA](https://github.com/elixir-cloud-aai/foca): https://github.com/elixir-cloud-aai/foca/issues/144
This issue in [Connexion](https://connexion.readthedocs.io/en/latest/index.html) is also of relevance: https://github.com/spec-first/connexion/issues/1617

Patches for `connexion.apps.FlaskApp` and `flask.app.Flask` are in `connexion_patch.py`.
A petstore test app making use of the patches is in `app.py`.

Simply install requirements with:

```bash
pip install -r requirements.txt
```

You can then run the app (on port 3000) with:

```bash
python app.py
```

To see how the patch allows autocompletion and type inference of the FOCA config, open `app.py` in VS Code (with Pylance) and hover over the second `app` (the actual patched Flask app) in `app.app`. The attribute `foca` should be autosuggested.

Usage of the patch in app context with Flask's `current_app` is not yet tested/addressed.

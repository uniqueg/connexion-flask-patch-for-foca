# Connexion/Flask patch for FOCA

This addresses the issue described in
[FOCA](https://github.com/elixir-cloud-aai/foca):
https://github.com/elixir-cloud-aai/foca/issues/144
This issue in
[Connexion](https://connexion.readthedocs.io/en/latest/index.html) is also of
relevance: https://github.com/spec-first/connexion/issues/1617

Patches for `connexion.apps.FlaskApp`, `flask.app.Flask` and
`flask.globals.current_app` are in `connexion_patch.py`. A pet store test app
making use of the patches is in `app.py`.

Simply install requirements with:

```bash
pip install -r requirements.txt
```

You can then run the app (on port 3000) with:

```bash
python app.py
```

To see how the patch allows auto-completion and type inference of the FOCA
config, open `app.py` in VS Code (with Pylance) and hover over the second `app`
(the actual patched Flask app) in `app.app`. The attribute `foca` should be
auto-suggested.

You can also inspect the `controllers.py` module and check how the
`current_app` patch is being used in a way that the editor is aware of the FOCA
configuration types. However, FOCA config types are not unambiguously
annotated, so `mypy` and other type checkers will still complain.

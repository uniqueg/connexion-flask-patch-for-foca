from flask import Flask
from connexion_patch import FlaskApp as current_app, FlaskApp, FocaApp

app: FocaApp = FlaskApp(__name__, specification_dir='./').app  # type: ignore
print(dir(app.foca))
# editor is now aware of `app.foca` and its properties, but only if the type
# `FocaApp` is explicitly hinted at; otherwise the type of `app` is `None` (as
# it is when using the unpatched `FlaskApp`); and assigning `None` to `FocaApp`
# still leads to a type check error that we need to ignore; still, this is an
# improvement, as this is generally hidden from the user, who will likely only
# access the app once it is already returned from FOCA (at which point the
# type is known)
app.run(port=3000)

"""Runs the program when called with "flask run".

To run the application it begins with this file. It connects everything
together. It all creates a shell context, which can be ran with "flask
shell".
"""
from app import app, db
from app.models import User, UserBehaviours


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'UserBehaviours': UserBehaviours}


if __name__ == "__main__":
    app.run()

import os

from flask import (
    Flask,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "replace-this-development-key"
)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(app.instance_path, "sessions")
app.config["SESSION_PERMANENT"] = False
os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)
Session(app)


@app.route("/")
def index():
    session["visit_count"] = session.get("visit_count", 0) + 1
    return render_template(
        "index.html",
        user_language=request.cookies.get("user_language"),
        visit_count=session["visit_count"],
    )


@app.route("/set_language/<language>")
def set_language(language):
    if language not in {"en", "es"}:
        abort(404)

    response = make_response(render_template("set_language.html", language=language))
    response.set_cookie(
        "user_language",
        language,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax",
    )
    return response


@app.route("/reset_session")
def reset_session():
    session.pop("visit_count", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

from . import home
@home.route("/")
def index():
    return "<h1>hello home</h1>"
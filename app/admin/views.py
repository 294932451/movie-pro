from . import admin
@admin.route("/")
def index():
    return "<h1>hello admin</h1>"
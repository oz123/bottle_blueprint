import bottle
from app.views import app as home_app

# you can have other apps for example
#from shop.views import app as shop_app


def make_app():
    """use this function to add more routes from your sub-applications"""
    app = bottle.Bottle()
    app.merge(home_app)
    # app.merge(shop_app)
    return app


app = make_app()


@app.route('/assets/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='assets')


if __name__ == "__main__":
    bottle.debug(True)
    bottle.run(app, host='0.0.0.0', port=8080, reloader=True)

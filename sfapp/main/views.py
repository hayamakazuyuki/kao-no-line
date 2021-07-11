from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    return render_template('index.html')


@main.route('/completed')
def completed():
    if not request.args:
        return render_template('completed.html')

    else:
        search_string = request.args.get('search_string')
        search_value = "%{}%".format(search_string)
        page = request.args.get('page', default=1, type=int)
        return render_template('completed.html', search_string=search_string)

from flask import Flask, render_template, request
from .model import DB, Review
import requests as rq
import json

response = rq.get('https://api.nytimes.com/svc/movies/v2/reviews/search.json?critics-pick=Y&order=by-opening-date&api-key=u78MLfj19FRRfvVP6Sfg6Lc6q1n6MDyN')

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/', methods = ['POST','GET'])
    def root():
        DB.drop_all()
        DB.create_all()
        content = json.loads(response.text)
        # critics_picks = []
        # for i in range(0,len(content['results'])):
        #     critics_picks.append((content['results'][i]['display_title'],content['results'][i]['publication_date'],content['results'][i]['link']['url']))
        
        for i in range(0,len(content['results'])):
                DB.session.add(
                    Review(title = content['results'][i]['display_title'],
                           date = content['results'][i]['publication_date'],
                           link = content['results'][i]['link']['url'])
                )
        DB.session.commit()
        reviews = Review.query.all()
        return render_template("base.html", reviews=reviews)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset', reviews=[])

    # @app.route('/user', methods=['POST'])
    # @app.route('/user/<name>', methods=['GET'])
    # def user(name=None, message=''):
    #     name = name or request.values['user_name']
    #     try:
    #         if request.method == 'POST':
    #             db_user = add_or_update_user(name)
    #             message = f"User {db_user.name} successfully added!"
    #         tweets = User.query.filter(User.name == name).one().tweets
    #     except Exception as e:
    #         message = "Error adding or fetching {}: {}".format(name, e)
    #         tweets = []
    #     return render_template('user.html', title=name, tweets=tweets, 
    #                             message=message)

    return app
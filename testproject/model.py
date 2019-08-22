from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Review(DB.Model):
    title = DB.Column(DB.String(50), primary_key=True)
    date = DB.Column(DB.String(50), nullable=False)
    link = DB.Column(DB.String(50),nullable=False)

    def __repr__(self):
        return '<Review {}, {}, {}'.format(self.title,self.date, self.link)
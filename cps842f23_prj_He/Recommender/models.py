from Recommender import db,app
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_rating = db.relationship('MovieRating', backref='user',lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class MovieRating(db.Model):
    __tablename__ = 'movieRatings'
    id = db.Column(db.Integer,primary_key=True)
    movie = db.Column(db.String(201), nullable=False)
    rating = db.Column(db.Numeric(2,1), nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)
    
    def __repr__(self):
        return f"MovieRating('{self.movie}', '{self.rating}')"

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(201), nullable=False)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Numeric(2,1), default=0, nullable=False)
    director = db.Column(db.String(200))
    

with app.app_context():
    db.create_all()
    #db.drop_all()
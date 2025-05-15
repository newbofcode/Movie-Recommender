from flask import Flask, render_template, redirect, flash, url_for,request,jsonify
from Recommender.forms import RegisterationForm, LoginForm, RatingsForm
from Recommender.models import User, Movies, MovieRating
from flask_paginate import Pagination
from Recommender import app,db
import json,math,re, random,os

@app.route("/")
@app.route("/Home")
def home():
    global Login_email
    Login_email = ''
    return render_template('index.html', title='Home')

Login_email = ''
recommended_list = None
@app.route("/Login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    global Login_email, recommended_list
    if form.validate_on_submit():
        #user = confirmUser(form.email, form.password)
        if confirmUser(form.email.data, form.password.data):
            user = confirmUser(form.email.data, form.password.data)
            flash(f'Welcome back {user[1]}!', 'success')
            Login_email = user[2]
            recommended_list = None
            movie_ratings  = MovieRating.query.all()
            grouped_data = {}
            for rating in movie_ratings:
                user_id = rating.user_id
                movie = rating.movie
                rating_value = float(rating.rating)

                if user_id not in grouped_data:
                    grouped_data[user_id] = []

                grouped_data[user_id].append({'movie': movie, 'rating': rating_value})

            # Write the dictionary to a JSON file
            with open('user_movie_ratings.json', 'w') as json_file:
                json.dump(grouped_data, json_file, indent=4)
            return redirect(url_for('accessHome'))
        else:
            flash(f'Login failed. Please check username and password','danger')
            return redirect(url_for('login'))
    return render_template('login.html',title='Sign In', form=form)

@app.route("/Register", methods=['GET', 'POST'])
def register():
    #auto_register()
    #fillMoviedb()
    #auto_rate()
    form = RegisterationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email = form.email.data).first():
            flash(f'This Email has already been used, please use a different one!', 'danger')
            redirect (url_for('register'))
        else:
            flash(f'Account created, welcome {form.username.data}!', 'success')
            addUsers(form.username.data, form.email.data, form.password.data)
            return redirect(url_for('home'))
    return render_template('register.html',title='Sign Up', form=form)
"""
def auto_rate():
    movies = moviesList('movies.json')
    
    emails = [ "user123@example.com", "awesome_user@gmail.com", "alpha_beta@yahoo.com", "user42@hotmail.com", "cool_dude@outlook.com", "coding_ninja@gmail.com", "python_lover@example.com", "web_master@yahoo.com", "tech_guru@hotmail.com", "dev_ops@gmail.com", "geeky_gamer@example.com", "creative_coder@yahoo.com", "code_wizard@gmail.com", "programmer_x@example.com", "data_scientist@hotmail.com", "cyber_punk@gmail.com", "hacker007@example.com", "digital_nomad@yahoo.com", "robot_overlord@hotmail.com", "pixel_pioneer@gmail.com", "java_junkie@example.com", "code_cruncher@yahoo.com", "byte_buddy@hotmail.com", "code_commander@gmail.com", "binary_scribe@example.com", "web_warrior@yahoo.com", "script_slinger@hotmail.com", "code_crafter@gmail.com", "byte_bandit@example.com" ]
    for user in emails:
        for movie in movies:
            random_rating = round(random.uniform(0.0, 5.0), 1)
            if random.random() < 0.2:
                with app.app_context():
                    addRating(user, movie, random_rating)
    return

def auto_register():
    usernames = [ "user123", "awesome_user", "alpha_beta", "user42", "cool_dude", "coding_ninja", "python_lover", "web_master", "tech_guru", "dev_ops", "geeky_gamer", "creative_coder", "code_wizard", "programmer_x", "data_scientist", "cyber_punk", "hacker007", "digital_nomad", "robot_overlord", "pixel_pioneer", "java_junkie", "code_cruncher", "byte_buddy", "code_commander", "binary_scribe", "web_warrior", "script_slinger", "code_crafter", "byte_bandit" ]
    emails = [ "user123@example.com", "awesome_user@gmail.com", "alpha_beta@yahoo.com", "user42@hotmail.com", "cool_dude@outlook.com", "coding_ninja@gmail.com", "python_lover@example.com", "web_master@yahoo.com", "tech_guru@hotmail.com", "dev_ops@gmail.com", "geeky_gamer@example.com", "creative_coder@yahoo.com", "code_wizard@gmail.com", "programmer_x@example.com", "data_scientist@hotmail.com", "cyber_punk@gmail.com", "hacker007@example.com", "digital_nomad@yahoo.com", "robot_overlord@hotmail.com", "pixel_pioneer@gmail.com", "java_junkie@example.com", "code_cruncher@yahoo.com", "byte_buddy@hotmail.com", "code_commander@gmail.com", "binary_scribe@example.com", "web_warrior@yahoo.com", "script_slinger@hotmail.com", "code_crafter@gmail.com", "byte_bandit@example.com" ]
    password = '123'
    for i,user in enumerate(usernames):
        with app.app_context():
            addUsers(user,emails[i],password)
    return
"""
#when you are logged in these are the sites you can go to
@app.route("/AccessHome")
def accessHome():
    global Login_email
    if Login_email == '':
        flash(f'Please Login')
        return redirect(url_for('login'))
    flash(f'Welcome {Login_email}','success')
    return render_template('accessHome.html', title='Welcome')
new_ratings = False
@app.route("/Rate", methods=['GET', 'POST'])
def rate():
    global Login_email,new_ratings
    if Login_email == '':
        flash(f'Please Login')
        return redirect(url_for('login'))
    movies = moviesList('movies.json')
    form = RatingsForm()
    if form.validate_on_submit and form.title.data != None:
        if form.rating.data < 0.0 or form.rating.data > 5.0:
            flash(f"Please input a value from 0-5!")
            return redirect(url_for('rate'))
        flash(f'Updated you rating of {form.title.data} to {round(form.rating.data,1)}!', 'success')
        new_ratings = True
        movie_name = form.title.data
        user_rating = round(form.rating.data,1)
        addRating(Login_email, movie_name, user_rating)
        movie_ratings  = MovieRating.query.all()
        grouped_data = {}
        for rating in movie_ratings:
            user_id = rating.user_id
            movie = rating.movie
            rating_value = float(rating.rating)
            if user_id not in grouped_data:
                grouped_data[user_id] = []
            grouped_data[user_id].append({'movie': movie, 'rating': rating_value})
        # Write the dictionary to a JSON file
        with open('user_movie_ratings.json', 'w') as json_file:
            json.dump(grouped_data, json_file, indent=4)
    return render_template('rate.html', title='Rate Movies', movies=movies, form=form)

app.config['PER_PAGE'] = 30
def get_items(recommended_dict, offset=0, per_page=None):
    return {k: v for idx, (k, v) in enumerate(recommended_dict.items()) if offset <= idx < offset + per_page}

@app.route("/Recommendations")
def recommendations():
    global Login_email, sim,new_ratings,recommended_list
    movies = moviesList('movies.json')
    if Login_email == '':
        flash(f'Please Login')
        return redirect(url_for('login'))
    if MovieRating.query.filter_by(user_id=Login_email).first():
        flash(f'Here are your recommendations based on what you have rated!','success')
    else:
        flash(f'You have not done any ratings yet, please rate some movies first!','danger')
        return redirect(url_for('rate')) 
    #saved_path = r'C:\Users\kenhy\OneDrive\Desktop\Ryerson_University\cps842\Project\saved'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, '..'))
    saved_path = os.path.join(project_dir, 'saved')
    json_file_path = os.path.join(saved_path, f'{Login_email}.json')
    if new_ratings:
        itemBasedCF()
        new_ratings = False
        recommendation_list = dict(sorted(recommend(movies).items(), key=lambda item: item[1], reverse=True))
        recommended_list = recommendation_list
        
        with open(json_file_path, 'w') as json_file:
            json.dump(recommended_list, json_file, indent=4)
    else:
        try:
            with open(json_file_path, 'r') as json_file:
                recommended_list= json.load(json_file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
        
    page = request.args.get('page', default=1, type=int)
    total = len(recommended_list)

    pagination = Pagination(page=page, total=total, per_page=app.config['PER_PAGE'], css_framework='bootstrap4')

    items = get_items(recommended_list,offset=(page-1) * app.config['PER_PAGE'], per_page=app.config['PER_PAGE'])
    
    
    return render_template('recommendations.html', title='Recommendations',items=items, pagination=pagination)
    
sim = {}
def recommend(movies):
    global Login_email
    recommendation_list = {}
    for movie in movies:
        if MovieRating.query.filter_by(movie=movie,user_id=Login_email).first():
            continue
        else:
            movie_id = Movies.query.filter_by(title=movie).with_entities(Movies.id).first()[0]
            escaped_variable = re.escape(str(movie_id))
            pattern = re.compile(rf',{escaped_variable}$|,{escaped_variable},|^{escaped_variable},|,{escaped_variable}\b')
            #print(f"The not rated movie is id: {escaped_variable}")
            numerator = 0
            denominator = 0
            for sim_score in sim:
                #print(f"Checking sim({sim_score}) ")
                if pattern.search(sim_score):
                    other_movie_id = sim_score.split(',')
                    if int(other_movie_id[0]) == movie_id:
                        other_movie_id = int(other_movie_id[1])
                        #print(f"The rated movie is id: {other_movie_id}")
                    else:
                        other_movie_id = int(other_movie_id[0])
                        #print(f"The rated movie is id: {other_movie_id}")
                    other_movie_query = Movies.query.filter_by(id=other_movie_id).with_entities(Movies.title).first()
                    for movie2 in other_movie_query:
                        other_movie=movie2
                        #print(f"The rated movie title: {other_movie}")
                    if MovieRating.query.filter_by(movie=other_movie,user_id=Login_email).first():
                        user_rating_query = MovieRating.query.filter_by(movie=other_movie,user_id=Login_email).with_entities(MovieRating.rating).first()
                        user_rating = float(user_rating_query[0])
                        #print(f"With a rating of: {user_rating}")
                        numerator += sim[sim_score]*user_rating
                        denominator += sim[sim_score]
            if denominator != 0 and numerator != 0:
                p_rating = numerator/denominator
                recommendation_list[movie] = round(p_rating,1)
                
    return recommendation_list
def itemBasedCF():
    movies = moviesList('movies.json')
    for index, movie in enumerate(movies.keys()):
        if index < len(movies.keys()):
            
            rater_dict = {}
            movie_average, movie_ratings = movieRateList(movie)#stores the movie average
            if movie_average == 0 or movie_ratings == 0:
                continue
            movie_raters = getAllRaters(movie) #stores everyone who rated the movie by email
            for i,rater in enumerate(movie_raters):
                rater_dict[rater] = movie_ratings[i]
            comparedToMovie(index, movies, movie_raters,movie, rater_dict)
    #can keep or remove
    with open('similarity_matrix.json', 'w') as json_file:
        json.dump(sim, json_file, indent=4)
    
    return

def comparedToMovie(index, movies,comparedRaters, comparedMovie, comparedMovieRaterDict):
    global sim
    for i, movie in enumerate(movies.keys()):
        if i > index:
            rater_dict = {}
            movie_average, movie_ratings = movieRateList(movie)#stores the movie average
            if movie_average == 0 or movie_ratings == 0:
                continue
            movie_raters = getAllRaters(movie) #stores everyone who rated the movie by email
            same_raters = getIntersectingRaters(movie_raters,comparedRaters)
            comparedAverage = 0
            thisAverage = 0 
            for i,rater in enumerate(movie_raters):
                rater_dict[rater] = movie_ratings[i]
            for i,rater in enumerate(same_raters):
                comparedAverage+=comparedMovieRaterDict[rater]
                thisAverage += rater_dict[rater]
            if len(same_raters) == 0:
                continue
            comparedAverage /= len(same_raters)
            thisAverage /= len(same_raters)
            numerator = 0
            denom1, denom2 = 0,0
            for r in same_raters:
                numerator += (comparedMovieRaterDict[r]-comparedAverage)*(rater_dict[r]-thisAverage)
                denom1+= (comparedMovieRaterDict[r]-comparedAverage)**2
                denom2+= (rater_dict[r]-thisAverage)**2
            denom1 = math.sqrt(denom1)
            denom2 = math.sqrt(denom2)
            if denom1 == 0 or denom2 == 0:
                continue
            sim_score = numerator/(denom1*denom2)
            if sim_score > 0.7:
                first = Movies.query.filter_by(title=comparedMovie).with_entities(Movies.id).first()
                second = Movies.query.filter_by(title=movie).with_entities(Movies.id).first()
                sim[f'{first[0]},{second[0]}'] = sim_score
    return
def movieRateList(movie_title):#calculates the movie average in the movieRatings db
    user_count = MovieRating.query.filter_by(movie=movie_title).count()
    if user_count == 0:
        return 0,0
    user_ratings = MovieRating.query.filter_by(movie=movie_title).with_entities(MovieRating.rating).order_by(MovieRating.user_id.desc()).all()
    user_Average = round(sum([float(rating[0]) for rating in user_ratings])/user_count,1)
    user_rating = [round(float(rating[0]),1) for rating in user_ratings]
    return user_Average,user_rating
def getAllRaters(movie_title):#gets a list of users who rated the movie
    movie_raters = MovieRating.query.filter_by(movie=movie_title).with_entities(MovieRating.user_id).order_by(MovieRating.user_id.desc()).all()
    list_of_raters = []
    for users in movie_raters:
        list_of_raters.append(users[0])
    return list_of_raters
def getIntersectingRaters(raterList1, raterList2):
    intersection = list(set(raterList1) & set(raterList2))
    return intersection



@app.route("/Search",methods=['GET', 'POST'])
def search():
    global Login_email
    q = request.args.get("q")
    form = RatingsForm()
    if q:
        results = Movies.query.filter(Movies.title.icontains(q) | Movies.director.icontains(q) | Movies.genre.icontains(q)).order_by(Movies.rating.desc()).limit(100).all()
    else:
        results = []
    user_movie_ratings = MovieRating.query.filter_by(user_id=Login_email).all()

    # Create a dictionary of movie:rating pairs
    user_ratings_dict = {rating.movie: float(rating.rating) for rating in user_movie_ratings}
    return render_template('search_results.html',title="Search",results=results,form=form,user_ratings_dict=user_ratings_dict)

def addRating(email, title, rating):
    if MovieRating.query.filter_by(user_id=email, movie=title).first():
        user = MovieRating.query.filter_by(user_id=email, movie=title).first()
        original_user_rating = user.rating
        user.rating = round(rating,1)
        db.session.commit()
        movie_rating = Movies.query.filter_by(title=title).first()
        number_of_ratings = MovieRating.query.filter_by(movie=title).count()
        original_movie_rating = movie_rating.rating*number_of_ratings - original_user_rating
        movie_rating.rating = (original_movie_rating + user.rating)/number_of_ratings
        db.session.commit()
    else:
        rating = round(rating,1)
        new_user = MovieRating(user_id = email, movie=title, rating=rating)
        db.session.add(new_user)
        db.session.commit()
        movie_rating = Movies.query.filter_by(title=title).first()
        number_of_ratings = MovieRating.query.filter_by(movie=title).count()
        original_movie_rating = movie_rating.rating*(number_of_ratings-1)
        movie_rating.rating = round((float(original_movie_rating) + rating)/number_of_ratings,1)
        db.session.commit()
    return
    
def addUsers(username,email,password):
    new_user = User(username = username, email = email, password = password)
    db.session.add(new_user)
    db.session.commit()
    return
def confirmUser(email, password):
    isUser = User.query.filter_by(email=email, password=password).first()
    
    if isUser:
        return [True,isUser.username, isUser.email, isUser.password]
    return False
def moviesList(movie_file):
    with open(movie_file,'r') as file:
        movies = json.load(file)
    return movies
"""
def fillMoviedb():
    movies = moviesList('movies.json')
    for title,details in movies.items():
        genre = details[0]
        rating = details[1]
        director= details[3]
        new_movie = Movies(title=title,genre=genre,rating=rating,director=director)
        db.session.add(new_movie)
        db.session.commit()
    return
"""
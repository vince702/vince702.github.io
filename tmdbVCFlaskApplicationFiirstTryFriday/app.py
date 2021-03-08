from flask import Flask
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)
import requests
from flask import Flask, request, render_template, jsonify
import json




app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "HOME"




@app.route('/trending', methods=['GET'])
def trending():
	trending_url = "https://api.themoviedb.org/3/trending/movie/week?api_key=eddb8596c7eaef5452157ca5768e7fbc"
	response = requests.get(trending_url)
	response = response.json()
	trending =  response["results"][:5]
	trending_top5 = []
	for item in trending:
		item = {'title': item['title'], 'backdrop_path': item['backdrop_path'], 'release_date': item['release_date']}
		trending_top5.append(item)
	return jsonify({'result':trending_top5})


@app.route('/airing', methods=['GET'])
def airing():
	airing_url = "https://api.themoviedb.org/3/tv/airing_today?api_key=eddb8596c7eaef5452157ca5768e7fbc"
	response = requests.get(airing_url)
	response = response.json()
	airing =  response["results"][:5]
	airing_top5 = []
	for item in airing:
		item = {'name': item['name'], 'backdrop_path': item['backdrop_path'], 'first_air_date': item['first_air_date']}
		airing_top5.append(item)
	return jsonify({'result':airing_top5})



#https://api.themoviedb.org/3/search/movie

@app.route('/searchmovies',methods=['GET'])
def search_movies():
    query = ''

    if 'query' in request.args:
        query = request.args['query']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    search_movie_url="https://api.themoviedb.org/3/search/movie?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US&query={q}&page=1&include_adult=false".format(q=query)
    
    response = requests.get(search_movie_url)
    response = response.json()
    results = response["results"][:10]
    results_top10 = []
    for item in results:
    	item = {'id':item['id'],'title':item['title'],'overview':item['overview'],'poster_path':item['poster_path'],'release_date':item['release_date'],'vote_average':item['vote_average'],'vote_count':item['vote_count'],'genre_ids':item['genre_ids']}
    	results_top10.append(item)
    return jsonify({'result':results_top10})


#https://api.themoviedb.org/3/search/tv?api_key=97588ddc4a26e3091152aa0c9a40de22&language=en-US&page=1&query=game%20of&include_adult=false

@app.route('/searchtv',methods=['GET'])
def search_tv():
    query = ''

    if 'query' in request.args:
        query = request.args['query']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    search_movie_url="https://api.themoviedb.org/3/search/tv?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US&page=1&query={q}&include_adult=false".format(q=query)
    
    response = requests.get(search_movie_url)
    response = response.json()
    results = response["results"][:10]
    results_top10 = []
    for item in results:
    	try:
    		item['first_air_date']=item['first_air_date']
    	except:
    		item['first_air_date']=' N/A '
    	item = {'id':item['id'],'name':item['name'],'overview':item['overview'],'poster_path':item['poster_path'],'first_air_date':item['first_air_date'],'vote_average':item['vote_average'],'vote_count':item['vote_count'],'genre_ids':item['genre_ids']}


    	results_top10.append(item)
    return jsonify({'result':results_top10})


#https://api.themoviedb.org/3/search/multi?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US&query=game%20of&page=1&include_adult=false

@app.route('/multisearch', methods=['GET'])
def search_multi():
    query = ''

    if 'query' in request.args:
        query = request.args['query']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')
    search_url = "https://api.themoviedb.org/3/search/multi?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US&query={q}&page=1&include_adult=false".format(q=query)

    response = requests.get(search_url)
    response = response.json()
    results = response["results"]
    #return jsonify(results[1]['media_type'])
    results_moviestv = []
    for item in results:
    	try:
    		if item["media_type"] == "movie":
    			item = {
    			'media_type': 'movie', 'id':item['id'],
    			'title':item['title'],'overview':item['overview'],
    			'poster_path':item['poster_path'],'release_date':item['release_date'],
    			'vote_average':item['vote_average'],'vote_count':item['vote_count'],
    			'genre_ids':item['genre_ids']
    			}
    			results_moviestv.append(item)
    		if item["media_type"] == 'tv':
    			try:
    				item['first_air_date']=item['first_air_date']
    			except:
    				item['first_air_date']=' N/A '

    			item = {
    			'media_type':'tv', 'id':item['id'],'title':item['name'],'overview':item['overview'],
    			'poster_path':item['poster_path'],'release_date':item['first_air_date'],
    			'vote_average':item['vote_average'],'vote_count':item['vote_count'],'genre_ids':item['genre_ids']
    			}
    			results_moviestv.append(item)
    		else:
    			continue
    	except:
      		continue
    results_moviestv = results_moviestv[:10]
    return jsonify({'result':results_moviestv})


@app.route('/moviedetails',methods=['GET'])
def movie_details():
    query = ''

    if 'id' in request.args:
        query = request.args['id']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    search_movie_url="https://api.themoviedb.org/3/movie/{id}?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US".format(id=query)
    
    response = requests.get(search_movie_url)
    item = response.json()

    item = {
    'id':item['id'],
    'title':item['title'],
    'overview':item['overview'],
    'spoken_languages':item['spoken_languages'],
    'poster_path':item['poster_path'],
    'release_date':item['release_date'],
    'vote_average':item['vote_average'],
    'vote_count':item['vote_count'],
    'backdrop_path':item['backdrop_path'], 
    'genres':item['genres']
    }
    
    return jsonify(item)




@app.route('/moviecredits',methods=['GET'])
def movie_credits():
    #API Example:https://api.themoviedb.org/3/movie/284052/credits?api_key=97588ddc4a26e3091152aa0c9a40de22&language=en-US
    query = ''

    if 'id' in request.args:
        query = request.args['id']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    cast_url="https://api.themoviedb.org/3/movie/{id}/credits?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US".format(id=query)
    
    response = requests.get(cast_url)
    response = response.json()
    results = response["cast"]
    #return jsonify(results[1]['media_type'])
    results_cast = []
    for item in results:
        item = {
    		'name': item['name'], 
    		'profile_path':item['profile_path'],
    		'character':item['character']
    		}
        if (item['profile_path']):
                pass
        else:
                item['profile_path'] = "N/A"

        results_cast.append(item)


    results_cast = results_cast[:8]
    return jsonify({'result':results_cast})




@app.route('/moviereviews',methods=['GET'])
def movie_reviews():
    query = ''

    if 'id' in request.args:
        query = request.args['id']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    review_url = "https://api.themoviedb.org/3/movie/{id}/reviews?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US&page=1".format(id=query)

    response = requests.get(review_url)
    response = response.json()
    results = response["results"]
    #return jsonify({'result':results})
    #return jsonify(results[1]['media_type'])
    results_review = []
    for item in results:
    		item = {
    		'username': item['author_details']['username'], 
    		'content':item['content'],
    		'rating':item['author_details']['rating'],
    		 'created_at':item['created_at']
    		 }
    		results_review.append(item)
    if (item['rating']):
        pass
    else:
        item['rating'] = ''
    results_review.append(item)

    results_review = results_review[:5]
    return jsonify({'result':results_review})


@app.route('/tvdetails',methods=['GET'])
def tv_details():
    query = ''

    if 'id' in request.args:
        query = request.args['id']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    search_movie_url="https://api.themoviedb.org/3/tv/{id}?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US".format(id=query)
    
    response = requests.get(search_movie_url)
    item = response.json()

    item = {
    'backdrop_path':item['backdrop_path'],
    'episode_run_time':item['episode_run_time'],
    'first_air_date':item['first_air_date'],
    'genres':item['genres'],
    'id':item['id'],
    'name':item['name'],
    'number_of_seasons':item['number_of_seasons'],
    'overview':item['overview'],
    'poster_path':item['poster_path'],
    'spoken_languages':item['spoken_languages'],
    'vote_average':item['vote_average'],
    'vote_count':item['vote_count'],
    }
    
    return jsonify(item)

@app.route('/tvcredits',methods=['GET'])
def tv_credits():
    #API Example:https://api.themoviedb.org/3/movie/284052/credits?api_key=97588ddc4a26e3091152aa0c9a40de22&language=en-US
    query = ''

    if 'id' in request.args:
        query = request.args['id']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    cast_url="https://api.themoviedb.org/3/tv/{id}/credits?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US".format(id=query)
    
    response = requests.get(cast_url)
    response = response.json()
    results = response["cast"]
    #return jsonify(results[1]['media_type'])
    results_cast = []
    for item in results:
        item = {
    		'name': item['name'], 
    		'profile_path':item['profile_path'],
    		'character':item['character']
    		}
        if (item['profile_path']):
                pass
        else:
                item['profile_path'] = "N/A"
        results_cast.append(item)
        


    results_cast = results_cast[:8]
    return jsonify({'result':results_cast})

@app.route('/tvreviews',methods=['GET'])
def tv_reviews():
    query = ''

    if 'id' in request.args:
        query = request.args['id']
        
    else:
        return jsonify({'result':[]})

    query.replace(' ','%20')

    review_url = "https://api.themoviedb.org/3/tv/{id}/reviews?api_key=eddb8596c7eaef5452157ca5768e7fbc&language=en-US&page=1".format(id=query)

    response = requests.get(review_url)
    response = response.json()
    results = response["results"]
    #return jsonify({'result':results})
    #return jsonify(results[1]['media_type'])
    results_review = []
    for item in results:

        item = {
    		'username': item['author_details']['username'], 
    		'content':item['content'],
    		'rating':item['author_details']['rating'],
    		 'created_at':item['created_at']
    		}
        if (item['rating']):
            pass
        else:
            item['rating'] = ''

        results_review.append(item)

    results_review = results_review[:5]
    return jsonify({'result':results_review})









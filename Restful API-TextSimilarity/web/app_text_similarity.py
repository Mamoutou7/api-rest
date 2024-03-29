from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient
import bcrypt
import spacy

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):
	if users.find({"Username":username}).count() == 0 :
		return False
	else:
		return True


class Register(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]


		if UserExist(username):
			retJON ={
				"status": 301,
				"msg": "Invalid Username"
			}
			return jsonify(retJON)

		hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		users.insert({
			"Username": username,
			"Password": hashed_pw,
			"Tokens": 6
			})
		retJON = {
			"status": 200,
			"msg": "You've successful signed up to the API"
		}

		return jsonify(retJON)



def verifyPw(username, password):
	if not UserExist(username):
		return False 

	hashed_pw = users.find({
		"Username":username
		})[0]["Password"]
	if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
		return True
	else:
		return False

def countTokens(username):
	tokens = users.find({
		"Username":username
	})[0]["Tokens"]
	return tokens


class Detect(Resource):
	def post(self):

		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]
		text1 = postedData["text1"]
		text2 = postedData["text2"] 

		if not UserExist(username):
			retJON = {
				"status": 301,
				"msg": "Invalid Username"
			}
		
		correct_pw = verifyPw(username, password)

		if not correct_pw:
			retJON = {
				"status": 302,
				"msg": "Invalid Password"
			}
		num_tokens = countTokens(username)

		if num_tokens <= 0:
			retJON = {
				"status": 303,
				"msg": "You're out of tokens, please refill!"
			}
			return jsonify(retJON)


		# Calculate the edit disance 
		text1 = nlp(text1)
		text2 = nlp(text2)

		ratio =  text1.similarity(text2)

		retJON = {
			"status":200,
			"similarity": ratio,
			"msg": "Similarity score calculated successfully"
		}
		current_tokens = countTokens(username)

		users.update({
			"Username":username
			}, {
			"$set":{
			"Tokens": current_tokens-1
			}
		})

		return jsonify(retJON)


class Refill(Resource):
	def post(self):

		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]

		refill_amont = postedData["refill"]

		if not UserExist(username):
			retJON = {
				"status": 301,
				"msg": "Invalid Username"
			}
			return jsonify(retJON)

		correct_pw = "abc123"

		if not password == correct_pw:
			retJON = {
				"status": 304,
				"msg": "Invalid Admin Password"
			}
			return jsonify(retJON)

		users.update({
			"Username":username
			}, {
			"$set":{
			"Tokens": refill_amont
			}
		})
		retJON = {
			"status":200,
			"msg": "Reffill successfully"
		}
		return jsonify(retJON)




api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')



if __name__ == '__main__':
		app.run(host='0.0.0.0')	















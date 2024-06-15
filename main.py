from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.hashing import Hash
from fastapi import FastAPI, HTTPException, Depends, Request,status
from auth.oauth import get_current_user
from auth.jwttoken import create_access_token
from fastapi.middleware.cors import CORSMiddleware
from database.models import User,Questions
from bson.objectid import ObjectId
from config import collection_user,collection
from typing import Optional
from llm import llm



app=FastAPI()




#------------------------------------------------------------------Authentication---------------------------------------------------------------------------

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(current_user:User = Depends(get_current_user)):
	return {"data":"Hello OWrld",'user':current_user}



@app.post('/users')
def create_user(request:User):
	try:
		hashed_pass = Hash.bcrypt(request.password)
		user_object = dict(request)
		user = collection_user.find_one({"username":user_object['username']})
		if user:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = f'Username Alreday Exists')
		user_object["password"] = hashed_pass
		user = collection_user.insert_one(user_object)
		print(user)
		return {"res":"created"}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))


@app.post('/auth/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
	try:

		user = collection_user.find_one({"username":request.username})
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
		if not Hash.verify(user["password"],request.password):
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
		access_token = create_access_token(data={"sub": user["username"] })
		return {"access_token": access_token, "token_type": "bearer"}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))



#---------------------------------------------------------------------Blog Posts--------------------------------------------------------------------------------

@app.get('/users/{user_id}')
def get_user(user_id:str,current_user:User = Depends(get_current_user)):
	try:
		user = collection_user.find_one({"username":user_id})
		print(user)
		return {"res":helper(user)}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))

def helper(data) -> dict:
	return {
	"id": str(data["_id"]),
	"username": data["username"]
	}

@app.post('/questions')
def post_answer(request:Questions,current_user:User = Depends(get_current_user)):
	try:
		ques_obj=dict(request)
		ans=llm.get_answer(ques_obj['title'])
		user = collection_user.find_one({"username":current_user.username})
		ques_obj['ans']=ans
		ques_obj['user_id']=user['_id']
		obj=collection.insert_one(ques_obj)
		return {"res":ans}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))
	

@app.get('/questions/{question_id}')
def get_question(question_id:str,current_user:User = Depends(get_current_user)):
	try:
		id= ObjectId(question_id)
		ques = collection.find_one({"_id":id})
		print(ques)
		return {"res":queshelper(ques)}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))
	

@app.get('/users/{user_id}/questions')
def get_specific_user_question(user_id:str,current_user:User = Depends(get_current_user)):
	try:
		question = collection.find({"user_id":user_id})
		lst=[]
		for ques in question:
			print(ques)
			lst.append(helper(ques))
		return {"res":lst}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))



def helper(data) -> dict:
	return {
	"id": str(data["_id"]),
	"username": data["username"]
	}

def queshelper(data)->dict:
	return{
		"id":str(data['_id']),
		'question':data['title'],
		'answer':data['ans'],
		'user_id':str(data['_id'])
	}
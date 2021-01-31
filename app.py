from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
#connect the webapp to the database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://dust:liu147che@localhost:5432/createUser'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#creater the model for the user with ID, firstName and lastName, first and last name can not be null and can be duplicate, ID is unique
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(), nullable = False)
    lastName =db.Column(db.String(), nullable = False)
   
    #for sql to test the what the model contain
    def __repr__(self):
        return f'<user {self.id} {self.firstName} {self.lastName}>'

#create the model
db.create_all()

#deal with the create actionand get the data from front end, the method must be POST
@app.route('/user/create',methods=['POST'])
def create_user():  
    error = False  #Initial the error flag to flase
    body ={}  # the variable use to store the data and transfer back to front end
    try:
        firstName = request.get_json()['firstName']
        lastName = request.get_json()['lastName']

        #store the data in the database
        user = User(firstName=firstName,lastName=lastName) 
        db.session.add(user)
        db.session.commit()

        #data back to front end
        body['firstName'] =user.firstName
        body['lastName'] =user.lastName
        body['id']=user.id

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close() 
    if not error:
        #if no error, send data
        return jsonify(body)


@app.route('/')
def index():
    return render_template('index.html')


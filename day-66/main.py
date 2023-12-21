import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route('/random')
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    print(random_cafe)
    # return f"<h3> Random cafe is: {random_cafe.name} </h3>"
    return jsonify(cafe={"id": random_cafe.id,
                         "name": random_cafe.name,
                         "map_url": random_cafe.map_url,
                         "img_url": random_cafe.img_url,
                         "location": random_cafe.location,
                         "seats": random_cafe.seats,
                         "has_toilet": random_cafe.has_toilet,
                         "has_wifi": random_cafe.has_wifi,
                         "has_sockets": random_cafe.has_sockets,
                         "can_take_calls": random_cafe.can_take_calls,
                         "coffee_price": random_cafe.coffee_price}
                   )


@app.route('/all')
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafes = []
    for cafe in all_cafes:
        cafes.append(cafe.to_dict())

    cafes_json = dict()
    cafes_json['cafes'] = cafes
    print(cafes_json)
    return jsonify(cafes_json)


@app.route('/search')
def search_cafes():
    location = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    all_cafes = result.scalars().all()

    if len(all_cafes) == 0:
        return jsonify(error="Data not found"), 404
    else:
        return jsonify(cafes=[x.to_dict() for x in all_cafes])


## HTTP POST - Create Record
@app.route("/suggest", methods=['POST'])
def add_cafe():
    try:
        new_cafe = Cafe(
            name=request.args.get("name"),
            map_url=request.args.get("map_url"),
            img_url=request.args.get("img_url"),
            location=request.args.get("location"),
            seats=request.args.get("seats"),
            has_toilet=bool(request.args.get("has_toilet")),
            has_wifi=bool(request.args.get("has_wifi")),
            has_sockets=bool(request.args.get("has_sockets")),
            can_take_calls=bool(request.args.get("can_take_calls")),
            coffee_price=request.args.get("coffee_price")
        )

        db.session.add(new_cafe)
        db.session.commit()

        return jsonify(response={"success": "New cafe added"})
    except:
        return jsonify(response={"error": "There was a problem with the request"})


## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:id>', methods=['PATCH'])
def update_price(id):

    cafe = db.get_or_404(Cafe, id)
    print(type(cafe))

    if cafe:
        cafe.coffee_price = request.args.get('price')
        db.session.commit()
        return jsonify(cafe=cafe.to_dict()), 200

    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 405


## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == 'TopSecretAPIKey':
        cafe = db.get_or_404(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe"}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 405
    else:
        return jsonify(error={"Not Found": "Sorry the api key provided didn't match"}), 403
    return ('api_key')


if __name__ == '__main__':
    app.run(debug=True)

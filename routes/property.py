from flask import Blueprint, request, jsonify, g, json
from middleware.auth import authenticate
property_bp = Blueprint("property", __name__)


@property_bp.route("/property/addProperty", methods=["POST"])
@authenticate
def post_property():
    try:
        user_id = g.user['user_id']
        from app import mysql
        propertyData = request.json
        host_id = user_id
        property_name = propertyData["property_name"]
        type = propertyData["type"]
        city = propertyData["city"]
        state = propertyData["state"]
        country = propertyData["country"]
        no_of_guests = propertyData["no_of_guests"]
        bedrooms = propertyData["bedrooms"]
        beds = propertyData["beds"]
        bathrooms = propertyData["bathrooms"]
        description = propertyData["description"]
        image = propertyData["image"]
        price = propertyData["price"]
        print(image)

        # Execute SQL query to insert property data into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO property (host_id, property_name, type, city, state, country, no_of_guests, bedrooms, beds, bathrooms, description, image, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (host_id, property_name, type, city, state, country, no_of_guests, bedrooms, beds, bathrooms, description, json.dumps(image), price))
        mysql.connection.commit()
        cur.close()
        return 'property added successfully'
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error', 500


@property_bp.route("/property")
def get_allProperties():
    try:
        from app import mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM property")
        properties = cur.fetchall()
        cur.close()

        propertyData = []
        for property in properties:
            each_property = {
                'property_id': property[0],
                "host_id": property[1],
                "property_name": property[2],
                "type": property[3],
                "city": property[4],
                "state": property[5],
                "country": property[6],
                "no_of_guests": property[7],
                "bedrooms": property[8],
                "beds": property[9],
                "bathrooms": property[10],
                "description": property[11],
                "image": property[12],
                "price": property[13]
            }
            propertyData.append(each_property)
        return jsonify(propertyData)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error', 500


# getting host properties by id
@property_bp.route("/property/host/<host_id>")
def hostProp(host_id):
    try:
        from app import mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM property WHERE host_id=%s", (host_id,))
        properties = cur.fetchall()
        cur.close()
        
        propertyData = []
        for property in properties:
            each_property = {
                'property_id': property[0],
                "host_id": property[1],
                "property_name": property[2],
                "type": property[3],
                "city": property[4],
                "state": property[5],
                "country": property[6],
                "no_of_guests": property[7],
                "bedrooms": property[8],
                "beds": property[9],
                "bathrooms": property[10],
                "description": property[11],
                "image": property[12],
                "price": property[13]
            }
            propertyData.append(each_property)
        return jsonify(propertyData)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error', 500


# {
#     "property_name":"Adorable treehouse with common swimming pool",
#     "type":"tropical",
#     "city":"Curtorim",
#     "state":"Goa",
#     "country":"India",
#     "no_of_guests":2,
#     "bedrooms":1,
#     "beds":1,
#     "bathrooms":1,
#     "description":"",
#     "image":[""],
#     "price":
# }

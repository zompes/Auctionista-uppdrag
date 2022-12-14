# Create Environment
# pip install flask
# pip install pymysql
# pip install flask-mysql

from flask import Flask, jsonify, request, session
import pymysql
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

# connect database
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'zomps'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fsinqt12'
app.config['MYSQL_DATABASE_DB'] = 'auctionista_webb_api'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


# login
@app.route("/api/login", methods=["POST"])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM konto WHERE email = %s AND lossenord = %s"
        bind = (request.json['email'], request.json['lossenord'])
        cursor.execute(query, bind)
        user = cursor.fetchone()        
        if user['email']:
            session['user'] = user
            print(session.get("user"))
            return jsonify({"login": True})
    except Exception as e:
        return jsonify({"login": False})
    finally:
        cursor.close()
        conn.close()



# check if logged in
@app.route("/api/login", methods=["GET"])
def check_session():
    if session.get('user'):
        return jsonify({"login": True})

    return jsonify({"login": False})


# logout
@app.route("/api/login", methods=["DELETE"])
def logout():
    session['user'] = {}
    return jsonify({"logout": True})


# get current user
@app.route("/api/user", methods=["GET"])
def user_data():
    if session.get('user'):
        return jsonify(session['user'])

    return jsonify({"login": False})

# 1
@app.route("/api/auktionslista", methods=["GET"])
def auktionlista():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM auktionslista"
        cursor.execute(query)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

# 2
@app.route("/api/auktionsobjekts/<id>", methods=["GET"])
def objektdetalj(id: int):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT titel, beskrivning, starttid, sluttid, bild, saljare, bud, tidpunkt FROM auktionsobjekts, bud WHERE auktionsobjekts.id = %s ORDER BY tidpunkt DESC LIMIT 1"
        bind = (id)
        cursor.execute(query, bind)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

# 3
@app.route("/api/konto", methods=["POST"])
def skapa_konto():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "INSERT INTO konto SET fornamn = %s, efternamn = %s, email = %s, lossenord = %s"
        bind = (request.json["fornamn"], request.json["efternamn"], request.json["email"], request.json["lossenord"])
        cursor.execute(query, bind)
        conn.commit()
        response = jsonify({"Skapad konto": cursor.lastrowid})
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# 5
@app.route("/api/auktionsobjekts", methods=["POST"])
def skapa_objekt():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if session.get("user"):
        try:
            query = "INSERT INTO auktionsobjekts SET titel = %s, beskrivning = %s, starttid = %s, sluttid = %s, bild = %s, saljare = %s"
            bind = (request.json["titel"], request.json["beskrivning"], 
            request.json["starttid"], request.json["sluttid"], 
            request.json["bild"],session.get("user")["id"])
            cursor.execute(query, bind)
            conn.commit()
            response = jsonify({"Skapad objekt": cursor.lastrowid})
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
            return "error"
        finally:
                cursor.close()
                conn.close()

# 7
@app.route("/api/auktionsobjekts/bud", methods=["GET"])
def get_auction_bid():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT auktionsobjekts.titel, MAX(bud.bud) AS bud
        FROM auktionsobjekts
        JOIN bud
        ON auktionsobjekts.id = bud.auktionobjekt
        GROUP BY auktionsobjekts.titel;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

# 8
# Visar dem senaste 5 buden p?? ett specifikt auktionsobjekt som anv??ndaren matar in
@app.route("/api/auktionsobjekts/<id>", methods=["GET"])
def fem_senaste_buden(id : str):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Query fungerar korrekt i Beekeeper men inte h??r, vet inte varf??r.
        # Jag tror att efter %s i query:en s?? g??r programmet tills n??sta del och
        # ignorerar resten av query:en.
        query = """
        SELECT tidpunkt, bud, titel, auktionsobjekts.beskrivning, 
        starttid, sluttid, bild, saljare 
        FROM auktionsobjekts, bud 
        WHERE auktionsobjekts.id = %s AND bud.auktionobjekt = auktionsobjekts.id
        ORDER BY tidpunkt DESC 
        LIMIT 5"""
        bind = (id)
        cursor.execute(query, bind)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
 
# Visar dem 5 senaste lagda buden, bryr sig inte om auktionsobjekt utan bara
# tiden buden lades. Sorteras efter tidpunkt kulumen i bud tabellen.
@app.route("/api/fem_senaste_lagda_bud", methods=["GET"])
def fem_senaste_lagda_bud():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM fem_senaste_lagda_bud"
        cursor.execute(query)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

# 9, 10
@app.route("/api/auktionsobjekts/<auktionsobjekts_id>/bud", methods=["POST"])
def bud(auktionsobjekts_id : str):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if session.get("user"):
        try:
            query = "SELECT saljare FROM auktionsobjekts WHERE id = %s"
            bind = request.json["auktionsobjekts_id"]
            cursor.execute(query, bind)
            saljare = cursor.fetchone()
            if saljare is not session.get('user'):
                query = "INSERT INTO bud SET bud = %s"
                bind = (request.json["bud"])
                cursor.execute(query, bind)
                conn.commit()
                response = jsonify({"Budets har lagts" : cursor.lastrowid})
                response._status_code = 200
                return response
            else:
                return print("Du kan inte buda p?? ditt eget objekt")
        except Exception as e:
            print(e)
            return "error"
        finally:
                cursor.close()
                conn.close()     

@app.route("/api/auktionsobjekts/<id>/bud", methods=["POST"])
def post_bid(id: int):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(session.get("user"))
    if session.get("user"):
        try:
            query = "select saljare from auktionsobjekts where id = %s"
            bind = (id)
            cursor.execute(query, bind)
            saljare = cursor.fetchone()
            print(saljare)
            print(session.get("user"))
            # Nr. 10
            if saljare is not session.get("user"):
                query = "INSERT INTO bud SET bud = %s, konto = %s, auktionsobjekt = %s"
                bind = (request.json["bud"], session.get("user")["id"], id)
                cursor.execute(query, bind)
                conn.commit()
                response = jsonify({"Budets har lagts": cursor.lastrowid})
                response._status_code = 200
                return response
            else:
                return jsonify("Du kan inte buda p?? ditt eget objekt")
        except Exception as e:
            print(e)
            return jsonify("error")
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify("Logga in")

# this route should only work if logged in
@app.route("/api/protected-data", methods=["GET"])
def protected_data():
    if session.get('user'):
        return jsonify({"get-this-data": "Only if logged in"})

    return jsonify({"login": False})


# this route should work even if you are not logged in
@app.route("/api/unprotected-data", methods=["GET"])
def unprotected_data():
    return jsonify({"get-this-data": "Even if you are logged out"})


if __name__ == "__main__":
    app.run(port=5001, debug=True, load_dotenv=True)

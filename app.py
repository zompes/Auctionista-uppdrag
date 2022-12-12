
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
        query = "SELECT titel, beskrivning, starttid, sluttid, bild, saljare, bud, tidpunkt FROM auktionsobjekts, bud where auktionsobjekts.id = %s;"
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

# 8

# 9

# 10
@app.route("/api/<auktionsobjekts_id>", methods=["POST"])
def stoppa_bud_po_eget_objekt():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if session.get("user"):
        try:
            query = "select saljare from auktionsobjekts where id = %s"
            bind = (request.json["auktionsobjekts_id"])
            cursor.execute(query,bind)
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
                return print("Du kan inte buda på ditt eget objekt")
        except Exception as e:
            print(e)
            return "error"
        finally:
                cursor.close()
                conn.close()        

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

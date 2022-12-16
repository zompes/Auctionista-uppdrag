Denna fil kommer förklara användingen av min API, instruktioner kan det kallas också.

Hur man skapar ett konto:
http://127.0.0.1:5001/api/konto
syntax:
{
    "fornamn": "",
    "efternamn": "",
    "email": "",
    "lossenord" : ""
}

Hur man loggar in:
http://127.0.0.1:5001/api/login
syntax:
{
    "email": "",
    "lossenord" : ""
}

Hur man checkar om man är inloggad:
http://127.0.0.1:5001/api/login
Har ingen syntax



Hur man skapar ett objekt:
http://127.0.0.1:5001/api/auktionsobjekts
syntax:
{
    "titel": "",
    "beskrivning": "",
    "starttid": "",
    "sluttid" : "",
    "bild" : ""
}
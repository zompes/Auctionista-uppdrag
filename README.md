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
Har ingen syntax.

Hur man får alla objekt som har ett bud, du får det senaste budet på objektet:
http://localhost:5001/api/auktionsobjekts/bud
Är en "GET", ingen syntax behövs.

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

Hur man får dem senaste 5 buden på ett objekt du själv matar in:
http://127.0.0.1:5001/api/auktionsobjekts/<id>
Hur den används är att ändra <id> till en siffra som tillhör ett objekt i
auktionsobjekts tabellen.
Exempel: http://127.0.0.1:5001/api/auktionsobjekts/<3> ger dig dem 5 senaste
buden på skor.

Hur man får dem 5 senaste buden, bryr sig bara om när dem kom ut:
http://localhost:5001/api/fem_senaste_lagda_bud
Listan sorteras efter tidpunkt kolumen i bud tabellen.

Hur man lägger till ett bud:
http://localhost:5001/api/auktionsobjekt/<id>/bud
syntax:
{
    "bud" : bud nummer
}
För tillfället fungerar inte denna funktionen, något med att inloggningen
med ett konto blir "None" i funktionen. Händer endast i denna.

Hur man loggar ut:
http://127.0.0.1:5001/api/login
Finns ingen syntax med metoden är en DELETE så kolla att den är på DELETE och inte något annat.
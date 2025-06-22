from flask import Flask, request, send_from_directory, jsonify, render_template, redirect, url_for
import os

app = Flask(__name__) #Erstellt Server
ordner_liste = [] #Liste der Ordner die schon existieren

@app.route('/') #Ist Startseite und sorgt, dass man die Startseite mit / ansprechen kann
def index():
    return render_template('index.html', ordner=ordner_liste)



@app.route('/ordner-anlegen', methods=['POST']) #Dass die Webseite unter /ordner-anlegen diese Funktion findet
def ordnerAnlegen():
    ordnername = request.form.get("Ordnername")
    übergeordneter_pfad = 

    pfad = f"/{ordnername}"
    if ordnername in ordner_liste:      #Prüft ob Ordner schon existiert
        return 'Ordner existiert schon', 300 #Fehlermeldung
    else:
        ordner_liste.append({"name": ordnername, "pfad": pfad}) #Fügt den Ordner der Liste hinzu
    return redirect(url_for("index")) #Lädt Startseite neu






if __name__ == '__main__':  #Wird bei Start asugeführt
    app.run(debug=True)
from flask import Flask, request, send_from_directory, jsonify, render_template, redirect, url_for
import shutil
import os

app = Flask(__name__) #Erstellt Server
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')



def ordner_aus_dateisystem(pfad_relativ):
    ordner = []
    pfad_absolut = os.path.join(UPLOAD_FOLDER, pfad_relativ)

    if os.path.isdir(pfad_absolut):
        for eintrag in os.listdir(pfad_absolut):
            vollpfad = os.path.join(pfad_absolut, eintrag)
            if os.path.isdir(vollpfad):
                ordner.append({
                    "name": eintrag,
                    "pfad": os.path.join(pfad_relativ, eintrag).replace("\\", "/")
                })
    return ordner

def dateien_aus_dateisystem(pfad_relativ):
    dateien = []
    pfad_absolut = os.path.join(UPLOAD_FOLDER, pfad_relativ)

    if os.path.isdir(pfad_absolut):
        for eintrag in os.listdir(pfad_absolut):
            vollpfad = os.path.join(pfad_absolut, eintrag)
            if os.path.isfile(vollpfad):
                dateien.append({
                    "name": eintrag,
                    "pfad": os.path.join(pfad_relativ, eintrag).replace("\\", "/")
                })
    return dateien

@app.route('/') #Ist Startseite und sorgt, dass man die Startseite mit / ansprechen kann
def index():
    aktueller_pfad = request.args.get("pfad", "").strip("/")
    sichtbarer_ordner = ordner_aus_dateisystem(aktueller_pfad)
    sichtbare_dateien = dateien_aus_dateisystem(aktueller_pfad)
    zurück_pfad = os.path.dirname(aktueller_pfad) if aktueller_pfad else ""

    return render_template(
        'index.html',
        ordner=sichtbarer_ordner,
        dateien=sichtbare_dateien, 
        aktueller_pfad=aktueller_pfad,
        zurück_pfad=zurück_pfad
    )


@app.route('/ordner-anlegen', methods=['POST']) #Dass die Webseite unter /ordner-anlegen diese Funktion findet
def ordnerAnlegen():
    ordnerstruktur = request.form.get("Ordnerstruktur").strip("/")
    aktueller_pfad = request.form.get("Pfad").strip("/") or ""



    teile = ordnerstruktur.split('/')
    pfad_bisher = aktueller_pfad

    for teil in teile:
        pfad_bisher = os.path.join(pfad_bisher, teil)
        pfad_absolut = os.path.join(UPLOAD_FOLDER, pfad_bisher)

        if not os.path.exists(pfad_absolut):
            os.makedirs(pfad_absolut, exist_ok=True)

    return redirect(url_for("index", pfad=aktueller_pfad))


@app.route('/upload', methods=['POST'])
def uploadDatei():
    datei = request.files.get("datei")
    aktueller_pfad = request.form.get("Pfad").strip("/") or ""

    neuer_dateiname = request.form.get("neuer_dateiname").strip("/")

    pfad = request.form.get("Pfad")
    alter_name = os.path.basename(pfad)
    _, endung = os.path.splitext(alter_name)


    if not neuer_dateiname:
        if datei and aktueller_pfad:
            zielpfad = os.path.join(UPLOAD_FOLDER, aktueller_pfad)
            os.makedirs(zielpfad, exist_ok=True)
            datei.save(os.path.join(zielpfad, datei.filename))
            return jsonify({"status": "ok"}), 200
    elif neuer_dateiname and aktueller_pfad and datei:
            zielpfad = os.path.join(UPLOAD_FOLDER, aktueller_pfad)
            neuer_dateiname = os.path.join(neuer_dateiname, endung)
            os.makedirs(zielpfad, exist_ok=True)
            datei.save(os.path.join(zielpfad, neuer_dateiname))
            return jsonify({"status": "ok"}), 200
    
    

@app.route('/delete', methods=['POST'])
def delete():
    aktueller_pfad = request.form.get("Pfad")
    zielpfad = os.path.join(UPLOAD_FOLDER, aktueller_pfad)

    if os.path.isdir(zielpfad):
        shutil.rmtree(zielpfad)
        zurück = os.path.dirname(aktueller_pfad)
        return redirect((url_for("index", pfad=zurück)))
    elif os.path.isfile(zielpfad):
        os.remove(zielpfad)
        return redirect((url_for("index", pfad=aktueller_pfad)))
    
@app.route('/download')
def download_file():
    pfad =  request.args.get("pfad")
    if not pfad:
        return "Kein Pfad angegeben", 400
    
    ordner = os.path.join(UPLOAD_FOLDER, os.path.dirname(pfad))
    dateiname = os.path.basename(pfad)

    return send_from_directory(ordner, dateiname, as_attachment=True)    

@app.route('/umbenennen', methods=['POST'])
def rename_file():
    neuer_name = request.form.get("neuer_name") #Dateiname

    pfad_relativ = request.form.get("Pfad", "").strip("/")
    ordner_relativ = os.path.dirname(pfad_relativ)
    dateien = dateien_aus_dateisystem(ordner_relativ)
    namen = [d["name"] for d in dateien]

    if not neuer_name:
        return "Kein Dateiname gegeben", 400
    
    pfad = request.form.get("Pfad")
    alter_name = os.path.basename(pfad)
    _, endung = os.path.splitext(alter_name)

    if neuer_name+endung in namen:
        return "Datei mit demselben Namen existiert schon", 400


    aktueller_pfad = os.path.join(UPLOAD_FOLDER, pfad)

    eltern_pfad = os.path.dirname(aktueller_pfad)
    neuer_pfad = os.path.join(eltern_pfad, neuer_name)
    if endung not in neuer_pfad:
        neuer_pfad = neuer_pfad + endung



    os.rename(aktueller_pfad, neuer_pfad)

    return redirect((url_for("index", pfad=eltern_pfad)))
    

if __name__ == '__main__':  #Wird bei Start asugeführt
    app.run(host="0.0.0.0", debug=True)






#            <td>
#                <form action="/delete" method="post">
#                   <input type="hidden" name="Pfad" value="{{ eintrag['pfad'] }}">
#                    <button class="btn btn-sm btn-danger">🗑️</button>
#                </form>
#            </td>
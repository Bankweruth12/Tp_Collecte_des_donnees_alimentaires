from flask import Flask, render_template, request # pyright: ignore[reportMissingImports]
from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]
import os

app = Flask(__name__)
# Configuration de la base de données
base_dir = os.path.dirname(os.path.abspath("file"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Création de la table dans la base de données
class Repas(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    date_repas = db.Column(db.String(20), nullable=False)
    heure_repas = db.Column(db.String(10), nullable=False)
    type_repas = db.Column(db.String(50), nullable=False)
    aliments = db.Column(db.Text, nullable=False)
    quantite = db.Column(db.String(20), nullable=False)
    lieu = db.Column(db.String(50), nullable=False)
    niveau_faim = db.Column(db.Integer, nullable=False)
    niveau_satisfaction = db.Column(db.Integer, nullable=False)

    def repr(self):
        return f'<Repas {self.id}>'

# Page d'accueil avec le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# Page pour recevoir les données du formulaire
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        new_repas = Repas(
            date_repas = request.form['date'],
            heure_repas = request.form['heure'],
            type_repas = request.form['type_repas'],
            aliments = request.form['aliments'],
            quantite = request.form['quantite'],
            lieu = request.form['lieu'],
            niveau_faim = request.form['niveau_faim'],
            niveau_satisfaction = request.form['niveau_satisfaction']
        )
        try:
            db.session.add(new_repas)
            db.session.commit()
            
            # Récupération des données pour l'affichage
            tous_les_repas = Repas.query.all()
            total = len(tous_les_repas)
            types = {}
            lieux = {}
            faim_moyenne = 0
            satisfaction_moyenne = 0

            if total > 0:
                for r in tous_les_repas:
                    types[r.type_repas] = types.get(r.type_repas, 0) + 1
                    lieux[r.lieu] = lieux.get(r.lieu, 0) + 1
                    faim_moyenne += r.niveau_faim
                    satisfaction_moyenne += r.niveau_satisfaction

                faim_moyenne = round(faim_moyenne / total, 1)
                satisfaction_moyenne = round(satisfaction_moyenne / total, 1)

            # ------------------- CODE DE L'INTELLIGENCE ARTIFICIELLE -------------------
            analyse_ia = ""
            suggestions = []

            if total > 0:
                if faim_moyenne >= 4:
                    analyse_ia = "Vous semblez avoir une très bonne appétit et vous mangez bien."
                    suggestions.append("✅ Continuez comme ça, vos repas sont bien consistants.")
                elif faim_moyenne <= 2:
                    analyse_ia = "Votre niveau de faim est assez bas."
                    suggestions.append("💡 Essayez de prendre des repas plus légers mais plus réguliers.")
                else:
                    analyse_ia = "Votre appétit est dans la moyenne, c'est parfait."

                if satisfaction_moyenne <= 3:
                    analyse_ia += " Par contre, vous n'êtes pas totalement satisfait de vos repas."
                    suggestions.append("😋 N'hésitez pas à tester de nouvelles recettes pour plus de plaisir.")

                if 'Dîner' in types and types['Dîner'] > 2:
                    suggestions.append("⏰ Attention, vous dînez souvent. Essayez de dîner plus tôt.")
                
                if 'Petit-déjeuner' not in types:
                    suggestions.append("☀️ N'oubliez pas le petit-déjeuner, c'est important !")
            # ---------------------------------------------------------------------------

            return render_template('results.html', 
                                   message="Données enregistrées avec succès !",
                                   total=total, 
                                   types=types, 
                                   lieux=lieux, 
                                   faim=faim_moyenne, 
                                   satisfaction=satisfaction_moyenne,
                                   analyse_ia=analyse_ia,
                                   suggestions=suggestions)
        except Exception as e:
            return f"Erreur : {e}"
        
# Page des statistiques
@app.route('/resultats')
def resultats():
    # Récupérer toutes les données
    tous_les_repas = Repas.query.all()
    total = len(tous_les_repas)

    # Compter par type de repas
    types = {}
    lieux = {}
    faim_moyenne = 0
    satisfaction_moyenne = 0

    if total > 0:
        for r in tous_les_repas:
            types[r.type_repas] = types.get(r.type_repas, 0) + 1
            lieux[r.lieu] = lieux.get(r.lieu, 0) + 1
            faim_moyenne += r.niveau_faim
            satisfaction_moyenne += r.niveau_satisfaction

        faim_moyenne = round(faim_moyenne / total, 1)
        satisfaction_moyenne = round(satisfaction_moyenne / total, 1)

    # ------------------- CODE DE L'INTELLIGENCE ARTIFICIELLE -------------------
    analyse_ia = ""
    suggestions = []

    if total > 0:
        if faim_moyenne >= 4:
            analyse_ia = "Vous semblez avoir une très bonne appétit et vous mangez bien."
            suggestions.append("✅ Continuez comme ça, vos repas sont bien consistants.")
        elif faim_moyenne <= 2:
            analyse_ia = "Votre niveau de faim est assez bas."
            suggestions.append("💡 Essayez de prendre des repas plus légers mais plus réguliers.")
        else:
            analyse_ia = "Votre appétit est dans la moyenne, c'est parfait."

        if satisfaction_moyenne < 3:
            analyse_ia += " Par contre, vous n'êtes pas totalement satisfait de vos repas."
            suggestions.append("😋 N'hésitez pas à tester de nouvelles recettes pour plus de plaisir.")

        if 'Dîner' in types and types['Dîner'] > 2:
            suggestions.append("⏰ Attention, vous dînez souvent. Essayez de dîner plus tôt.")
        
        if 'Petit-déjeuner' not in types:
            suggestions.append("☀️ N'oubliez pas le petit-déjeuner, c'est important !")
    # ---------------------------------------------------------------------------

    return render_template('results.html', 
                           total=total, 
                           types=types, 
                           lieux=lieux, 
                           faim=faim_moyenne, 
                           satisfaction=satisfaction_moyenne,
                           analyse_ia=analyse_ia,
                           suggestions=suggestions)

# Créer la base de données si elle n'existe pas
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
app.run(host='0.0.0.0' , port=8501, debug=True)
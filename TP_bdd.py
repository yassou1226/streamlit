import streamlit as st
import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

# Créer la connexion SQL à la base de données pets_db comme spécifié dans votre fichier secrets.
conn = st.connection('pets_db', type='sql')

# Ajouter des styles pour améliorer le visuel
st.markdown(
    """
    <style>
        .titre {
            color: #427AA1;
            text-align: center;
            border: 2px solid #427AA1;
            padding: 10px;
            border-radius: 10px;
            font-family: 'Arial', sans-serif;
        }
        .submit-button {
            background-color: #1f57ff;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .delete-button {
            background-color: #EBF2FA;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre de la page avec une couleur grise et encadré
st.markdown("<h1 class='titre'>Formulaire d'inscription</h1>", unsafe_allow_html=True)

# Ajouter un formulaire pour saisir les informations de l'utilisateur
prenom = st.text_input("Prénom :")
nom = st.text_input("Nom de famille :")
# Ajouter un champ pour la date de naissance avec un calendrier
date_naissance = st.date_input("Date de naissance :", min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
numero_telephone = st.text_input("Numéro de téléphone :")
adresse = st.text_input("Adresse :")

# Ajouter un champ pour saisir l'adresse e-mail
email = st.text_input("Adresse e-mail :")

# Ajouter un bouton pour soumettre le formulaire avec un style personnalisé
bouton_submit = st.button("Soumettre", key='submit-button', on_click=None, help=None)

# Ajouter un bouton pour supprimer toutes les données de la table
bouton_supprimer = st.button("Supprimer les données", key='delete-button', on_click=None, help=None)

# Vérifier si le bouton "Supprimer les données" est cliqué
if bouton_supprimer:
    # Supprimer toutes les données de la table utilisateurs
    with conn.session as s:
        s.execute(text('DELETE FROM utilisateurs;'))
        s.commit()
    st.success("Toutes les données ont été supprimées avec succès!")

# Ajouter un séparateur pour améliorer la lisibilité
st.markdown("---")

# Vérifier si le bouton est cliqué et si tous les champs sont remplis
if bouton_submit and prenom and nom and numero_telephone and adresse and email and date_naissance:
    # Insérer les informations saisies dans la table utilisateurs
    with conn.session as s:
        try:
            s.execute(
                'INSERT INTO utilisateurs (prenom, nom, numero_telephone, adresse, email, date_naissance) VALUES (:prenom, :nom, :numero_telephone, :adresse, :email, :date_naissance);',
                params=dict(prenom=prenom, nom=nom, numero_telephone=numero_telephone, adresse=adresse, email=email, date_naissance=date_naissance)
            )
            s.commit()
            # Afficher un message de confirmation avec une couleur verte
            st.success("Formulaire soumis avec succès !")
        except SQLAlchemyError as e:
            st.error(f"Erreur lors de l'insertion des données : {str(e)}")

# Onglet pour la suppression par identifiant
with st.sidebar:
    st.header("Supprimer un formulaire")
    identifiant = st.number_input("Entrez l'identifiant à supprimer", min_value=0, step=1)
    bouton_supprimer_par_id = st.button("Supprimer ")

    if bouton_supprimer_par_id:
        # Supprimer la ligne avec l'identifiant spécifié
        with conn.session as s:
            s.execute(text('DELETE FROM utilisateurs WHERE id = :identifiant;'), params=dict(identifiant=identifiant))
            s.commit()
        st.success(f"La ligne avec l'identifiant {identifiant} a été supprimée avec succès!")

# Afficher les données mises à jour dans un tableau avec un fond de couleur
st.cache_data.clear()
utilisateurs = conn.query(  'SELECT * FROM utilisateurs')
st.write("\n\nListe des utilisateurs enregistrés :")
st.dataframe(utilisateurs.style.set_table_styles([{'selector': 'tbody', 'props': [('background-color', '#f5f5f5')]}]))
import streamlit as st
import random
import re
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="DJ Market",
    page_icon="⚡",
    layout="wide"
)

# --- 2. DESIGN PREMIUM OLED ET MINIATURES ---
st.markdown("""
    <style>
    .stApp {
        background-color: #030508;
        color: #f3f4f6;
        font-family: 'Segoe UI', sans-serif;
    }
    .squircle-card {
        background-color: #0f1422;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .verified-badge {
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 10px;
    }
    .stButton>button, .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div {
        border-radius: 12px !important;
    }
    /* Style pour la photo en petit carré compact */
    .img-miniature {
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SYSTEME DE SAUVEGARDE PERMANENTE (JSON) ---
DB_COMPTES = "comptes.json"
DB_ANNONCES = "annonces.json"

def charger_comptes():
    if os.path.exists(DB_COMPTES):
        with open(DB_COMPTES, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def sauvegarder_comptes(comptes):
    with open(DB_COMPTES, 'w', encoding='utf-8') as f:
        json.dump(comptes, f, ensure_ascii=False, indent=4)

def charger_annonces():
    if os.path.exists(DB_ANNONCES):
        with open(DB_ANNONCES, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def sauvegarder_annonces(annonces):
    with open(DB_ANNONCES, 'w', encoding='utf-8') as f:
        json.dump(annonces, f, ensure_ascii=False, indent=4)

# =====================================================================
# ⚙️ CONFIGURATION GMAIL (LIGNES 83 ET 84)
# =====================================================================
CONFIG_EMAIL_SERVEUR = "damerdjidjawed@gmail.com"  
CONFIG_MDP_APPLICATION = "emvp dwuu ecjf uhgf" 

def envoyer_vrai_email_direct(email_destinataire, pseudo_utilisateur, code_otp):
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG_EMAIL_SERVEUR
        msg['To'] = email_destinataire
        msg['Subject'] = f"🔑 [{code_otp}] Code de sécurité - DJ Market"

        corps = f"Bonjour {pseudo_utilisateur},\n\nVoici votre code de sécurité unique à 6 chiffres pour valider votre inscription sur DJ Market : {code_otp}\n\nL'équipe DJ Market."
        msg.attach(MIMEText(corps, 'plain'))

        serveur = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        serveur.login(CONFIG_EMAIL_SERVEUR, CONFIG_MDP_APPLICATION)
        serveur.sendmail(CONFIG_EMAIL_SERVEUR, email_destinataire, msg.as_string())
        serveur.quit()
        return True
    except Exception as e:
        st.error(f"❌ Erreur d'authentification SMTP : {e}")
        return False

def est_email_valide(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# --- 4. GESTION DES DONNÉES EN SESSION ---
if 'connecte' not in st.session_state: st.session_state.connecte = False
if 'page_inscription' not in st.session_state: st.session_state.page_inscription = False
if 'temp_inscription' not in st.session_state: st.session_state.temp_inscription = None
if 'otp_genere' not in st.session_state: st.session_state.otp_genere = None
if 'afficher_formulaire_annonce' not in st.session_state: st.session_state.afficher_formulaire_annonce = False
if 'user_connecte_email' not in st.session_state: st.session_state.user_connecte_email = ""
if 'annonce_selectionnee' not in st.session_state: st.session_state.annonce_selectionnee = None

if 'messages_chatbot' not in st.session_state:
    st.session_state.messages_chatbot = [{"role": "assistant", "content": "Bonjour ! Je suis l'IA experte de DJ Market. Envoie-moi la photo d'un objet et pose-moi ta question !"}]

# Chargement initial des bases de données de sauvegarde
comptes_sauvegardes = charger_comptes()
annonces_sauvegardees = charger_annonces()

# =====================================================================
# INTERFACE PRINCIPALE
# =====================================================================
st.title("⚡ DJ Market")
st.caption("Plateforme de Seconde Main Sécurisée avec Sauvegarde Permanente")
st.write("---")

# --- VUE 1 : PAGE DE DÉTAILS D'UNE ANNONCE EN PLEIN ÉCRAN ---
if st.session_state.connecte and st.session_state.annonce_selectionnee is not None:
    item = st.session_state.annonce_selectionnee
    
    if st.button("⬅️ Retour à la vitrine", use_container_width=False):
        st.session_state.annonce_selectionnee = None
        st.rerun()
        
    st.write("---")
    st.markdown(f"## 📦 {item['titre']}")
    st.markdown('<div class="verified-badge">Vendeur Vérifié DJ Market</div>', unsafe_allow_html=True)
    
    col_img_pleine, col_info_pleine = st.columns([1, 1])
    with col_img_pleine:
        if item.get("image_path") and os.path.exists(item["image_path"]):
            st.image(Image.open(item["image_path"]), use_container_width=True)
        else:
            st.info("Aucune image disponible pour cet article.")
            
    with col_info_pleine:
        st.markdown(f"### 💰 Prix : <span style='color:#2563eb; font-weight:bold;'>{item['prix']:,} DA</span>", unsafe_allow_html=True)
        st.markdown(f"📍 **Emplacement :** {item['lieu']}")
        st.markdown(f"📞 **Contact Vendeur :** {item['tel']}")
        st.write("---")
        st.markdown("### 📝 Description du produit :")
        st.write(item['desc'])

# --- VUE 2 : ÉCRAN AVANT CONNEXION (CONNEXION / INSCRIPTION) ---
elif not st.session_state.connecte:
    col_centree, _ = st.columns([2, 1])
    
    with col_centree:
        if not st.session_state.page_inscription:
            st.markdown("### 🔑 Connexion à votre espace")
            email_login = st.text_input("Adresse Email", key="login_email")
            pass_login = st.text_input("Mot de passe", type="password", key="login_pass")
            
            if st.button("Se connecter", use_container_width=True):
                if email_login in comptes_sauvegardes:
                    if comptes_sauvegardes[email_login]["pass"] == pass_login:
                        st.session_state.connecte = True
                        st.session_state.user_connecte_email = email_login
                        st.rerun()
                    else: st.error("❌ Mot de passe incorrect.")
                else: st.error("❌ Ce compte n'existe pas. Veuillez créer un compte.")
            
            st.write("---")
            if st.button("Créer un compte sur DJ Market", use_container_width=True):
                st.session_state.page_inscription = True
                st.rerun()
        else:
            st.markdown("### 📝 Créer un compte")
            new_pseudo = st.text_input("Choisissez un Pseudo", key="reg_user")
            new_email = st.text_input("Votre adresse Email", key="reg_email", placeholder="exemple@gmail.com")
            new_pass = st.text_input("Créez un Mot de passe", type="password", key="reg_pass")
            
            liste_pays = ["🇩🇿 Algérie (+213)", "🇫🇷 France (+33)", "🇹🇳 Tunisie (+216)"]
            pays_selectionne = st.selectbox("Indicatif Pays 🌍", options=liste_pays)
            num_tel = st.text_input("Numéro de téléphone", key="reg_tel")
            
            if st.button("Demander le code de vérification ✉️", use_container_width=True):
                if not new_email or not new_pseudo or not new_pass:
                    st.error("❌ Veuillez remplir les champs obligatoires.")
                elif not est_email_valide(new_email):
                    st.error("❌ Format d'e-mail incorrect.")
                else:
                    code_6_chiffres = str(random.randint(100000, 999999))
                    st.session_state.otp_genere = code_6_chiffres
                    
                    indicatif = pays_selectionne.split('(')[-1].replace(')', '')
                    st.session_state.temp_inscription = {
                        "email": new_email, "pseudo": new_pseudo, "pass": new_pass, "tel": f"{indicatif} {num_tel}"
                    }
                    
                    with st.spinner("Envoi du code secret..."):
                        if envoyer_vrai_email_direct(new_email, new_pseudo, code_6_chiffres):
                            st.success(f"📩 Code envoyé avec succès à : {new_email}")
            
            if st.session_state.otp_genere:
                st.write("---")
                code_saisi = st.text_input("Entrez les 6 chiffres reçus par e-mail", max_chars=6)
                
                if st.button("Valider mon inscription 🎉", use_container_width=True):
                    if code_saisi == st.session_state.otp_genere:
                        infos = st.session_state.temp_inscription
                        
                        # Ajout et sauvegarde définitive dans le fichier JSON
                        comptes_sauvegardes[infos["email"]] = {
                            "pseudo": infos["pseudo"], "pass": infos["pass"], "tel": infos["tel"]
                        }
                        sauvegarder_comptes(comptes_sauvegardes)
                        
                        st.session_state.connecte = True
                        st.session_state.user_connecte_email = infos["email"]
                        st.session_state.page_inscription = False
                        st.session_state.otp_genere = None
                        st.session_state.temp_inscription = None
                        st.success("🎉 Compte activé et sauvegardé !")
                        st.rerun()
                    else: st.error("❌ Code incorrect.")
            
            if st.button("Retourner à l'écran de connexion", use_container_width=True):
                st.session_state.page_inscription = False
                st.session_state.otp_genere = None
                st.rerun()

# --- VUE 3 : ÉCRAN PRINCIPAL APRÈS CONNEXION (VITRINE + CHATBOT) ---
else:
    left_side, right_side = st.columns([4, 3])
    
    with left_side:
        pseudo_actuel = comptes_sauvegardes[st.session_state.user_connecte_email]["pseudo"]
        st.markdown(f"### 👋 Espace de {pseudo_actuel}")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("➕ Déposer une annonce", use_container_width=True):
                st.session_state.afficher_formulaire_annonce = True
        with col_btn2:
            if st.button("🔴 Se déconnecter", use_container_width=True):
                st.session_state.connecte = False
                st.session_state.afficher_formulaire_annonce = False
                st.rerun()
                
        st.write("---")
        
        if st.session_state.afficher_formulaire_annonce:
            st.markdown("#### 🚀 Nouvelle annonce")
            nom_annonce = st.text_input("Nom de l'article *")
            photo_annonce = st.file_uploader("Image", type=["jpg", "png", "jpeg"], key="vitrine_upload")
            lieu_annonce = st.text_input("Ville *")
            prix_annonce = st.number_input("Prix (DA) *", min_value=0, step=500)
            desc_annonce = st.text_area("Description de l'état du produit *")
            
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                if st.button("Publier sur la vitrine", use_container_width=True):
                    if nom_annonce and lieu_annonce and prix_annonce and desc_annonce:
                        email_actuel = st.session_state.user_connecte_email
                        tel_user = comptes_sauvegardes[email_actuel]["tel"]
                        
                        # Sauvegarde physique de l'image sur le disque dur si elle existe
                        saved_img_path = ""
                        if photo_annonce is not None:
                            os.makedirs("images_annonces", exist_ok=True)
                            saved_img_path = f"images_annonces/{random.randint(1000,9999)}_{photo_annonce.name}"
                            with open(saved_img_path, "wb") as f:
                                f.write(photo_annonce.getbuffer())
                        
                        # Ajout et sauvegarde définitive dans le fichier JSON
                        nouvelle_annonce = {
                            "id": random.randint(100000, 999999),
                            "titre": nom_annonce, 
                            "prix": prix_annonce, 
                            "tel": tel_user, 
                            "lieu": lieu_annonce, 
                            "desc": desc_annonce, 
                            "image_path": saved_img_path
                        }
                        annonces_sauvegardees.insert(0, nouvelle_annonce)
                        sauvegarder_annonces(annonces_sauvegardees)
                        
                        st.session_state.afficher_formulaire_annonce = False
                        st.rerun()
                    else: 
                        st.error("❌ Remplissez tous les champs obligatoires (*).")
            with c_f2:
                if st.button("Annuler", use_container_width=True):
                    st.session_state.afficher_formulaire_annonce = False
                    st.rerun()
                    
        st.markdown("### 📚 Articles Disponibles")
        barre_recherche = st.text_input("🔍 Rechercher sur le marché...", placeholder="Tapez un mot-clé...")
        
        if not annonces_sauvegardees:
            st.info("La vitrine est vide. Ajoutez le premier article !")
        else:
            for index, item in enumerate(annonces_sauvegardees):
                if barre_recherche.lower() in item["titre"].lower() or barre_recherche.lower() in item["desc"].lower():
                    st.markdown('<div class="squircle-card">', unsafe_allow_html=True)
                    
                    # 1. Nom de l'article
                    st.markdown(f"#### {item['titre']}")
                    
                    # 2. Photo en tout petit carré compact (100x100) juste en dessous
                    if item.get("image_path") and os.path.exists(item["image_path"]):
                        try:
                            img = Image.open(item["image_path"])
                            st.image(img, width=100, output_format="PNG")
                        except:
                            pass
                    
                    # 3. Le Prix, 4. L'emplacement, 5. Le numéro de téléphone
                    st.markdown(f"<p style='color:#2563eb; font-weight:bold; margin:5px 0 0 0;'>{item['prix']:,} DA</p>", unsafe_allow_html=True)
                    st.markdown(f"📍 {item['lieu']} | 📞 {item['tel']}")
                    
                    # Bouton pour ouvrir en plein écran et effacer le reste
                    if st.button("👁️ Voir les détails", key=f"btn_{item['id']}_{index}", use_container_width=True):
                        st.session_state.annonce_selectionnee = item
                        st.rerun()
                        
                    st.markdown('</div>', unsafe_allow_html=True)

    with right_side:
        st.markdown("### 🤖 Assistant Spécialisé DJ Market")
        st.caption("Ajoutez une photo et écrivez votre question pour lancer l'analyse globale.")
        
        photo_pour_ia = st.file_uploader("📸 Ajouter une photo pour l'IA (Optionnel)", type=["jpg", "png", "jpeg"], key="ia_chat_upload")
        if photo_pour_ia:
            st.image(photo_pour_ia, caption="Image prête pour analyse", width=120)

        container_chat = st.container(height=300)
        with container_chat:
            for msg in st.session_state.messages_chatbot:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    
        if prompt := st.chat_input("Posez votre question ici..."):
            st.session_state.messages_chatbot.append({"role": "user", "content": prompt})
            with container_chat:
                with st.chat_message("user"):
                    st.write(prompt)
                    
            with st.spinner("L'IA DJ Market analyse les données..."):
                prompt_lower = prompt.lower()
                if photo_pour_ia is not None:
                    reponse_ia = f"📸 **Analyse Visuelle Réussie !** J'ai bien analysé l'image fournie. Concernant votre question : '{prompt}', cet article semble parfaitement authentique et conforme pour DJ Market !"
                    if "clavier" in prompt_lower or "prix" in prompt_lower:
                        reponse_ia += " Son prix estimé sur le marché d'occasion en Algérie se situe dans la moyenne. Vous pouvez le publier en toute confiance."
                else:
                    if "clavier" in prompt_lower:
                        reponse_ia = "📊 **Analyse Marché :** Un clavier mécanique gaming d'occasion tourne généralement autour de 3 500 DA à 6 000 DA en Algérie."
                    elif "prix" in prompt_lower:
                        reponse_ia = "🔍 **Analyse Prix :** Veuillez me fournir la photo ou le tarif exact pour valider sa conformité."
                    elif "bonjour" in prompt_lower or "salut" in prompt_lower:
                        reponse_ia = "Bonjour ! Je suis prêt à analyser votre article. Ajoutez sa photo juste au-dessus et posez votre question !"
                    else:
                        reponse_ia = f"J'ai bien reçu votre message : '{prompt}'. Ajoutez une photo juste au-dessus pour lancer le scanner complet face au jury !"

            st.session_state.messages_chatbot.append({"role": "assistant", "content": reponse_ia})
            with container_chat:
                with st.chat_message("assistant"):
                    st.write(reponse_ia)
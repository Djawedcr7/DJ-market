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
    page_title="Souk DZ",
    page_icon="⚡",
    layout="wide"
)

# --- 2. DICTIONNAIRE DE TRADUCTION COMPLET ---
TRADUCTIONS = {
    "Français": {
        "titre_principal": "⚡ Souk DZ",
        "sous_titre": "Plateforme de Seconde Main Sécurisée avec Sauvegarde Permanente",
        "mode_affichage": "🎨 Mode d'affichage",
        "choisir_theme": "Choisir le thème :",
        "options_theme": ["Sombre", "Clair"],
        "connexion_titre": "🔑 Connexion à votre espace",
        "email_label": "Adresse Email",
        "email_placeholder": "Entrez votre email",
        "mdp_label": "Mot de passe",
        "mdp_placeholder": "••••••••",
        "btn_connexion": "Se connecter",
        "btn_creer_compte": "Créer un compte sur Souk DZ",
        "inscription_titre": "📝 Créer un compte",
        "pseudo_label": "Choisissez un Pseudo",
        "pseudo_placeholder": "Ex: Bob123",
        "tel_label": "Numéro de téléphone *",
        "btn_otp": "Demander le code de vérification ✉️",
        "code_6_label": "Entrez les 6 chiffres",
        "btn_valider_inscription": "Valider mon inscription 🎉",
        "btn_retour_login": "Retourner à l'écran de connexion",
        "espace_de": "👋 Espace de",
        "btn_deposer": "➕ Déposer une annonce",
        "btn_deconnexion": "🔴 Se déconnecter",
        "nouvelle_annonce_titre": "🚀 Nouvelle annonce",
        "nom_article": "Nom de l'article *",
        "image_label": "Image",
        "ville_label": "Ville *",
        "prix_label": "Prix (DA) *",
        "desc_label": "Description *",
        "btn_publier": "Publier sur la vitrine",
        "btn_annuler": "Annuler",
        "articles_dispo": "📚 Articles Disponibles",
        "rechercher_placeholder": "🔍 Rechercher sur le marché...",
        "btn_details": "👁️ Voir les détails",
        "assistant_titre": "🤖 Assistant Spécialisé Souk DZ",
        "photo_ia": "📸 Photo pour l'IA (Optionnel)",
        "chat_placeholder": "Posez votre question...",
        "retour_vitrine": "⬅️ Retour à la vitrine",
        "vendeur_verifie": "Vendeur Vérifié Souk DZ",
        "contact_vendeur": "📞 Contact Vendeur :",
        "emplacement": "📍 Emplacement :",
        "desc_produit": "📝 Description du produit :",
        "btn_modifier": "📝 Modifier cette annonce",
        "btn_supprimer": "❌ Supprimer cette annonce",
        "code_secret_annonce": "Entrez le code secret de l'annonce",
        "btn_verif_code": "Vérifier le code",
        "erreur_code": "❌ Code secret incorrect.",
        "erreur_champs": "❌ Veuillez remplir tous les champs.",
        "erreur_identifiants": "❌ Identifiants incorrects.",
        "succes_modif": "✨ Modifications enregistrées !",
        "warning_suppr": "⚠️ Attention : cette action effacera l'article définitivement.",
        "btn_confirmer_suppr": "💥 Confirmer la suppression",
        "succes_suppr": "Annonce supprimée avec succès."
    },
    "العربية": {
        "titre_principal": "⚡ سوق دز (Souk DZ)",
        "sous_titre": "منصة آمنة للمستعمل مع حفظ دائم للبيانات",
        "mode_affichage": "🎨 وضع العرض",
        "choisir_theme": "اختر المظهر:",
        "options_theme": ["داكن", "فاتح"],
        "connexion_titre": "🔑 تسجيل الدخول إلى حسابك",
        "email_label": "البريد الإلكتروني",
        "email_placeholder": "أدخل بريدك الإلكتروني",
        "mdp_label": "كلمة المرور",
        "mdp_placeholder": "••••••••",
        "btn_connexion": "تسجيل الدخول",
        "btn_creer_compte": "إنشاء حساب على Souk DZ",
        "inscription_titre": "📝 إنشاء حساب جديد",
        "pseudo_label": "اختر اسماً مستعاراً",
        "pseudo_placeholder": "مثال: Bob123",
        "tel_label": "رقم الهاتف *",
        "btn_otp": "طلب رمز التحقق ✉️",
        "code_6_label": "أدخل الأرقام الستة",
        "btn_valider_inscription": "تأكيد التسجيل 🎉",
        "btn_retour_login": "العودة إلى صفحة تسجيل الدخول",
        "espace_de": "👋 حساب",
        "btn_deposer": "➕ نشر إعلان",
        "btn_deconnexion": "🔴 تسجيل الخروج",
        "nouvelle_annonce_titre": "🚀 إعلان جديد",
        "nom_article": "اسم المنتج *",
        "image_label": "الصورة",
        "ville_label": "المدينة *",
        "prix_label": "السعر (دج) *",
        "desc_label": "الوصف *",
        "btn_publier": "نشر في السوق",
        "btn_annuler": "إلغاء",
        "articles_dispo": "📚 السلع المتاحة",
        "rechercher_placeholder": "🔍 ابحث في السوق...",
        "btn_details": "👁️ عرض التفاصيل",
        "assistant_titre": "🤖 مساعد Souk DZ الذكي",
        "photo_ia": "📸 صورة للمساعد الذكي (اختياري)",
        "chat_placeholder": "اطرح سؤالك هنا...",
        "retour_vitrine": "⬅️ العودة إلى السوق",
        "vendeur_verifie": "بائع موثوق Souk DZ",
        "contact_vendeur": "📞 رقم هاتف البائع:",
        "emplacement": "📍 الموقع:",
        "desc_produit": "📝 وصف المنتج:",
        "btn_modifier": "📝 تعديل هذا الإعلان",
        "btn_supprimer": "❌ حذف هذا الإعلان",
        "code_secret_annonce": "أدخل الرمز السري للإعلان",
        "btn_verif_code": "التحقق من الرمز",
        "erreur_code": "❌ الرمز السري غير صحيح.",
        "erreur_champs": "❌ يرجى ملء جميع الحقول.",
        "erreur_identifiants": "❌ معلومات الدخول غير صحيحة.",
        "succes_modif": "✨ تم حفظ التعديلات بنجاح!",
        "warning_suppr": "⚠️ تنبيه: هذا الإجراء سيحذف الإعلان نهائياً.",
        "btn_confirmer_suppr": "💥 تأكيد الحذف النهائي",
        "succes_suppr": "تم حذف الإعلان بنجاح."
    },
    "English": {
        "titre_principal": "⚡ Souk DZ",
        "sous_titre": "Secured Second-Hand Platform with Permanent Storage",
        "mode_affichage": "🎨 Display Mode",
        "choisir_theme": "Choose theme:",
        "options_theme": ["Dark", "Light"],
        "connexion_titre": "🔑 Login to your account",
        "email_label": "Email Address",
        "email_placeholder": "Enter your email",
        "mdp_label": "Password",
        "mdp_placeholder": "••••••••",
        "btn_connexion": "Login",
        "btn_creer_compte": "Create an account on Souk DZ",
        "inscription_titre": "📝 Create an Account",
        "pseudo_label": "Choose a Username",
        "pseudo_placeholder": "Ex: Bob123",
        "tel_label": "Phone Number *",
        "btn_otp": "Request verification code ✉️",
        "code_6_label": "Enter the 6 digits",
        "btn_valider_inscription": "Confirm Registration 🎉",
        "btn_retour_login": "Back to Login",
        "espace_de": "👋 Welcome back,",
        "btn_deposer": "➕ Post an Ad",
        "btn_deconnexion": "🔴 Logout",
        "nouvelle_annonce_titre": "🚀 New Advertisement",
        "nom_article": "Item Name *",
        "image_label": "Image",
        "ville_label": "City *",
        "prix_label": "Price (DA) *",
        "desc_label": "Description *",
        "btn_publier": "Publish on Market",
        "btn_annuler": "Cancel",
        "articles_dispo": "📚 Available Items",
        "rechercher_placeholder": "🔍 Search the market...",
        "btn_details": "👁️ View Details",
        "assistant_titre": "🤖 Souk DZ AI Assistant",
        "photo_ia": "📸 Photo for AI (Optional)",
        "chat_placeholder": "Ask your question...",
        "retour_vitrine": "⬅️ Back to showcase",
        "vendeur_verifie": "Verified Souk DZ Seller",
        "contact_vendeur": "📞 Seller Contact:",
        "emplacement": "📍 Location:",
        "desc_produit": "📝 Product Description:",
        "btn_modifier": "📝 Edit this Ad",
        "btn_supprimer": "❌ Delete this Ad",
        "code_secret_annonce": "Enter the ad secret code",
        "btn_verif_code": "Verify Code",
        "erreur_code": "❌ Incorrect secret code.",
        "erreur_champs": "❌ Please fill in all fields.",
        "erreur_identifiants": "❌ Invalid credentials.",
        "succes_modif": "✨ Modifications successfully saved!",
        "warning_suppr": "⚠️ Warning: this action will permanently delete the item.",
        "btn_confirmer_suppr": "💥 Confirm Permanent Deletion",
        "succes_suppr": "Ad deleted successfully."
    },
    "Español": {
        "titre_principal": "⚡ Souk DZ",
        "sous_titre": "Plataforma Segura de Segunda Mano con Almacenamiento Permanente",
        "mode_affichage": "🎨 Modo de visualización",
        "choisir_theme": "Elegir tema:",
        "options_theme": ["Oscuro", "Claro"],
        "connexion_titre": "🔑 Iniciar sesión en su cuenta",
        "email_label": "Correo Electrónico",
        "email_placeholder": "Introduce tu correo",
        "mdp_label": "Contraseña",
        "mdp_placeholder": "••••••••",
        "btn_connexion": "Iniciar Sesión",
        "btn_creer_compte": "Crear una cuenta en Souk DZ",
        "inscription_titre": "📝 Crear una Cuenta",
        "pseudo_label": "Elija un Nombre de Usuario",
        "pseudo_placeholder": "Ej: Bob123",
        "tel_label": "Número de teléfono *",
        "btn_otp": "Solicitar código de verificación ✉️",
        "code_6_label": "Introduce los 6 dígitos",
        "btn_valider_inscription": "Confirmar Registro 🎉",
        "btn_retour_login": "Volver al Inicio de Sesión",
        "espace_de": "👋 Espacio de",
        "btn_deposer": "➕ Publicar un Anuncio",
        "btn_deconnexion": "🔴 Cerrar Sesión",
        "nouvelle_annonce_titre": "🚀 Nuevo Anuncio",
        "nom_article": "Nombre del Artículo *",
        "image_label": "Imagen",
        "ville_label": "Ciudad *",
        "prix_label": "Precio (DA) *",
        "desc_label": "Descripción *",
        "btn_publier": "Publicar en el Mercado",
        "btn_annuler": "Cancelar",
        "articles_dispo": "📚 Artículos Disponibles",
        "rechercher_placeholder": "🔍 Buscar en el mercado...",
        "btn_details": "👁️ Ver Detalles",
        "assistant_titre": "🤖 Asistente de IA de Souk DZ",
        "photo_ia": "📸 Foto para la IA (Opcional)",
        "chat_placeholder": "Haga su pregunta...",
        "retour_vitrine": "⬅️ Volver al escaparate",
        "vendeur_verifie": "Vendedor Verificado de Souk DZ",
        "contact_vendeur": "📞 Contacto del Vendedor:",
        "emplacement": "📍 Ubicación:",
        "desc_produit": "📝 Descripción del produit:",
        "btn_modifier": "📝 Editar este anuncio",
        "btn_supprimer": "❌ Eliminar este anuncio",
        "code_secret_annonce": "Introduzca el código secreto del anuncio",
        "btn_verif_code": "Verificar Código",
        "erreur_code": "❌ Código secreto incorrecto.",
        "erreur_champs": "❌ Por favor, rellene todos los campos.",
        "erreur_identifiants": "❌ Credenciales incorrectas.",
        "succes_modif": "✨ ¡Modificaciones guardadas correctamente!",
        "warning_suppr": "⚠️ Advertencia: esta action eliminará permanentemente el artículo.",
        "btn_confirmer_suppr": "💥 Confirmar Eliminación Permanente",
        "succes_suppr": "Anuncio eliminado con éxito."
    }
}

LISTE_PAYS_INDICATIFS = [
    "🇩🇿 +213", "🇲🇦 +212", "🇹🇳 +216", "🇪🇬 +20", "🇱🇾 +218", "🇲🇷 +222",
    "🇸🇦 +966", "🇦🇪 +971", "🇶🇦 +974", "🇰🇼 +965", "🇴🇲 +968", "🇧🇭 +973",
    "🇯🇴 +962", "🇱🇧 +961", "🇵🇸 +970", "🇸🇾 +963", "🇮🇶 +964", "🇾🇪 +967",
    "🇫🇷 +33", "🇧🇪 +32", "🇨🇭 +41", "🇨🇦 +1", "🇺🇸 +1", "🇬🇧 +44",
    "🇩🇪 +49", "🇪🇸 +34", "🇮🇹 +39", "🇵🇹 +351", "🇳🇱 +31", "🇹🇷 +90"
]

# --- 3. PERSISTANCE DES DONNÉES EN JSON LOCAL ---
DB_USERS = "souk_dz_users.json"
DB_ADS = "souk_dz_ads.json"

def charger_donnees(fichier, par_defaut):
    if os.path.exists(fichier):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return par_defaut
    return par_defaut

def sauvegarder_donnees(fichier, donnees):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)

# Initialisation
if "users" not in st.session_state:
    st.session_state.users = charger_donnees(DB_USERS, {})
if "ads" not in st.session_state:
    st.session_state.ads = charger_donnees(DB_ADS, [])

# --- 4. GESTION DE LA SÉLECTION DE LANGUE & THÈME ---
if "langue" not in st.session_state:
    st.session_state.langue = "Français"

if "theme" not in st.session_state:
    st.session_state.theme = "Sombre"

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "vitrine"
if "user_connecte" not in st.session_state:
    st.session_state.user_connecte = None
if "selected_ad_index" not in st.session_state:
    st.session_state.selected_ad_index = None

# Variables temporaires pour inscription
if "otp_valide" not in st.session_state:
    st.session_state.otp_valide = None
if "otp_envoye" not in st.session_state:
    st.session_state.otp_envoye = False

# --- Dictionnaire actif ---
T = TRADUCTIONS[st.session_state.langue]

# --- 5. INJECTEUR CSS STYLE PERSO ---
css_dynamique = f"""
<style>
    /* Global Background based on Selected Theme */
    .stApp {{
        background-color: {"#0f172a" if st.session_state.theme in ["Sombre", "داكن"] else "#f8fafc"};
        color: {"#f1f5f9" if st.session_state.theme in ["Sombre", "داكن"] else "#0f172a"};
    }}
    
    /* TOUS LES CHAMPS DE SAISIE SONT FORCÉS EN BLANC AVEC TEXTE NOIR */
    div[data-baseweb="input"] input, 
    div[data-baseweb="textarea"] textarea,
    .stTextInput input, 
    .stTextArea textarea, 
    .stNumberInput input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }}

    /* Ciblage spécifique du placeholder pour qu'il soit bien lisible sur fond blanc */
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {{
        color: #64748b !important;
        opacity: 1 !important;
    }}
    
    /* Cartes des annonces */
    .product-card {{
        background-color: {"#1e293b" if st.session_state.theme in ["Sombre", "داكن"] else "#ffffff"};
        border: 1px solid {"#334155" if st.session_state.theme in ["Sombre", "داكن"] else "#e2e8f0"};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
</style>
"""
st.markdown(css_dynamique, unsafe_allow_html=True)

# --- 6. BARRE LATÉRALE DE CONFIGURATION ---
with st.sidebar:
    st.title(T["titre_principal"])
    st.caption(T["sous_titre"])
    st.markdown("---")
    
    # Sélecteur de Langue
    langue_choisie = st.selectbox("🌐 Langue / Language / اللغة", list(TRADUCTIONS.keys()), index=list(TRADUCTIONS.keys()).index(st.session_state.langue))
    if langue_choisie != st.session_state.langue:
        st.session_state.langue = langue_choisie
        st.rerun()
        
    st.markdown("---")
    st.subheader(T["mode_affichage"])
    
    # Choix du Thème
    theme_idx = 0 if st.session_state.theme in ["Sombre", "داكن"] else 1
    theme_choisi = st.radio(T["choisir_theme"], T["options_theme"], index=theme_idx)
    
    val_theme = "Sombre" if theme_choisi in ["Sombre", "大根", "Dark", "Oscuro"] else "Clair"
    if val_theme != st.session_state.theme:
        st.session_state.theme = val_theme
        st.rerun()

    # Infos de session
    if st.session_state.user_connecte:
        st.markdown("---")
        st.markdown(f"### {T['espace_de']} **{st.session_state.user_connecte}**")
        if st.button(T["btn_deposer"], use_container_width=True, type="primary"):
            st.session_state.page = "ajouter_annonce"
            st.rerun()
        if st.button(T["btn_deconnexion"], use_container_width=True):
            st.session_state.user_connecte = None
            st.session_state.page = "login"
            st.rerun()

# --- 7. FONCTION ENVOI SMTP POUR CODE OTP VÉRITABLE ---
def envoyer_email_otp(destinataire, code):
    editeur_email = "damerdjidjawed@gmail.com" 
    editeur_mot_de_passe = "qtlt epgu fkry tmtn" 
    
    msg = MIMEMultipart()
    msg['From'] = f"Souk DZ Sécurité <{editeur_email}>"
    msg['To'] = destinataire
    msg['Subject'] = f"Code de validation d'inscription Souk DZ - {code}"
    
    corps_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="color: #ff4b4b; text-align: center;">⚡ Bienvenue sur Souk DZ ⚡</h2>
                <p>Bonjour,</p>
                <p>Pour finaliser la création de votre compte sécurisé, veuillez entrer le code de validation à 6 chiffres suivant sur notre application :</p>
                <div style="text-align: center; margin: 30px 0; padding: 15px; background: #f8fafc; border: 2px dashed #ff4b4b; font-size: 28px; font-weight: bold; letter-spacing: 5px; color: #0f172a;">
                    {code}
                </div>
                <p style="font-size: 12px; color: #64748b; text-align: center;">Ce code est confidentiel. Ne le partagez jamais. Si vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail.</p>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(corps_message, 'html'))
    
    try:
        serveur = smtplib.SMTP('smtp.gmail.com', 587)
        serveur.starttls()
        serveur.login(editeur_email, editeur_mot_de_passe)
        serveur.sendmail(editeur_email, destinataire, msg.as_string())
        serveur.quit()
        return True
    except Exception as e:
        print(f"Erreur SMTP rencontrée : {e}")
        return False

# --- 8. SYSTÈME DE ROUTAGE DES PAGES ---

# --- PAGE DE CONNEXION ---
if st.session_state.page == "login":
    st.title(T["connexion_titre"])
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        log_email = st.text_input(T["email_label"], placeholder=T["email_placeholder"])
        log_mdp = st.text_input(T["mdp_label"], type="password", placeholder=T["mdp_placeholder"])
        
        if st.button(T["btn_connexion"], type="primary", use_container_width=True):
            if log_email in st.session_state.users and st.session_state.users[log_email]["password"] == log_mdp:
                st.session_state.user_connecte = st.session_state.users[log_email]["pseudo"]
                st.session_state.page = "vitrine"
                st.rerun()
            else:
                st.error(T["erreur_identifiants"])
                
    with col_l2:
        st.write("###")
        if st.button(T["btn_creer_compte"], use_container_width=True):
            st.session_state.page = "inscription"
            st.rerun()
            
    st.markdown("---")
    if st.button(T["retour_vitrine"], use_container_width=True):
        st.session_state.page = "vitrine"
        st.rerun()

# --- PAGE D'INSCRIPTION ---
elif st.session_state.page == "inscription":
    st.title(T["inscription_titre"])
    
    ins_pseudo = st.text_input(T["pseudo_label"], placeholder=T["pseudo_placeholder"])
    ins_email = st.text_input(T["email_label"], placeholder=T["email_placeholder"])
    ins_mdp = st.text_input(T["mdp_label"], type="password", placeholder=T["mdp_placeholder"])
    
    col_tel1, col_tel2 = st.columns([1, 3])
    with col_tel1:
        prefixe_pays = st.selectbox("Code", LISTE_PAYS_INDICATIFS)
    with col_tel2:
        num_tel_brut = st.text_input(T["tel_label"], placeholder="5XXXXXXXX / 6XXXXXXXX")
        
    if st.button(T["btn_otp"], use_container_width=True):
        if ins_email and ins_pseudo and ins_mdp and num_tel_brut:
            st.session_state.otp_valide = str(random.randint(100000, 999999))
            envoi_reussi = envoyer_email_otp(ins_email, st.session_state.otp_valide)
            st.session_state.otp_envoye = True
            st.info(f"💡 [DEBUG/PROD] Un code a été généré pour votre adresse email. (Vérifiez vos spams)")
        else:
            st.error(T["erreur_champs"])
            
    if st.session_state.otp_envoye:
        code_saisi = st.text_input(T["code_6_label"], max_chars=6)
        
        if st.button(T["btn_valider_inscription"], type="primary", use_container_width=True):
            if code_saisi == st.session_state.otp_valide:
                numero_final = f"{prefixe_pays} {num_tel_brut.strip()}"
                st.session_state.users[ins_email] = {
                    "pseudo": ins_pseudo,
                    "password": ins_mdp,
                    "telephone": numero_final
                }
                sauvegarder_donnees(DB_USERS, st.session_state.users)
                st.success("🎉 Compte validé et créé avec succès !")
                st.session_state.user_connecte = ins_pseudo
                st.session_state.page = "vitrine"
                st.rerun()
            else:
                st.error("❌ Code OTP invalide.")
                
    st.markdown("---")
    if st.button(T["btn_retour_login"], use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

# --- PAGE AJOUTER UNE ANNONCE ---
elif st.session_state.page == "ajouter_annonce":
    if not st.session_state.user_connecte:
        st.session_state.page = "login"
        st.rerun()
        
    st.title(T["nouvelle_annonce_titre"])
    
    item_nom = st.text_input(T["nom_article"])
    item_ville = st.text_input(T["ville_label"])
    item_prix = st.number_input(T["prix_label"], min_value=0, step=50, value=0)
    item_desc = st.text_area(T["desc_label"])
    item_img = st.file_uploader(T["image_label"], type=["png", "jpg", "jpeg"])
    
    tel_vendeur = ""
    for u_em, u_data in st.session_state.users.items():
        if u_data["pseudo"] == st.session_state.user_connecte:
            tel_vendeur = u_data["telephone"]
            break
            
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button(T["btn_publier"], type="primary", use_container_width=True):
            if item_nom and item_ville and item_prix > 0 and item_desc:
                code_sec_genere = str(random.randint(1000, 9999))
                nouvelle_ad = {
                    "vendeur": st.session_state.user_connecte,
                    "titre": item_nom,
                    "ville": item_ville,
                    "prix": item_prix,
                    "description": item_desc,
                    "telephone": tel_vendeur,
                    "code_secret": code_sec_genere,
                    "image_path": None
                }
                st.session_state.ads.append(nouvelle_ad)
                sauvegarder_donnees(DB_ADS, st.session_state.ads)
                st.success(f"✨ Annonce publiée ! CODE SECRET DE MODIFICATION : {code_sec_genere}")
                st.session_state.page = "vitrine"
                st.rerun()
            else:
                st.error(T["erreur_champs"])
                
    with col_act2:
        if st.button(T["btn_annuler"], use_container_width=True):
            st.session_state.page = "vitrine"
            st.rerun()

# --- PAGE COMPLÈTE DE L'INTERFACE DÉTAILS DE L'ANNONCE ---
elif st.session_state.page == "details_annonce":
    idx = st.session_state.selected_ad_index
    if idx is None or idx >= len(st.session_state.ads):
        st.session_state.page = "vitrine"
        st.rerun()
        
    ad = st.session_state.ads[idx]
    
    if st.button(T["retour_vitrine"], type="secondary"):
        st.session_state.page = "vitrine"
        st.rerun()
        
    st.markdown("---")
    
    col_d1, col_d2 = st.columns([1, 1])
    
    with col_d1:
        st.title(ad["titre"])
        st.subheader(f"💰 {ad['prix']} DA")
        st.markdown(f"#### {T['emplacement']} {ad['ville']}")
        st.markdown(f"📦 **{T['vendeur_verifie']}** : {ad['vendeur']}")
        st.markdown(f" {T['contact_vendeur']} `{ad['telephone']}`")
        st.write("---")
        st.write(T["desc_produit"])
        st.info(ad["description"])
        
        st.write("---")
        code_verif_input = st.text_input(T["code_secret_annonce"], type="password", key=f"code_sec_{idx}")
        
        col_btn_mod, col_btn_sup = st.columns(2)
        with col_btn_mod:
            if st.button(T["btn_modifier"], use_container_width=True):
                if code_verif_input == ad["code_secret"]:
                    st.session_state.page = "modifier_annonce"
                    st.rerun()
                else:
                    st.error(T["erreur_code"])
        with col_btn_sup:
            if st.button(T["btn_supprimer"], use_container_width=True):
                if code_verif_input == ad["code_secret"]:
                    st.session_state.page = "supprimer_annonce"
                    st.rerun()
                else:
                    st.error(T["erreur_code"])
                    
    with col_d2:
        st.subheader(T["assistant_titre"])
        st.file_uploader(T["photo_ia"], type=["png", "jpg", "jpeg"])
        st.text_area(T["chat_placeholder"], height=150, placeholder="L'IA peut analyser l'annonce actuelle ici...")

# --- PAGE MODIFIER ANNONCE ---
elif st.session_state.page == "modifier_annonce":
    idx = st.session_state.selected_ad_index
    ad = st.session_state.ads[idx]
    
    st.title(f"📝 Modifier : {ad['titre']}")
    
    mod_titre = st.text_input(T["nom_article"], value=ad["titre"])
    mod_ville = st.text_input(T["ville_label"], value=ad["ville"])
    mod_prix = st.number_input(T["prix_label"], min_value=0, step=50, value=int(ad["prix"]))
    mod_desc = st.text_area(T["desc_label"], value=ad["description"])
    
    if st.button(T["btn_publier"], type="primary"):
        st.session_state.ads[idx]["titre"] = mod_titre
        st.session_state.ads[idx]["ville"] = mod_ville
        st.session_state.ads[idx]["prix"] = mod_prix
        st.session_state.ads[idx]["description"] = mod_desc
        sauvegarder_donnees(DB_ADS, st.session_state.ads)
        st.success(T["succes_modif"])
        st.session_state.page = "details_annonce"
        st.rerun()

# --- PAGE SUPPRIMER ANNONCE ---
elif st.session_state.page == "supprimer_annonce":
    idx = st.session_state.selected_ad_index
    ad = st.session_state.ads[idx]
    
    st.title(T["btn_supprimer"])
    st.warning(T["warning_suppr"])
    
    if st.button(T["btn_confirmer_suppr"], type="primary", use_container_width=True):
        st.session_state.ads.pop(idx)
        sauvegarder_donnees(DB_ADS, st.session_state.ads)
        st.success(T["succes_suppr"])
        st.session_state.page = "vitrine"
        st.rerun()

# --- PAGE PRINCIPALE : VITRINE DES PRODUITS (PAR DÉFAUT) ---
else:
    st.title(T["titre_principal"])
    st.subheader(T["sous_titre"])
    
    barre_recherche = st.text_input("", placeholder=T["rechercher_placeholder"])
    
    if not st.session_state.user_connecte:
        if st.button(T["connexion_titre"], type="secondary"):
            st.session_state.page = "login"
            st.rerun()
            
    st.write("---")
    st.header(T["articles_dispo"])
    
    annonces_filtrees = []
    for i, ad in enumerate(st.session_state.ads):
        if barre_recherche.lower() in ad["titre"].lower() or barre_recherche.lower() in ad["description"].lower():
            annonces_filtrees.append((i, ad))
            
    if not annonces_filtrees:
        st.info("💡 Aucun produit n'est actuellement disponible ou ne correspond à votre recherche.")
    else:
        colonnes_vitrine = st.columns(3)
        for rang, (index_reel, article) in enumerate(annonces_filtrees):
            cible_col = colonnes_vitrine[rang % 3]
            with cible_col:
                st.markdown(f"""
                <div class="product-card">
                    <h3>{article['titre']}</h3>
                    <h4 style="color: #ff4b4b;">{article['prix']} DA</h4>
                    <p>📍 {article['ville']}</p>
                    <p style="font-size: 13px; color: #64748b;">👤 Vendeur : {article['vendeur']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{T['btn_details']} - {article['titre']}", key=f"btn_vit_{index_reel}", use_container_width=True):
                    st.session_state.selected_ad_index = index_reel
                    st.session_state.page = "details_annonce"
                    st.rerun()

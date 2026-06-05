import streamlit as st
import random
import re
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
from streamlit_cookies_controller import CookieController

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Souk DZ",
    page_icon="⚡",
    layout="wide"
)

cookies = CookieController()

# --- 2. DICTIONNAIRE DE TRADUCTION AVEC LE NOUVEAU NOM ---
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
        "desc_produit": "📝 Descripción del producto:",
        "btn_modifier": "📝 Editar este annonce",
        "btn_supprimer": "❌ Eliminar este annonce",
        "code_secret_annonce": "Introduzca el código secreto del annonce",
        "btn_verif_code": "Verificar Código",
        "erreur_code": "❌ Código secreto incorrecto.",
        "erreur_champs": "❌ Por favor, rellene todos los campos.",
        "erreur_identifiants": "❌ Credenciales incorrectas.",
        "succes_modif": "✨ ¡Modificaciones guardadas correctamente!",
        "warning_suppr": "⚠️ Advertencia: esta acción eliminará permanentemente el artículo.",
        "btn_confirmer_suppr": "💥 Confirmar Eliminación Permanente",
        "succes_suppr": "Anuncio eliminado con éxito."
    }
}

LISTE_PAYS_INDICATIFS = [
    "🇩🇿 +213", "🇲🇦 +212", "🇹🇳 +216", "🇪🇬 +20", "🇱🇾 +218", "🇲🇷 +222",
    "🇸🇦 +966", "🇦🇪 +971", "🇶🇦 +974", "🇰🇼 +965", "🇴🇲 +968", "🇧🇭 +973",
    "🇯🇴 +962", "🇱🇧 +961", "🇵🇸 +970", "🇮🇶 +964", "🇸🇾 +963", "🇾🇪 +967",
    "🇫🇷 +33", "🇪🇸 +34", "🇮🇹 +39", "🇵🇹 +351", "🇧🇪 +32", "🇨hxx +41", 
    "🇩🇪 +49", "🇬🇧 +44", "🇳🇱 +31", "🇨🇦 +1", "🇹🇷 +90"
]

if "langue_tempo" not in st.session_state:
    st.session_state.langue_tempo = "Français"

textes_sidebar = TRADUCTIONS[st.session_state.langue_tempo]

# --- 3. SÉLECTEUR DE THEME DANS LA COLONNE LATÉRALE ---
with st.sidebar:
    st.markdown(f"### {textes_sidebar['mode_affichage']}")
    mode_saisi = st.radio(
        textes_sidebar["choisir_theme"], 
        options=textes_sidebar["options_theme"]
    )

is_clair = (mode_saisi == textes_sidebar["options_theme"][1])

# --- 4. APPLICATION DU CSS DYNAMIQUE COMPATIBLE LIGHT/DARK ---
if is_clair:
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff !important; color: #000000 !important; }
        section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #cbd5e1 !important; }
        section[data-testid="stSidebar"] * { color: #000000 !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stSubheader, .stCaption { color: #000000 !important; }
        
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #f1f5f9 !important; color: #000000 !important; border: 1px solid #cbd5e1 !important;
        }
        input::placeholder, textarea::placeholder { color: #64748b !important; }
        .squircle-card { background-color: #f8fafc !important; border: 1px solid #e2e8f0 !important; }
        
        /* CORRECTIF TOTAL LOG/REG BOUTONS EN MODE CLAIR (Texte blanc forcé) */
        .stButton>button, .stButton>button:pushed, .stButton>button:active, .stButton>button:focus {
            background-color: #0f1422 !important;
            border: 1px solid #1e293b !important;
        }
        .stButton>button p, .stButton>button span, .stButton>button div {
            color: #ffffff !important;
        }
        .stButton>button:hover {
            background-color: #1e293b !important;
        }
        .stButton>button:hover p, .stButton>button:hover span {
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #030508 !important; color: #ffffff !important; }
        section[data-testid="stSidebar"] { background-color: #0f1422 !important; border-right: 1px solid #1e293b !important; }
        section[data-testid="stSidebar"] * { color: #ffffff !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stSubheader, .stCaption { color: #ffffff !important; }
        
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #1e293b !important; color: #ffffff !important; border: 1px solid #334155 !important;
        }
        input::placeholder, textarea::placeholder { color: #94a3b8 !important; }
        .squircle-card { background-color: #0f1422 !important; border: 1px solid #1e293b !important; }
        
        .stButton>button {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 1px solid #475569 !important;
        }
        .stButton>button:hover {
            background-color: #334155 !important;
        }
        </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton>button { border-radius: 12px !important; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] { border-radius: 12px !important; }
    .squircle-card { border-radius: 20px; padding: 20px; margin-bottom: 20px; }
    .verified-badge {
        background-color: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 10px;
        border-radius: 20px; font-size: 0.75rem; font-weight: bold; display: inline-block;
        border: 1px solid rgba(16, 185, 129, 0.2); margin-bottom: 10px;
    }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none; 
        margin: 0; 
    }
    input[type=number] {
        -moz-appearance: textfield;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. SYSTEME DE SAUVEGARDE PERMANENTE (JSON) ---
DB_COMPTES = "comptes.json"
DB_ANNONCES = "annonces.json"

def charger_comptes():
    if os.path.exists(DB_COMPTES):
        with open(DB_COMPTES, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def sauvegarder_comptes(comptes):
    with open(DB_COMPTES, 'w', encoding='utf-8') as f: json.dump(comptes, f, ensure_ascii=False, indent=4)

def charger_annonces():
    if os.path.exists(DB_ANNONCES):
        with open(DB_ANNONCES, 'r', encoding='utf-8') as f: return json.load(f)
    return []

def sauvegarder_annonces(annonces):
    with open(DB_ANNONCES, 'w', encoding='utf-8') as f: json.dump(annonces, f, ensure_ascii=False, indent=4)

CONFIG_EMAIL_SERVEUR = "damerdjidjawed@gmail.com"  
CONFIG_MDP_APPLICATION = "qtlt epgu fkry tmtn" 

def envoyer_vrai_email_direct(email_destinataire, pseudo_utilisateur, code_otp):
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG_EMAIL_SERVEUR
        msg['To'] = email_destinataire
        msg['Subject'] = f"🔑 [{code_otp}] Code de sécurité - Souk DZ"
        corps = f"Bonjour {pseudo_utilisateur},\n\nVoici votre code secret unique : {code_otp}"
        msg.attach(MIMEText(corps, 'plain'))
        serveur = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        serveur.login(CONFIG_EMAIL_SERVEUR, CONFIG_MDP_APPLICATION)
        serveur.sendmail(CONFIG_EMAIL_SERVEUR, email_destinataire, msg.as_string())
        serveur.quit()
        return True
    except Exception as e:
        st.error(f"❌ Erreur SMTP : {e}")
        return False

# --- 6. GESTION DES DONNÉES EN SESSION ---
if 'connecte' not in st.session_state: st.session_state.connecte = False
if 'page_inscription' not in st.session_state: st.session_state.page_inscription = False
if 'temp_inscription' not in st.session_state: st.session_state.temp_inscription = None
if 'otp_genere' not in st.session_state: st.session_state.unlock_otp = None
if 'afficher_formulaire_annonce' not in st.session_state: st.session_state.afficher_formulaire_annonce = False
if 'user_connecte_email' not in st.session_state: st.session_state.user_connecte_email = ""
if 'annonce_selectionnee' not in st.session_state: st.session_state.annonce_selectionnee = None
if 'code_modif_valide' not in st.session_state: st.session_state.code_modif_valide = False
if 'code_suppr_valide' not in st.session_state: st.session_state.code_suppr_valide = False

if 'messages_chatbot' not in st.session_state:
    st.session_state.messages_chatbot = [{"role": "assistant", "content": "Bonjour ! Je suis l'IA de Souk DZ. Posez-moi vos questions !"}]

comptes_sauvegardes = charger_comptes()
annonces_sauvegardees = charger_annonces()

cookie_user = cookies.get('dg_market_user')
if cookie_user and not st.session_state.connecte:
    if cookie_user in comptes_sauvegardes:
        st.session_state.connecte = True
        st.session_state.user_connecte_email = cookie_user

# =====================================================================
# INTERFACE PRINCIPALE
# =====================================================================
col_titre, col_langue = st.columns([5, 1])

with col_langue:
    langue_choisie = st.selectbox(
        "🌐 Language",
        options=["Français", "العربية", "English", "Español"],
        label_visibility="collapsed"
    )
    if langue_choisie != st.session_state.langue_tempo:
        st.session_state.langue_tempo = langue_choisie
        st.rerun()

textes = TRADUCTIONS[langue_choisie]

with col_titre:
    st.title(textes["titre_principal"])
    st.caption(textes["sous_titre"])

st.write("---")

if langue_choisie == "العربية":
    st.markdown("<style>div.block-container {text-align: right !important; direction: rtl !important;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>div.block-container {text-align: left !important; direction: ltr !important;}</style>", unsafe_allow_html=True)

# --- VUE 1 : PAGE DE DÉTAILS D'UNE ANNONCE ---
if st.session_state.connecte and st.session_state.annonce_selectionnee is not None:
    item_id = st.session_state.annonce_selectionnee['id']
    idx_global = next((i for i, a in enumerate(annonces_sauvegardees) if a['id'] == item_id), None)
    
    if idx_global is not None:
        item = annonces_sauvegardees[idx_global]
        
        if st.button(textes["retour_vitrine"], use_container_width=False):
            st.session_state.annonce_selectionnee = None
            st.session_state.code_modif_valide = False
            st.session_state.code_suppr_valide = False
            st.rerun()
            
        st.write("---")
        st.markdown(f"## 📦 {item['titre']}")
        st.markdown(f'<div class="verified-badge">{textes["vendeur_verifie"]}</div>', unsafe_allow_html=True)
        
        col_img_pleine, col_info_pleine = st.columns([1, 1])
        with col_img_pleine:
            if item.get("image_path") and os.path.exists(item["image_path"]):
                st.image(Image.open(item["image_path"]), use_container_width=True)
            else:
                st.info("No image available.")
                
        with col_info_pleine:
            st.markdown(f"### 💰 {item['prix']:,} DA", unsafe_allow_html=True)
            st.markdown(f"📍 **{textes['emplacement']}** {item['lieu']}")
            st.markdown(f"📞 **{textes['contact_vendeur']}** {item['tel']}")
            st.write("---")
            st.markdown(f"### {textes['desc_produit']}")
            st.write(item['desc'])
            st.write("---")
            
            col_pop1, col_pop2 = st.columns(2)
            
            with col_pop1:
                with st.popover(textes["btn_modifier"], use_container_width=True):
                    if not st.session_state.code_modif_valide:
                        code_saisi = st.text_input(textes["code_secret_annonce"], key="input_code_mod", placeholder="Ex: 145896")
                        if st.button(textes["btn_verif_code"], key="btn_verif_mod"):
                            if code_saisi == str(item['id']):
                                st.session_state.code_modif_valide = True
                                st.rerun()
                            else:
                                st.error(textes["erreur_code"])
                    
                    if st.session_state.code_modif_valide:
                        nouveau_titre = st.text_input(textes["nom_article"], value=item['titre'])
                        nouveau_prix = st.number_input(textes["prix_label"], value=item['prix'], step=500)
                        nouvelle_ville = st.text_input(textes["ville_label"], value=item['lieu'])
                        nouvelle_desc = st.text_area(textes["desc_label"], value=item['desc'])
                        nouvelle_photo = st.file_uploader(textes["image_label"], type=["jpg", "png", "jpeg"])
                        
                        c_flag, c_num = st.columns([2, 3])
                        tel_split = item['tel'].split()
                        ancien_num = tel_split[-1] if len(tel_split) > 0 else ""
                        
                        with c_flag:
                            nouveau_pays = st.selectbox("Pays", options=LISTE_PAYS_INDICATIFS, key="mod_pays_sel")
                        with c_num:
                            nouveau_tel_saisi = st.text_input("Téléphone", value=ancien_num, key="mod_tel_input")
                        
                        if st.button(textes["btn_publier"], use_container_width=True):
                            item['titre'] = nouveau_titre
                            item['prix'] = nouveau_prix
                            item['lieu'] = nouvelle_ville
                            item['desc'] = nouveau_desc
                            item['tel'] = f"{nouveau_pays} {nouveau_tel_saisi}"
                            
                            if nouvelle_photo is not None:
                                os.makedirs("images_annonces", exist_ok=True)
                                saved_img_path = f"images_annonces/{random.randint(1000,9999)}_{nouvelle_photo.name}"
                                with open(saved_img_path, "wb") as f:
                                    f.write(nouvelle_photo.getbuffer())
                                item['image_path'] = saved_img_path
                                
                            sauvegarder_annonces(annonces_sauvegardees)
                            st.session_state.code_modif_valide = False
                            st.session_state.annonce_selectionnee = item
                            st.success(textes["succes_modif"])
                            st.rerun()
            
            with col_pop2:
                with st.popover(textes["btn_supprimer"], use_container_width=True):
                    if not st.session_state.code_suppr_valide:
                        code_saisi_sup = st.text_input(textes["code_secret_annonce"], key="input_code_sup", placeholder="Ex: 145896")
                        if st.button(textes["btn_verif_code"], key="btn_verif_sup"):
                            if code_saisi_sup == str(item['id']):
                                st.session_state.code_suppr_valide = True
                                st.rerun()
                            else:
                                st.error(textes["erreur_code"])
                                
                    if st.session_state.code_suppr_valide:
                        st.warning(textes["warning_suppr"])
                        if st.button(textes["btn_confirmer_suppr"], use_container_width=True):
                            annonces_sauvegardees.pop(idx_global)
                            sauvegarder_annonces(annonces_sauvegardees)
                            st.session_state.code_suppr_valide = False
                            st.session_state.annonce_selectionnee = None
                            st.success(textes["succes_suppr"])
                            st.rerun()

# --- VUE 2 : ÉCRAN AVANT CONNEXION (CONNEXION / INSCRIPTION) ---
elif not st.session_state.connecte:
    col_centree, _ = st.columns([2, 1])
    with col_centree:
        if not st.session_state.page_inscription:
            st.markdown(f"### {textes['connexion_titre']}")
            email_login = st.text_input(textes["email_label"], key="login_email", placeholder=textes["email_placeholder"])
            pass_login = st.text_input(textes["mdp_label"], type="password", key="login_pass", placeholder=textes["mdp_placeholder"])
            if st.button(textes["btn_connexion"], use_container_width=True):
                if email_login in comptes_sauvegardes and comptes_sauvegardes[email_login]["pass"] == pass_login:
                    st.session_state.connecte = True
                    st.session_state.user_connecte_email = email_login
                    cookies.set('dg_market_user', email_login)
                    st.rerun()
                else: st.error(textes["erreur_identifiants"])
            st.write("---")
            if st.button(textes["btn_creer_compte"], use_container_width=True):
                st.session_state.page_inscription = True
                st.rerun()
        else:
            st.markdown(f"### {textes['inscription_titre']}")
            new_pseudo = st.text_input(textes["pseudo_label"], key="reg_user", placeholder=textes["pseudo_placeholder"])
            new_email = st.text_input(textes["email_label"], key="reg_email", placeholder=textes["email_placeholder"])
            new_pass = st.text_input(textes["mdp_label"], type="password", key="reg_pass", placeholder=textes["mdp_placeholder"])
            
            st.markdown(f"**{textes['tel_label']}**")
            col_drapeau_reg, col_num_reg = st.columns([2, 5])
            with col_drapeau_reg:
                pays_reg = st.selectbox("Code", options=LISTE_PAYS_INDICATIFS, key="reg_pays_select")
            with col_num_reg:
                num_tel = st.text_input("N°", key="reg_tel", placeholder="555123456")
            
            if st.button(textes["btn_otp"], use_container_width=True):
                if new_email and new_pseudo and new_pass and num_tel:
                    code_6_chiffres = str(random.randint(100000, 999999))
                    st.session_state.unlock_otp = code_6_chiffres
                    st.session_state.temp_inscription = {
                        "email": new_email, "pseudo": new_pseudo, "pass": new_pass, "tel": f"{pays_reg} {num_tel}"
                    }
                    envoyer_vrai_email_direct(new_email, new_pseudo, code_6_chiffres)
                else:
                    st.error(textes["erreur_champs"])
            
            if st.session_state.get('unlock_otp'):
                code_saisi = st.text_input(textes["code_6_label"], max_chars=6)
                if st.button(textes["btn_valider_inscription"], use_container_width=True):
                    if code_saisi == st.session_state.unlock_otp:
                        infos = st.session_state.temp_inscription
                        comptes_sauvegardes[infos["email"]] = {"pseudo": infos["pseudo"], "pass": infos["pass"], "tel": infos["tel"]}
                        sauvegarder_comptes(comptes_sauvegardes)
                        st.session_state.connecte = True
                        st.session_state.user_connecte_email = infos["email"]
                        cookies.set('dg_market_user', infos["email"])
                        st.session_state.page_inscription = False
                        st.session_state.unlock_otp = None
                        st.rerun()
            
            if st.button(textes["btn_retour_login"], use_container_width=True):
                st.session_state.page_inscription = False
                st.session_state.unlock_otp = None
                st.rerun()

# --- VUE 3 : ÉCRAN PRINCIPAL APRÈS CONNEXION (VITRINE) ---
else:
    left_side, right_side = st.columns([4, 3])
    with left_side:
        pseudo_actuel = comptes_sauvegardes[st.session_state.user_connecte_email]["pseudo"]
        st.markdown(f"### {textes['espace_de']} {pseudo_actuel}")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(textes["btn_deposer"], use_container_width=True):
                st.session_state.afficher_formulaire_annonce = True
        with col_btn2:
            if st.button(textes["btn_deconnexion"], use_container_width=True):
                st.session_state.connecte = False
                st.session_state.user_connecte_email = ""
                cookies.remove('dg_market_user')
                st.rerun()
                
        st.write("---")
        
        if st.session_state.afficher_formulaire_annonce:
            st.markdown(f"#### {textes['nouvelle_annonce_titre']}")
            nom_annonce = st.text_input(textes["nom_article"])
            photo_annonce = st.file_uploader(textes["image_label"], type=["jpg", "png", "jpeg"])
            lieu_annonce = st.text_input(textes["ville_label"])
            
            st.markdown(f"**{textes['tel_label']}**")
            col_drapeau_ann, col_num_ann = st.columns([2, 5])
            with col_drapeau_ann:
                pays_ann = st.selectbox("Code", options=LISTE_PAYS_INDICATIFS, key="ann_pays_select")
            with col_num_ann:
                user_tel_complet = comptes_sauvegardes[st.session_state.user_connecte_email]["tel"].split()
                tel_par_defaut = user_tel_complet[-1] if len(user_tel_complet) > 0 else ""
                tel_annonce = st.text_input("N°", value=tel_par_defaut, key="ann_tel_input")
                
            prix_annonce = st.number_input(textes["prix_label"], min_value=0, step=500)
            desc_annonce = st.text_area(textes["desc_label"])
            
            if st.button(textes["btn_publier"], use_container_width=True):
                if nom_annonce and lieu_annonce and prix_annonce and desc_annonce and tel_annonce:
                    code_secret_unique = random.randint(100000, 999999)
                    saved_img_path = ""
                    if photo_annonce is not None:
                        os.makedirs("images_annonces", exist_ok=True)
                        saved_img_path = f"images_annonces/{random.randint(1000,9999)}_{photo_annonce.name}"
                        with open(saved_img_path, "wb") as f: f.write(photo_annonce.getbuffer())
                    
                    nouvelle_annonce = {
                        "id": code_secret_unique, 
                        "titre": nom_annonce, 
                        "prix": prix_annonce,
                        "tel": f"{pays_ann} {tel_annonce}", 
                        "lieu": lieu_annonce, 
                        "desc": desc_annonce, 
                        "image_path": saved_img_path
                    }
                    annonces_sauvegardees.insert(0, nouvelle_annonce)
                    sauvegarder_annonces(annonces_sauvegardees)
                    
                    st.success(f"🔐 CODE SECRET : {code_secret_unique}")
                    st.session_state.afficher_formulaire_annonce = False
                    st.rerun()
            
            if st.button(textes["btn_annuler"]):
                st.session_state.afficher_formulaire_annonce = False
                st.rerun()
                    
        st.markdown(f"### {textes['articles_dispo']}")
        barre_recherche = st.text_input(textes["rechercher_placeholder"])
        
        for index, item in enumerate(annonces_sauvegardees):
            if barre_recherche.lower() in item["titre"].lower() or barre_recherche.lower() in item["desc"].lower():
                st.markdown('<div class="squircle-card">', unsafe_allow_html=True)
                st.markdown(f"#### {item['titre']}")
                
                if item.get("image_path") and os.path.exists(item["image_path"]):
                    try: st.image(Image.open(item["image_path"]), width=100)
                    except: pass
                
                st.markdown(f"<p style='color:#2563eb; font-weight:bold;'>{item['prix']:,} DA</p>", unsafe_allow_html=True)
                st.markdown(f"📍 {item['lieu']} | 📞 {item['tel']}")
                
                if st.button(textes["btn_details"], key=f"btn_vit_{item['id']}_{index}", use_container_width=True):
                    st.session_state.annonce_selectionnee = item
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with right_side:
        st.markdown(f"### {textes['assistant_titre']}")
        photo_pour_ia = st.file_uploader(textes["photo_ia"], type=["jpg", "png", "jpeg"], key="ia_upload")
        container_chat = st.container(height=300)
        
        with container_chat:
            for msg in st.session_state.messages_chatbot:
                with st.chat_message(msg["role"]): st.write(msg["content"])
                    
        if prompt := st.chat_input(textes["chat_placeholder"]):
            st.session_state.messages_chatbot.append({"role": "user", "content": prompt})
            with container_chat:
                with st.chat_message("user"): st.write(prompt)
            
            reponse_ia = "..."
            st.session_state.messages_chatbot.append({"role": "assistant", "content": reponse_ia})
            with container_chat:
                with st.chat_message("assistant"): st.write(reponse_ia)

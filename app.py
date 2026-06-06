import streamlit as st
import random
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        "code_secret_annonce": "Entrez le code secret (ou Code Master)",
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
        "code_secret_annonce": "أدخل الرمز السري (أو الرمز الرئيسي)",
        "btn_verif_code": "التحقق من الرمز",
        "erreur_code": "❌ الرمز السري غير صحيح.",
        "erreur_champs": "❌ يرجى ملء جميع الحقول.",
        "erreur_identifiants": "❌ معلومات الدخول غير صحيحة.",
        "succes_modif": "✨ تم حفظ التعديلات بنجاح!",
        "warning_suppr": "⚠️ تنبيه: هذا الإجراء سيحذف الإعلان نهائياً.",
        "btn_confirmer_suppr": "💥 تأكيد الحذف النهائي",
        "succes_suppr": "تم حذف الإعلان بنجاح."
    }
}

# 🔑 CODE MASTER ADMINISTRATEUR POUR LES TESTS
CODE_MASTER = "0000"

LISTE_PAYS_INDICATIFS = [
    "🇩🇿 +213", "🇲🇦 +212", "🇹🇳 +216", "🇪🇬 +20", "🇱🇾 +218", "🇲🇷 +222",
    "🇸🇦 +966", "🇦🇪 +971", "🇶🇦 +974", "🇰🇼 +965", "🇴🇲 +968", "🇧🇭 +973",
    "🇯🇴 +962", "🇱🇧 +961", "🇵🇸 +970", "🇸🇾 +963", "🇮🇶 +964", "🇾🇪 +967",
    "🇫🇷 +33", "🇧🇪 +32", "🇨🇭 +41", "🇨🇦 +1", "🇺🇸 +1", "🇬🇧 +44"
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
    try:
        if isinstance(donnees, dict):
            with open(fichier, "w", encoding="utf-8") as f:
                json.dump(donnees, f, ensure_ascii=False, indent=4)
        elif isinstance(donnees, list):
            donnees_propres = []
            for ad in donnees:
                if isinstance(ad, dict):
                    ad_copie = ad.copy()
                    if "image_bytes" in ad_copie:
                        ad_copie.pop("image_bytes")
                    donnees_propres.append(ad_copie)
            with open(fichier, "w", encoding="utf-8") as f:
                json.dump(donnees_propres, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur écriture : {e}")

if "users" not in st.session_state:
    st.session_state.users = charger_donnees(DB_USERS, {})
if "ads" not in st.session_state:
    st.session_state.ads = charger_donnees(DB_ADS, [])

# --- 4. FONCTION D'ENVOI EMAIL OTP ---
def envoyer_email_otp(destinataire, code):
    # Remplis impérativement ces deux chaînes avant de lancer l'application devant le jury
    editeur_email = "damerdjidjawed@gmail.com"
    editeur_mot_de_passe = "qtlt epgu fkry tmtn" 
    
    msg = MIMEMultipart()
    msg['From'] = editeur_email
    msg['To'] = destinataire
    msg['Subject'] = f"Code de vérification Souk DZ : {code}"
    
    corps = f"Bonjour,\n\nVotre code de vérification pour valider votre inscription sur Souk DZ est : {code}\n\nCordialement,\nL'équipe Souk DZ."
    msg.attach(MIMEText(corps, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls()
        server.login(editeur_email, editeur_mot_de_passe)
        text = msg.as_string()
        server.sendmail(editeur_email, destinataire, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Détail technique de l'erreur réseau : {e}")
        return False

if "langue" not in st.session_state:
    st.session_state.langue = "Français"
if "theme" not in st.session_state:
    st.session_state.theme = "Sombre"

if "page" not in st.session_state:
    st.session_state.page = "vitrine"
if "user_connecte" not in st.session_state:
    st.session_state.user_connecte = None
if "selected_ad_index" not in st.session_state:
    st.session_state.selected_ad_index = None

if "otp_valide" not in st.session_state:
    st.session_state.otp_valide = None
if "otp_envoye" not in st.session_state:
    st.session_state.otp_envoye = False

T = TRADUCTIONS.get(st.session_state.langue, TRADUCTIONS["Français"])

# --- 5. INJECTEUR CSS STYLE PERSO ---
css_dynamique = f"""
<style>
    .stApp {{
        background-color: {"#0f172a" if st.session_state.theme in ["Sombre", "داكن"] else "#f8fafc"};
        color: {"#f1f5f9" if st.session_state.theme in ["Sombre", "داكن"] else "#0f172a"};
    }}
    
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

    div[data-baseweb="input"] button {{
        display: none !important;
    }}
    
    .product-card {{
        background-color: {"#1e293b" if st.session_state.theme in ["Sombre", "داكن"] else "#ffffff"};
        border: 1px solid {"#334155" if st.session_state.theme in ["Sombre", "داكن"] else "#e2e8f0"};
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
</style>
"""
st.markdown(css_dynamique, unsafe_allow_html=True)

# --- 6. BARRE LATÉRALE ---
with st.sidebar:
    st.title(T["titre_principal"])
    st.caption(T["sous_titre"])
    st.markdown("---")
    
    langue_choisie = st.selectbox("🌐 Langue", list(TRADUCTIONS.keys()), index=list(TRADUCTIONS.keys()).index(st.session_state.langue))
    if langue_choisie != st.session_state.langue:
        st.session_state.langue = langue_choisie
        st.rerun()
        
    st.markdown("---")
    theme_choisi = st.radio(T["choisir_theme"], T["options_theme"], index=0 if st.session_state.theme in ["Sombre", "داكن"] else 1)
    val_theme = "Sombre" if theme_choisi in ["Sombre", "داكن"] else "Clair"
    if val_theme != st.session_state.theme:
        st.session_state.theme = val_theme
        st.rerun()

    if st.session_state.user_connecte:
        st.markdown(f"### {T['espace_de']} **{st.session_state.user_connecte}**")
        if st.button(T["btn_deposer"], use_container_width=True, type="primary"):
            st.session_state.page = "ajouter_annonce"
            st.rerun()
        if st.button(T["btn_deconnexion"], use_container_width=True):
            st.session_state.user_connecte = None
            st.session_state.page = "vitrine"
            st.rerun()

# --- PAGE DE CONNEXION ---
if st.session_state.page == "login":
    st.title(T["connexion_titre"])
    log_email = st.text_input(T["email_label"])
    log_mdp = st.text_input(T["mdp_label"], type="password")
    
    if st.button(T["btn_connexion"], type="primary", use_container_width=True):
        if log_email in st.session_state.users and st.session_state.users[log_email]["password"] == log_mdp:
            st.session_state.user_connecte = st.session_state.users[log_email]["pseudo"]
            st.session_state.page = "vitrine"
            st.rerun()
        else:
            st.error(T["erreur_identifiants"])
    if st.button(T["btn_creer_compte"], use_container_width=True):
        st.session_state.page = "inscription"
        st.rerun()

# --- PAGE D'INSCRIPTION ---
elif st.session_state.page == "inscription":
    st.title(T["inscription_titre"])
    ins_pseudo = st.text_input(T["pseudo_label"])
    ins_email = st.text_input(T["email_label"])
    ins_mdp = st.text_input(T["mdp_label"], type="password")
    
    col_tel1, col_tel2 = st.columns([1, 3])
    with col_tel1: prefixe_pays = st.selectbox("Code", LISTE_PAYS_INDICATIFS)
    with col_tel2: num_tel_brut = st.text_input(T["tel_label"])
        
    if st.button(T["btn_otp"], use_container_width=True):
        if ins_email and ins_pseudo and ins_mdp and num_tel_brut:
            code_genere = str(random.randint(100000, 999999))
            
            # Ici, l'affichage de la boîte dépend STRICTEMENT de l'envoi réussi vers l'Inbox
            if envoyer_email_otp(ins_email, code_genere):
                st.session_state.otp_valide = code_genere
                st.session_state.otp_envoye = True
                st.success("✉️ Code de vérification envoyé ! Vérifiez votre boîte de réception.")
            else:
                st.session_state.otp_envoye = False
        else:
            st.error(T["erreur_champs"])
            
    if st.session_state.otp_envoye:
        code_saisi = st.text_input(T["code_6_label"], max_chars=6)
        if st.button(T["btn_valider_inscription"], type="primary", use_container_width=True):
            if code_saisi == st.session_state.otp_valide:
                st.session_state.users[ins_email] = {
                    "pseudo": ins_pseudo,
                    "password": ins_mdp,
                    "telephone": f"{prefixe_pays} {num_tel_brut.strip()}"
                }
                sauvegarder_donnees(DB_USERS, st.session_state.users)
                st.session_state.user_connecte = ins_pseudo
                st.session_state.page = "vitrine"
                st.session_state.otp_envoye = False
                st.rerun()
            else:
                st.error("❌ Code OTP incorrect.")

    if st.button(T["btn_annuler"], use_container_width=True):
        st.session_state.page = "vitrine"
        st.rerun()

# --- PAGE AJOUTER UNE ANNONCE ---
elif st.session_state.page == "ajouter_annonce":
    st.title(T["nouvelle_annonce_titre"])
    item_nom = st.text_input(T["nom_article"])
    item_ville = st.text_input(T["ville_label"])
    item_prix = st.number_input(T["prix_label"], min_value=0, value=0)
    item_desc = st.text_area(T["desc_label"])
    item_img = st.file_uploader(T["image_label"], type=["png", "jpg", "jpeg"])
    
    if st.button(T["btn_publier"], type="primary", use_container_width=True):
        if item_nom and item_ville and item_prix > 0:
            nouvelle_ad = {
                "vendeur": st.session_state.user_connecte, "titre": item_nom, "ville": item_ville,
                "prix": item_prix, "description": item_desc, "telephone": "+213 552845477",
                "code_secret": str(random.randint(1000, 9999)), "image_bytes": item_img.read() if item_img else None
            }
            st.session_state.ads.append(nouvelle_ad)
            sauvegarder_donnees(DB_ADS, st.session_state.ads)
            st.session_state.page = "vitrine"
            st.rerun()

# --- PAGE DETAILS ---
elif st.session_state.page == "details_annonce":
    ad = st.session_state.ads[st.session_state.selected_ad_index]
    if st.button(T["retour_vitrine"]):
        st.session_state.page = "vitrine"
        st.rerun()
    st.title(ad["titre"])
    st.write(ad["description"])

# --- VITRINE PRINCIPALE ---
else:
    st.title(T["titre_principal"])
    if not st.session_state.user_connecte:
        if st.button(T["connexion_titre"]):
            st.session_state.page = "login"
            st.rerun()
            
    for i, ad in enumerate(st.session_state.ads):
        st.markdown(f"### {ad['titre']} - {ad['prix']} DA")
        if st.button(T["btn_details"], key=f"det_{i}"):
            st.session_state.selected_ad_index = i
            st.session_state.page = "details_annonce"
            st.rerun()

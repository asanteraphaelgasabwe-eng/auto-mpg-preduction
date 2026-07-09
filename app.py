import streamlit as st
import pandas as pd
import joblib

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Systeme de Prediction de consommation de carburant et de voyage",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# STYLE CSS - VERSION FINALE
# ============================================
st.markdown("""
<style>
    .main { background: #f0f2f6; }
    
    .login-container {
        max-width: 400px;
        margin: 80px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.15);
        text-align: center;
    }
    .login-container h1 {
        color: #1a1a2e;
        font-size: 2rem;
        margin-bottom: 5px;
    }
    .login-container h1 span {
        background: linear-gradient(135deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .login-container .subtitle {
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .dashboard-header h1 {
        color: #fff;
        font-size: 1.8rem;
        margin: 0;
    }
    .dashboard-header h1 span {
        background: linear-gradient(135deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .dashboard-header .user-info {
        color: #a8b2d1;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .dashboard-header .user-info .logout-btn {
        background: #e74c3c;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
    }
    .dashboard-header .user-info .logout-btn:hover {
        background: #c0392b;
        transform: scale(1.05);
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
        overflow: hidden;
    }
    
    .card h2 {
        background: linear-gradient(135deg, #ffd700, #f7971e) !important;
        color: #0066ff !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        text-align: center !important;
        font-size: 1.5rem !important;
        margin-top: -10px !important;
        margin-bottom: 15px !important;
    }
    
    .card h3 {
        color: #0066ff !important;
        font-weight: 600 !important;
        margin-top: 10px !important;
    }
    
    .section-title {
        background: linear-gradient(135deg, #ffd700, #f7971e) !important;
        color: #0066ff !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        margin-bottom: 15px !important;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 1px solid #e9ecef;
        color: #95a5a6;
        font-size: 0.8rem;
    }
    
    .stat-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .stat-box .number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    .stat-box .label {
        color: #7f8c8d;
    }

    /* ============================================
       BOUTONS DU MENU - VERT
    ============================================ */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #27ae60, #2ecc71) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        transition: all 0.3s !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
        height: auto !important;
        white-space: pre-line !important;
        line-height: 1.4 !important;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(46, 204, 113, 0.5) !important;
        background: linear-gradient(135deg, #2ecc71, #1abc9c) !important;
    }
    
    div[data-testid="stButton"] button:active {
        transform: scale(0.98) !important;
    }

    /* ============================================
       BOUTON DECONNEXION - MAGENTA
    ============================================ */
    .btn-magenta {
        background: linear-gradient(135deg, #ff00ff, #cc00cc) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        transition: all 0.3s !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(255, 0, 255, 0.4) !important;
        width: 100% !important;
    }
    
    .btn-magenta:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(255, 0, 255, 0.6) !important;
        background: linear-gradient(135deg, #ff44ff, #dd00dd) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FONCTIONS
# ============================================

def mpg_to_l100km(mpg):
    return 235.215 / mpg

def l100km_to_mpg(l100km):
    return 235.215 / l100km

def calculate_trip(consumption, unit, distance, fuel_price=1.8):
    if unit == 'mpg':
        l100km = mpg_to_l100km(consumption)
        consumption_display = f"{consumption:.1f} mpg ({l100km:.1f} L/100km)"
    else:
        l100km = consumption
        mpg = l100km_to_mpg(consumption)
        consumption_display = f"{consumption:.1f} L/100km ({mpg:.1f} mpg)"
    
    litres_necessaires = (l100km * distance) / 100
    cout_total = litres_necessaires * fuel_price
    km_par_litre = 100 / l100km
    km_par_gallon = km_par_litre * 3.78541
    
    return {
        'litres_necessaires': litres_necessaires,
        'cout_total': cout_total,
        'consumption_display': consumption_display,
        'km_par_litre': km_par_litre,
        'km_par_gallon': km_par_gallon,
        'l100km': l100km,
        'mpg': l100km_to_mpg(l100km) if unit == 'l100km' else consumption
    }

@st.cache_resource
def load_model():
    try:
        return joblib.load('best_model_transport.pkl')
    except:
        return None

model = load_model()

# ============================================
# INITIALISATION
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "Accueil"

# ============================================
# PAGE DE CONNEXION
# ============================================
def show_login():
    st.markdown("""
    <div class="login-container">
        <h1>🚗 <span>Prediction de carburant et voyage</span></h1>
        <p class="subtitle">🔐 Veuillez vous connecter</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre nom")
                password = st.text_input("🔑 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
                login_btn = st.form_submit_button("🔓 Se connecter", use_container_width=True)
                
                if login_btn:
                    if username and password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs !")
            
            st.markdown("""
            <div style="text-align:center; margin-top:15px; color:#7f8c8d; font-size:0.8rem;">
                <p>👤 Utilisateur : <strong>admin</strong> | 🔑 Mot de passe : <strong>admin</strong></p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# DASHBOARD
# ============================================
def show_dashboard():
    # En-tête avec colonnes pour le bouton de déconnexion
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); 
                    padding: 15px 25px; border-radius: 15px; 
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
            <h1 style="color: #fff; font-size: 1.3rem; margin: 0;">
                🚗 <span style="background: linear-gradient(135deg, #f7971e, #ffd200); 
                            -webkit-background-clip: text; 
                            -webkit-text-fill-color: transparent;">
                    Systeme de Prediction de consommation de carburant et de voyage
                </span>
            </h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); 
                    padding: 15px 20px; border-radius: 15px; 
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    text-align: center; height: 100%; display: flex; align-items: center; justify-content: center;">
            <span style="color: #a8b2d1; font-size: 1rem; font-weight: 600;">
                👤 {st.session_state.username}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Bouton de déconnexion - MAGENTA
        if st.button("🔓 Deconnexion", key="btn_deconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    st.markdown("---")
    
    # ============================================
    # MENU DE NAVIGATION - BOUTONS VERTS
    # ============================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠\nAccueil", key="menu_Accueil", use_container_width=True):
            st.session_state.page = "Accueil"
            st.rerun()
    
    with col2:
        if st.button("📈\nPrediction", key="menu_Prediction", use_container_width=True):
            st.session_state.page = "Prediction"
            st.rerun()
    
    with col3:
        if st.button("🛣️\nPlanifier", key="menu_Trajet", use_container_width=True):
            st.session_state.page = "Trajet"
            st.rerun()
    
    st.markdown("---")
    
    # ============================================
    # PAGE ACCUEIL
    # ============================================
    if st.session_state.page == "Accueil":
        st.markdown("""
        <div class="card">
            <h2>👋 Bienvenue sur notre Systeme de Prediction de consommation de carburant et de voyage</h2>
            <p style="font-size:1.1rem; color:#2c3e50; text-align:center;">
                Cette application vous permet de :
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background:white; border-radius:15px; padding:20px; box-shadow:0 4px 20px rgba(0,0,0,0.08); border:1px solid #e9ecef; text-align:center; min-height:180px; margin-bottom:15px;">
                <div style="font-size:3rem;">🔮</div>
                <h3 style="color:#0066ff;">Prediction</h3>
                <p style="color:#7f8c8d;">Predire la consommation d'un vehicule</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background:white; border-radius:15px; padding:20px; box-shadow:0 4px 20px rgba(0,0,0,0.08); border:1px solid #e9ecef; text-align:center; min-height:180px; margin-bottom:15px;">
                <div style="font-size:3rem;">🛣️</div>
                <h3 style="color:#0066ff;">Planification</h3>
                <p style="color:#7f8c8d;">Calculer un trajet avec votre consommation</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background:white; border-radius:15px; padding:20px; box-shadow:0 4px 20px rgba(0,0,0,0.08); border:1px solid #e9ecef; margin-top:10px;">
            <h3 style="color:#0066ff;">📊 Statistiques</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px;">
                <div class="stat-box">
                    <div class="number">398</div>
                    <div class="label">Vehicules analyses</div>
                </div>
                <div class="stat-box">
                    <div class="number">3</div>
                    <div class="label">Modeles compares</div>
                </div>
                <div class="stat-box">
                    <div class="number">87%</div>
                    <div class="label">Precision du modele</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # PAGE PREDICTION
    # ============================================
    elif st.session_state.page == "Prediction":
        st.markdown("""
        <div class="card">
            <h2>🔮 Prediction de consommation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="section-title">📋 Caracteristiques</div>', unsafe_allow_html=True)
            
            cylinders = st.selectbox("Cylindres", [3, 4, 5, 6, 8], index=1)
            displacement = st.number_input("Cylindree (cu in)", 50, 500, 150, 10)
            horsepower = st.number_input("Puissance (hp)", 40, 250, 100, 5)
            weight = st.number_input("Poids (lbs)", 1500, 5500, 3000, 100)
            acceleration = st.number_input("Acceleration (sec)", 8.0, 25.0, 15.0, 0.5, format="%.1f")
            model_year = st.number_input("Annee", 70, 82, 76, 1)
            origin = st.selectbox("Origine", [1, 2, 3], format_func=lambda x: {1: "USA", 2: "Europe", 3: "Asie"}[x])
            
            predict_btn = st.button("🔮 Predire", type="primary", use_container_width=True)
        
        with col2:
            if predict_btn:
                if model is None:
                    st.error("Modele non trouve !")
                else:
                    try:
                        input_data = pd.DataFrame({
                            'cylinders': [cylinders],
                            'displacement': [displacement],
                            'horsepower': [horsepower],
                            'weight': [weight],
                            'acceleration': [acceleration],
                            'model_year': [model_year],
                            'origin': [origin]
                        })
                        
                        prediction_mpg = model.predict(input_data)[0]
                        prediction_l100km = mpg_to_l100km(prediction_mpg)
                        
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#667eea,#764ba2); padding:20px; border-radius:15px; color:white; text-align:center;">
                            <h2 style="margin:0;">📊 Resultat</h2>
                            <div style="font-size:3rem; font-weight:700; margin:10px 0;">{prediction_mpg:.1f} mpg</div>
                            <div style="font-size:1.2rem;">≈ {prediction_l100km:.1f} L/100km</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if prediction_mpg >= 30:
                            category = "🟢 Tres econome"
                            color = "#27ae60"
                        elif prediction_mpg >= 25:
                            category = "🟢 Econome"
                            color = "#2ecc71"
                        elif prediction_mpg >= 20:
                            category = "🟡 Moyenne"
                            color = "#f1c40f"
                        elif prediction_mpg >= 15:
                            category = "🟠 Elevee"
                            color = "#e67e22"
                        else:
                            category = "🔴 Tres elevee"
                            color = "#e74c3c"
                        
                        st.markdown(f"""
                        <div style="background:#f8f9fa; padding:15px; border-radius:10px; margin-top:10px; text-align:center;">
                            <h3 style="color:{color};">{category}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Erreur : {e}")
    
    # ============================================
    # PAGE TRAJET
    # ============================================
    elif st.session_state.page == "Trajet":
        st.markdown("""
        <div class="card">
            <h2>🛣️ Planifier un trajet</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-title">📊 Votre consommation</div>', unsafe_allow_html=True)
            consumption_unit = st.radio("Unite", ["L/100km", "mpg"], index=0)
            
            if consumption_unit == "L/100km":
                consumption = st.number_input("Consommation (L/100km)", 3.0, 30.0, 7.5, 0.5)
            else:
                consumption = st.number_input("Consommation (mpg)", 8.0, 60.0, 31.0, 1.0)
        
        with col2:
            st.markdown('<div class="section-title">🛣️ Details du trajet</div>', unsafe_allow_html=True)
            distance = st.number_input("Distance (km)", 1, 5000, 100, 10)
            fuel_price = st.number_input("Prix carburant (€/L)", 1.0, 3.0, 1.8, 0.1)
            trip_btn = st.button("📊 Calculer", type="primary", use_container_width=True)
        
        if trip_btn:
            unit = 'mpg' if consumption_unit == 'mpg' else 'l100km'
            result = calculate_trip(consumption, unit, distance, fuel_price)
            
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Resultat du trajet</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#667eea,#764ba2); padding:20px; border-radius:15px; color:white; text-align:center;">
                    <div style="font-size:0.9rem; opacity:0.8;">⛽ Carburant</div>
                    <div style="font-size:2.5rem; font-weight:700;">{result['litres_necessaires']:.1f}</div>
                    <div>litres</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#f7971e,#ffd200); padding:20px; border-radius:15px; color:#1a1a2e; text-align:center;">
                    <div style="font-size:0.9rem; opacity:0.8;">💰 Cout total</div>
                    <div style="font-size:2.5rem; font-weight:700;">{result['cout_total']:.2f}</div>
                    <div>euros</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#27ae60,#2ecc71); padding:20px; border-radius:15px; color:white; text-align:center;">
                    <div style="font-size:0.9rem; opacity:0.8;">📏 Autonomie</div>
                    <div style="font-size:2.5rem; font-weight:700;">{result['km_par_litre']:.1f}</div>
                    <div>km par litre</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background:white; border-radius:15px; padding:20px; box-shadow:0 4px 20px rgba(0,0,0,0.08); border:1px solid #e9ecef; margin-top:15px;">
                <h4 style="color:#0066ff;">📋 Details</h4>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                    <div><strong>Distance :</strong> {distance} km</div>
                    <div><strong>Consommation :</strong> {result['consumption_display']}</div>
                    <div><strong>Cout au km :</strong> {result['cout_total']/distance:.3f} €/km</div>
                    <div><strong>CO₂ emis :</strong> {(result['l100km'] * distance / 100 * 2.3):.1f} kg</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# AFFICHAGE PRINCIPAL
# ============================================
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()
    
    # ============================================
    # CHARGEMENT DES DONNÉES POUR L'APPLICATION
    # ============================================
    
    # Charger le fichier
    df = pd.read_csv('AUTOMPG.csv')
    
    # Supprimer la colonne inutile
    df = df.drop('Unnamed: 0', axis=1)
    
    # Supprimer les valeurs manquantes
    df_clean = df.dropna()
    
    print(f"✅ Données chargées : {len(df_clean)} lignes")
    
    # ============================================
    # PIED DE PAGE
    # ============================================
    st.markdown("""
    <div class="footer">
        <p><strong>Systeme de Prediction de consommation de carburant et de voyage</strong> • Cours de Machine Learning • © 2026</p>
        <p><strong><h4>Projet realise par: ASANTE USABWIMANA Raphael et IRUMVA HAKIZIMANA Elisee</h4></strong></p>
    </div>
    """, unsafe_allow_html=True)
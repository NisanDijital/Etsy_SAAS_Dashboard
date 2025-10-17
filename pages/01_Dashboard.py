# pages/01_Dashboard.py (SON HALİ – Tüm AI Özellikler Entegre, Stoksuz)

import streamlit as st
import pandas as pd
import time
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import google.generativeai as genai

# YETKİLENDİRME KONTROLÜ
if 'logged_in' not in st.session_state or st.session_state['logged_in'] != True:
    st.warning("Bu sayfaya erişim yetkiniz yok. Lütfen giriş yapın.")
    time.sleep(0.5) 
    st.switch_page("etsy_dashboard.py")
    st.stop()

# YAPILANDIRMA
SHOP_NAME = "Etsy Ana Otomasyon Dashboard (Stoksuz POD)"
SHOP_ID = st.secrets.get("ETSY_SHOP_ID", "YOUR_SINGLE_SHOP_ID")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YAPISTIR_SENIN_GERCEK_GEMINI_ANAHTARIN")

# Stoksuz JOURNAL_TRENDS
JOURNAL_TRENDS = [
    {'nis': 'Wellness', 'trend': 'Meditasyon Kapakları, pembe lotus motif', 'fiyat': 150, 'marj': 0.5},
    {'nis': 'Travel', 'trend': 'Seyahat Harita Motifli Journal', 'fiyat': 200, 'marj': 0.65},
    {'nis': 'Fitness', 'trend': 'Workout Tracker Kapak, gym ikonlu', 'fiyat': 120, 'marj': 0.4},
    {'nis': 'Productivity', 'trend': 'Goal Setter Minimalist Planner', 'fiyat': 180, 'marj': 0.6},
    {'nis': 'Creative', 'trend': 'Junk Journal Kolajlı Sanatçı Stili', 'fiyat': 160, 'marj': 0.55},
]

# AI BAĞLANTISI
AI_AKTIF = False
model = None
try:
    if GEMINI_API_KEY and GEMINI_API_KEY != "YAPISTIR_SENIN_GERCEK_GEMINI_ANAHTARIN":
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        AI_AKTIF = True
except Exception as e:
    st.error(f"AI Bağlantı Hatası: {e}")

# FONKSİYONLAR
def generate_etsy_seo(product_name, target_audience):
    if not AI_AKTIF or not model:
        return "AI kapalı.", False
    prompt = f"""Etsy SEO için {product_name} - {target_audience}: TITLE: [80 char]\nTAGS: [13 etiket]"""
    try:
        response = model.generate_content(prompt)
        return response.text, True
    except Exception as e:
        return f"Hata: {e}", False

def generate_trend_tahmini(nis_input, ay_input):
    if not AI_AKTIF or not model:
        return "AI kapalı.", False
    prompt = f"""2025 {ay_input} {nis_input} trend tahmini: BÜYÜME: %XX\nALT NİŞLER: [3 tane]\nRAKİP: Düşük\nÖNERİ: [Tema]"""
    try:
        response = model.generate_content(prompt)
        return response.text, True
    except Exception as e:
        return f"Hata: {e}", False

def generate_fiyat_opt(nis_input, maliyet_input, hedef_marg):
    if not AI_AKTIF or not model:
        return "AI kapalı.", False
    prompt = f"""Stoksuz POD {nis_input} fiyat optimizasyonu (maliyet {maliyet_input} TL, marj %{hedef_marg}): ÖNERİLEN FİYAT: XX TL\nRAKİP ARALIĞI: XX-XX\nSATIŞ HACMİ: Orta\nA/B TEST: [Öneri]"""
    try:
        response = model.generate_content(prompt)
        return response.text, True
    except Exception as e:
        return f"Hata: {e}", False

def create_journal_image(nis, trend):
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.text(0.5, 0.9, f"{nis} Journal Kapağı - {trend}", ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(0.5, 0.8, "Stoksuz Dijital/POD Hazır! 🚀", ha='center', va='center', fontsize=12)
    ax.axis('off')
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return img_base64

def simulate_etsy_push(nis, trend, fiyat):
    api_key = st.secrets.get("ETSY_API_KEY", "YOUR_KEY")
    if api_key != "YOUR_KEY":
        url = f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/listings/draft"
        headers = {'x-api-key': api_key, 'Content-Type': 'application/json'}
        data = {'title': f"{nis} Journal - {trend}", 'price': str(fiyat), 'quantity': 999, 'is_digital': True}
        try:
            response = requests.post(url, headers=headers, json=data)
            return {'status': response.status_code, 'id': response.json().get('listing_id', 'Gerçek ID')}
        except:
            return {'status': 500, 'id': 'Hata'}
    return {'status': 200, 'id': f'Simüle ID: {nis}-{int(time.time())}'}

def simulate_pod_order(etsy_id):
    return {'order_id': f'POD-{etsy_id}', 'status': 'Baskılandı & Kargolandı (Stoksuz)', 'takip': f'TR{int(time.time())}789'}

# DASHBOARD UI
st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")
st.title(f"🚀 {SHOP_NAME} - Stoksuz Otomasyon Dashboard")
st.markdown("---")

with st.sidebar:
    st.subheader("Oturum")
    if st.button('🚪 Çıkış Yap'):
        st.session_state['logged_in'] = False
        st.switch_page("etsy_dashboard.py")
    st.markdown("---")
    st.subheader("⚙️ Mağaza Bilgisi")
    st.info(f"Aktif ID: **{SHOP_ID}**")

# POD FULFILLMENT SIMÜLASYONU
st.header("🚚 POD Fulfillment Simülasyonu (Stoksuz Mod)")
if st.button("🧪 Test Sipariş Simüle Et"):
    with st.spinner('Printful stoksuz işliyor...'):
        for trend in JOURNAL_TRENDS:
            etsy_id = simulate_etsy_push(trend['nis'], trend['trend'], trend['fiyat'])
            pod_result = simulate_pod_order(etsy_id['id'])
            st.info(f"{trend['nis']}: {pod_result['status']}, Takip: {pod_result['takip']}")
    st.success("Stoksuz fulfillment tamam! Dijital link/POD hazır.")

st.markdown("---")

# AI SEO ÜRETİCİSİ
st.header("✨ AI SEO Üreticisi")
col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("Ürün Adı", placeholder="Wellness Journal")
    target_audience = st.selectbox("Hedef Kitle", ['Genç, Minimalist', 'Hediye Arayan'])
    if st.button("Üret", type="primary"):
        result, success = generate_etsy_seo(product_name, target_audience)
        if success:
            st.code(result, language='markdown')
        else:
            st.error(result)

st.markdown("---")

# AI TREND TAHMİNİ
st.header("🔮 AI Trend Tahmini")
col3, col4 = st.columns(2)
with col3:
    nis_input = st.text_input("Niş", placeholder="Wellness")
    ay_input = st.selectbox("Ay", ['Ekim 2025', 'Kasım 2025'])
    if st.button("Tahmin Et", type="primary"):
        result, success = generate_trend_tahmini(nis_input, ay_input)
        if success:
            st.code(result, language='markdown')
        else:
            st.error(result)

st.markdown("---")

# AI FİYAT OPTİMİZASYONU
st.header("💰 AI Fiyat Optimizasyonu")
col5, col6 = st.columns(2)
with col5:
    nis_input_price = st.text_input("Niş", placeholder="Fitness")
    maliyet_input = st.number_input("Maliyet (TL)", value=80.0)
    hedef_marg = st.slider("Marj %", 30.0, 70.0, 50.0)
    if st.button("Optimize Et", type="primary"):
        result, success = generate_fiyat_opt(nis_input_price, maliyet_input, hedef_marg)
        if success:
            st.code(result, language='markdown')
        else:
            st.error(result)

st.markdown("---")

# AI ÖZELLİK YÖNETİCİSİ
st.header("🤖 AI Özellik Yöneticisi")
ai_komut = st.text_area("Komut Gir", placeholder="Yeni stok tahmini ekle")
if st.button("Ekle", type="primary") and ai_komut:
    prompt = f"""Streamlit uzmanısın. Stoksuz Etsy dashboard'una {ai_komut}: KOD: [Streamlit kodu]"""
    result, success = model.generate_content(prompt) if model else ("AI kapalı.", False)
    if success:
        st.code(result.text, language='python')
        if st.button("Uygula"):
            try:
                exec(result.text)
                st.success("Eklendi!")
                st.rerun()
            except Exception as e:
                st.error(f"Hata: {e}")

st.markdown("---")

# KAR RAPORU
st.header("💰 Kar Dağılımı Raporu (Stoksuz)")
kar_df = pd.DataFrame(JOURNAL_TRENDS).copy()
kar_df['kar'] = kar_df['fiyat'] * kar_df['marj']
st.bar_chart(kar_df.set_index('nis')['kar'])
st.metric("Toplam Tahmini Kar", f"{kar_df['kar'].sum():.0f} TL")

st.markdown("---")
st.caption("🔄 Stoksuz Dashboard otomatik yenileniyor... Son güncelleme: " + time.strftime("%H:%M:%S, %d/%m/%Y"))

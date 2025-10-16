# pages/01_Dashboard.py (UYGULAMA İÇERİĞİ)

import streamlit as st
import pandas as pd
import time
import requests
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
from google import genai 

# --- YETKİLENDİRME KONTROLÜ (ÇOK ÖNEMLİ: Sayfayı korur) ---
if 'logged_in' not in st.session_state or st.session_state['logged_in'] != True:
    st.warning("Bu sayfaya erişim yetkiniz yok. Lütfen giriş yapın.")
    time.sleep(0.5) 
    st.switch_page("etsy_dashboard.py")
    st.stop()
# --- KONTROL BAŞARILI, UYGULAMAYI YÜKLE ---


# --- YAPILANDIRMA VE VERİLER ---
SHOP_NAME = "Etsy Ana Otomasyon Dashboard"
SHOP_ID = "YOUR_SINGLE_SHOP_ID"
# DİKKAT: API anahtarlarınızı buraya değil, st.secrets'a yazmalısınız.
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YAPISTIR_SENIN_GERCEK_GEMINI_ANAHTARIN")

# Simülasyon Verileri
JOURNAL_TRENDS = [
    {'nis': 'Wellness', 'trend': 'Meditasyon Kapakları', 'fiyat': 150, 'marj': 0.5, 'stok': 5},
    {'nis': 'Travel', 'trend': 'Seyahat Harita Motifli', 'fiyat': 200, 'marj': 0.65, 'stok': 3},
]

# --- YAPAY ZEKA BAĞLANTISI ---
try:
    if GEMINI_API_KEY and GEMINI_API_KEY != "YAPISTIR_SENIN_GERCEK_GEMINI_ANAHTARIN":
        client = genai.Client(api_key=GEMINI_API_KEY)
        model = 'gemini-2.5-flash'
        AI_AKTIF = True
    else:
        AI_AKTIF = False
except Exception:
    AI_AKTIF = False

# Yapay Zeka SEO Üretici Fonksiyonu
def generate_etsy_seo(product_name, target_audience, client):
    if not AI_AKTIF: return "API Anahtarı ayarlanmadığı için Yapay Zeka kapalı.", False

    prompt = f"""Etsy SEO uzmanısın. {product_name} ürünü için {target_audience} hedef kitlesine yönelik: 
    1. Ürünün ana başlığını (Max 80 karakter, 3-5 anahtar kelime)
    2. 13 adet popüler Etsy etiketini (Virgülle ayrılmış)
    İngilizce olarak üret. Format: TITLE: [Başlık metni]\nTAGS: [etiket1, etiket2, ...]"""

    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text, True
    except Exception as e:
        return f"Yapay zeka yanıt hatası: {e}", False


# --- STREAMLIT DASHBOARD İÇERİĞİ ---
st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

st.title(f"🚀 {SHOP_NAME} - Otomasyon Dashboard")
st.markdown("---")

# Sol kenar çubuğu (Çıkış Butonu)
with st.sidebar:
    st.subheader("Oturum")
    if st.button('🚪 Çıkış Yap'):
        st.session_state['logged_in'] = False
        st.switch_page("etsy_dashboard.py")
    st.markdown("---")
    st.subheader("⚙️ Mağaza Bilgisi")
    st.info(f"Aktif ID: **{SHOP_ID}**")


# 1. KRİTİK STOK DURUMU
trends_df = pd.DataFrame(JOURNAL_TRENDS)
st.header("⚠️ Kritik Stok Durumu")
low_stock = trends_df[trends_df['stok'] < 10].sort_values(by='stok')

if not low_stock.empty:
    st.error(f"🚨 **{len(low_stock)} adet** ürün kritik stok seviyesinin altında.")
    st.dataframe(low_stock[['nis', 'trend', 'stok']], hide_index=True)
else:
    st.success("Tüm ürünlerde stok durumu güvende.")

st.markdown("---")

# 2. YAPAY ZEKA SEO ÜRETİCİSİ
st.header("✨ Yapay Zeka Destekli SEO Üreticisi")

if not AI_AKTIF:
    st.error("🚨 UYARI: Gemini API anahtarı tanımlanmadığı için bu özellik kapalı. Anahtarınızı ayarlayın.")

else:
    col_input, col_output = st.columns([1.5, 2])
    with col_input:
        product_name = st.text_input("Ürün Temel Adı", max_chars=50)
        target_audience = st.selectbox("Hedef Kitle", ['Genç, Minimalist', 'Hediye Arayan', 'Çevreye Duyarlı'])
        generate_button = st.button("🚀 Başlık ve Etiket Üret", type="primary")

    if generate_button and product_name:
        with st.spinner('Gemini en iyi kelimeleri araştırıyor...'):
            result_text, success = generate_etsy_seo(product_name, target_audience, client)

        with col_output:
            if success:
                st.subheader("Üretilen SEO Sonuçları")
                st.code(result_text, language='markdown')
            else:
                st.error(result_text)
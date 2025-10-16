# etsy_dashboard.py (ANA GİRİŞ SAYFASI)

import streamlit as st
import time
from streamlit_authenticator import Hasher 

# --- GÜVENLİK VE GİRİŞ YAPILANDIRMASI ---
# Şifreler hash'lenmiştir. (Kolayca 'sifre123' şifresiyle giriş yapabilirsiniz)
USERNAME = "admin"
PASSWORD_HASH = Hasher(['sifre123']).generate()[0] # Bu, 'sifre123' şifresinin şifreli halidir.
# ---

st.set_page_config(page_title="Giriş", page_icon="🔑", layout="centered")

st.title("🔑 EtsyJournalDash Giriş")
st.markdown("---")

# Giriş Formu
with st.form("login_form"):
    user_input = st.text_input("Kullanıcı Adı")
    password_input = st.text_input("Şifre", type="password")
    submitted = st.form_submit_button("Giriş Yap")

# Giriş Kontrolü
if submitted:
    if user_input == USERNAME:
        # Girilen şifrenin hash'ini alıp, kayıtlı hash ile karşılaştır
        if Hasher([password_input]).check_hashes(PASSWORD_HASH, [password_input])[0]:
            
            st.success("Giriş başarılı! Dashboard'a yönlendiriliyorsunuz...")
            st.session_state['logged_in'] = True  # Oturum durumunu kaydet
            time.sleep(0.5)
            
            # Dashboard sayfasına yönlendir (pages/01_Dashboard.py)
            st.switch_page("pages/01_Dashboard.py") 
            
        else:
            st.error("Hatalı şifre.")
    else:
        st.error("Hatalı kullanıcı adı.")
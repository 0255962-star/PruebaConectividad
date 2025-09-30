import streamlit as st

st.set_page_config(page_title="Test Google Sheets", layout="centered")
st.title("Test de conexión a Google Sheets (paso a paso)")

# 1) SECRETS
try:
    st.write("Paso 1: leyendo Secrets…")
    SHEET_ID = st.secrets["SHEET_ID"]
    svc = st.secrets["gcp_service_account"]
    st.success("✅ Paso 1 OK: Secrets cargados.")
    st.write(f"- SHEET_ID len: {len(SHEET_ID)}")
    st.write(f"- Service account: {svc.get('client_email','(sin client_email)')}")
except Exception as e:
    st.error("❌ Paso 1 FALLÓ: No pude leer los Secrets. Revisa formato TOML.")
    st.exception(e)
    st.stop()

# 2) CONEXIÓN A SHEETS (forma estándar con gspread)
with st.status("Paso 2: Conectando a Google Sheets…", expanded=True) as s:
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = Credentials.from_service_account_info(dict(svc), scopes=SCOPES)
        gc = gspread.authorize(creds)

        st.write("2.1 Abriendo el Sheet por ID…")
        sh = gc.open_by_key(SHEET_ID)

        st.write("2.2 Leyendo título…")
        st.success(f"✅ Conexión OK. Documento: **{sh.title}**")
        s.update(label="Paso 2 completo", state="complete")
    except Exception as e:
        s.update(label="Paso 2 FALLÓ", state="error")
        st.error("❌ Error conectando a Google Sheets.")
        st.caption("Verifica: compartir el Sheet con el client_email, SHEET_ID correcto y APIs habilitadas.")
        st.exception(e)
        st.stop()

st.success("✅ Test completado. Ya podemos volver al app completo cuando confirmes esto.")


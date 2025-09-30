import streamlit as st

st.set_page_config(page_title="Test Sheets", layout="centered")
st.title("Test de conexión a Google Sheets (paso a paso)")

# 1) Leer Secrets
try:
    SHEET_ID = st.secrets["SHEET_ID"]
    svc = st.secrets["gcp_service_account"]
    st.success("✅ Paso 1 OK: Secrets cargados.")
    st.write(f"- SHEET_ID len: {len(SHEET_ID)}")
    st.write(f"- Service account: {svc.get('client_email','(sin client_email)')}")
except Exception as e:
    st.error("❌ Paso 1 FALLÓ: no pude leer los Secrets (revisa formato TOML).")
    st.exception(e)
    st.stop()

# 2) Autenticación y apertura del Sheet
with st.status("Paso 2: Conectando a Google Sheets…", expanded=True) as s:
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import AuthorizedSession

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = Credentials.from_service_account_info(dict(svc), scopes=SCOPES)
        # Sesión con timeout corto para evitar “cargas eternas”
        authed = AuthorizedSession(creds)
        authed.configure(timeout=10)  # segundos
        gc = gspread.Client(auth=creds, session=authed)

        sh = gc.open_by_key(SHEET_ID)
        st.write("✅ Conexión OK.")
        st.write(f"Documento: **{sh.title}**")
        s.update(label="Paso 2 completo", state="complete")
    except Exception as e:
        s.update(label="Paso 2 FALLÓ", state="error")
        st.error("❌ Error conectando a Google Sheets.")
        st.caption("Verifica: compartir el Sheet con el client_email, SHEET_ID correcto, APIs habilitadas.")
        st.exception(e)
        st.stop()

st.success("✅ Test completado. Ya puedes reemplazar este archivo por tu app completa cuando quieras.")

# 2) CONEXIÓN A SHEETS (forma estándar con gspread)
with st.status("Paso 2: Conectando a Google Sheets…", expanded=True) as s:
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # Credenciales desde secrets
        creds = Credentials.from_service_account_info(dict(svc), scopes=SCOPES)

        # Cliente gspread
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


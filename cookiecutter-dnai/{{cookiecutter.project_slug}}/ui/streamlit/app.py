import os
import requests
import streamlit as st

st.set_page_config(page_title="{{ cookiecutter.project_name }}", page_icon="🤖", layout="centered")

st.title("{{ cookiecutter.project_name }} — Streamlit")
st.caption("Talk to the backend /chat endpoint")

api = st.text_input("API base URL", value=os.getenv("API_BASE_URL", ""), placeholder="https://<api-id>.execute-api.<region>.amazonaws.com/prod")
auth = st.text_input("Authorization header (optional)", type="default")
q = st.text_area("Prompt", height=140, placeholder="Ask something...")

if st.button("Send"):
    if not api:
        st.error("Set API base URL")
    else:
        try:
            url = api.rstrip("/") + "/chat"
            headers = {"Content-Type": "application/json"}
            if auth:
                headers["Authorization"] = auth
            r = requests.post(url, json={"q": q}, headers=headers, timeout=60)
            st.code(r.text, language="json")
        except Exception as e:
            st.exception(e)


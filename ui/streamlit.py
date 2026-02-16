import streamlit as st 
import requests

API = st.secerets.get("API_URL","http://localhost:80000")
st.title(" UK Transaction Categorization")


desc = st.text_input("Transaction description","contactless tesco milk <ref>")
amount = st.number_input("Amount", value=12.3)

if st.button("Predict"):
    r = requests.post(f"{API}/predict", json={"description":desc, "amount":amount})
    if r.ok:
        out = r.json()
        st.success(f"Category : {out['category']}")
        st.write(f"Confidence : {out['confidence']:.2f}")
    else:
        st.error(r.text)

    
import streamlit as st
from streamlit_ketcher import st_ketcher
import pandas as pd
import numpy as np
import requests
import joblib
import io

from rdkit import Chem, DataStructs

from PIL import Image

# =========================================================
# Author : Dr. Sk. Abdul Amin
# =========================================================
# Streamlit
#logo_url = "https://raw.githubusercontent.com/Amincheminform/phKMOi_v1/main/phKMOi_v1_logo.jpg"
logo_url = "https://github.com/Amincheminfom/Amincheminfom/raw/main/Cheminform_logo.jpg"

st.set_page_config(
    page_title="pCDK1i_v1.0: predictor of CDK1 inhibitors",
    layout="wide",
    page_icon=logo_url
)

st.markdown("""
<style>
section[data-testid="stSidebar"] label {
    font-size: 20px !important;
    font-weight: bold !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)
# --------- Utility Functions ---------

def mol_to_array(mol, size=(300, 300)):
    try:
        from rdkit.Chem.Draw import rdMolDraw2D  # ✅ import here only
        drawer = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        img_data = drawer.GetDrawingText()
        return Image.open(io.BytesIO(img_data))
    except Exception as e:
        return None

def pred_label(pred):
    return "### **Active**" if pred == 1 else "### **Inactive**"

# --------- Load Model ---------

@st.cache_resource
def load_model():
    url = "https://raw.githubusercontent.com/Amincheminfom/pCDK1i_v1/main/random_forest_model.pkl"
    response = requests.get(url)

    if response.status_code == 200:
        with open("model.pkl", "wb") as f:
            f.write(response.content)
    else:
        st.error("Model download failed!")
        return None

    return joblib.load("model.pkl")

#model = load_model()
model = load_model()

if model is None:
    st.stop()

# --------- Fingerprint Generator ---------

fpg = rdFingerprintGenerator.GetMorganGenerator(radius=3, fpSize=2048)

# --------- Prediction Function ---------

def predict_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None, None

    fp = fpg.GetFingerprint(mol)
    arr = np.zeros((2048,), dtype=int)
    DataStructs.ConvertToNumpyArray(fp, arr)

    fp = arr.reshape(1, -1)

    pred = model.predict(fp)[0]
    prob = model.predict_proba(fp)[0][1]

    return pred, prob

# --------- UI ---------

st.title("pCDK1i_v1.0")

with st.expander("About", expanded=True):
    st.write("""
    **pCDK1i_v1.0** predicts whether a molecule is CDK1 **Active** or **Inactive**
    using a machine learning model.
    """)

st.sidebar.image(logo_url)
st.sidebar.success("Thank you for using pCDK1i_v1.0")

# --------- Mode Selection ---------

mode = st.sidebar.radio(
    "Select Prediction Mode",
    ["Select...", "Single Molecule Prediction", "Batch Prediction"]
)

if mode == "Select...":
    st.info("Please select a prediction mode from the sidebar.")
    st.stop()

if mode == "Single Molecule Prediction":
    st.header("Single Molecule Prediction")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Draw Molecule")
        smile_code = st_ketcher()

    with col2:
        st.markdown("### SMILES Input")

        smiles_input = st.text_input(
            "Enter or edit SMILES:",
            value=smile_code if smile_code else ""
        )

        if smiles_input:

            mol = Chem.MolFromSmiles(smiles_input)

            if mol:
                st.markdown("---")
                st.subheader("Results")

                #prediction, probability = predict_smiles(smiles_input)
                with st.spinner("Predicting..."):
                    prediction, probability = predict_smiles(smiles_input)

                if prediction is None:
                    st.error("Prediction failed!")
                else:
                    label = "Active" if prediction == 1 else "Inactive"

                    # 🔹 SAME ROW layout
                    #res_col1, res_col2 = st.columns([1, 1])
                    res_col1, res_col2 = st.columns([1, 1.2])

                    with res_col1:
                        mol_img = mol_to_array(mol)
                        if mol_img:
                            st.image(mol_img, use_container_width=True)
                        else:
                            st.warning("⚠️ Molecule visualization not supported in this environment.")
                        #st.image(mol_img, caption="Query Molecule", width=220)
                        #st.image(mol_img, caption="Query Molecule", use_container_width=True)

                    with res_col2:
                        st.markdown(
                            f"""
                            <div style="
                                font-size:42px;
                                font-weight:700;
                                text-align:center;
                                color:{'green' if prediction == 1 else 'red'};
                            ">
                            {label}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if probability is not None:
                            st.markdown(
                                f"""
                                <div style="
                                    text-align:center;
                                    font-size:18px;
                                    margin-top:10px;
                                ">
                                <b>Probability (Active)</b><br>
                                {probability:.3f}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                """
                                <div style="text-align:center; font-size:18px; margin-top:10px;">
                                <b>Probability (Active)</b><br>
                                NA
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

            else:
                st.error("Invalid SMILES!")

# =========================================================
# 🔹 BATCH MODE
# =========================================================

elif mode == "Batch Prediction":

    st.header("Batch Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file with 'Smiles' column",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        # Read file
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success(f"File loaded successfully! Total molecules: {len(df)}")

        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()

        # Check column
        if "Smiles" not in df.columns:
            st.error("File must contain a 'Smiles' column")
            st.stop()

        # Run predictions
        predictions = []
        probabilities = []
        labels = []

        with st.spinner("Running predictions..."):
            for smi in df["Smiles"]:
                pred, prob = predict_smiles(smi)

                if pred is None:
                    predictions.append(None)
                    probabilities.append(None)
                    labels.append("Invalid SMILES")
                else:
                    predictions.append(pred)
                    probabilities.append(prob)
                    labels.append("Active" if pred == 1 else "Inactive")

        # Add results
        df["Prediction"] = predictions
        df["Probability"] = probabilities
        df["Label"] = labels

        st.success("Batch prediction completed!")

        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Results",
            data=csv,
            file_name="prediction_results.csv",
            mime="text/csv"
        )

# =========================================================
# 🔹 CONTACT
# =========================================================

with st.expander("Contact"):
    st.write("""
    **Dr. Sk. Abdul Amin**  
    📧 pharmacist.amin@gmail.com  
    🔗 https://github.com/Amincheminform
    """)

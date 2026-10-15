import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")
class_model = joblib.load("degree_class_model.pkl")

programs = {
    "BCH": "Biochemistry",
    "BLD": "Building Technology",
    "CEN": "Computer Engineering",
    "CHE": "Chemical Engineering",
    "CHM": "Industrial Chemistry",
    "CIS": "Computer Science",
    "CVE": "Civil Engineering",
    "EEE": "Electrical and Electronics Engineering",
    "ICE": "Information and Communication Engineering",
    "MAT": "Mathematics",
    "MCB": "Microbiology",
    "MCE": "Mechanical Engineering",
    "MIS": "Management and Information System",
    "PET": "Petroleum Engineering",
    "PHYE": "Industrial Physics: Electronics and IT Applications",
    "PHYG": "Industrial Physics: Applied Geophysics",
    "PHYR": "Industrial Physics: Renewable Energy",
}

st.title("Final CGPA Predictor")
st.write(
    "Enter a student's first-year result to get an estimate of their final CGPA. "
    "The model was trained on graduates of Landmark University (2010 to 2014)."
)
st.warning("All grades must be on a 5.0 scale. Do not enter grades from a 4.0 scale.")

cgpa100 = st.number_input("First-year CGPA (0 to 5)", 0.0, 5.0, 3.5, 0.01)
secondary = st.number_input("Secondary school grade (0 to 5)", 0.0, 5.0, 3.5, 0.01)
code = st.selectbox("Program of study", list(programs), format_func=lambda c: programs[c])

if st.button("Predict"):
    row = pd.DataFrame(0.0, index=[0], columns=columns)
    row["CGPA100"] = cgpa100
    row["SecondaryGrade"] = secondary
    row["Prog Code_" + code] = 1.0

    guess = model.predict(row)[0]
    guess = min(max(guess, 0.0), 5.0)

    chances = class_model.predict_proba(row)[0]
    by_class = dict(zip(class_model.classes_, chances))
    best = max(by_class, key=by_class.get)
    order = ["First", "Second Upper", "Second Lower", "Third"]

    st.success(f"Estimated final CGPA: {guess:.2f}")
    st.info(f"Most likely degree class: {best}")

    table = pd.DataFrame({
        "Degree class": order,
        "Chance (%)": [round(by_class[c] * 100) for c in order],
    })
    st.table(table.set_index("Degree class"))

    st.caption(
        "These are estimates. The CGPA guess is off by about 0.31 points on average. "
        "The degree class was right for about 72% of students in testing, "
        "but the model finds only about 1 in 5 Third Class students."
    )

import os
import streamlit as st
from pymongo import MongoClient

# --- MongoDB Connection ---
client = MongoClient(os.environ["MONGODB_URI"])
db = client.get_database("Omnivia")
responses_collection = db.get_collection("responses")

def create_survey_question():
    """Creates a survey question section with question type selection and conditional logic."""
    st.subheader("Create Survey Question")
    question_type = st.selectbox("Select Question Type", ["Multiple Choice", "Text", "Rating Scale", "Dropdown"])
    question_text = st.text_input("Enter Question Text:")

    options = []
    if question_type in ["Multiple Choice", "Dropdown"]:
        num_options = st.number_input("Number of Options", min_value=2, max_value=10, value=4)
        for i in range(int(num_options)):
            options.append(st.text_input(f"Option {i+1}:"))

    # Conditional Logic (Dynamically Show/Hide Questions)
    condition_enabled = st.checkbox("Enable Conditional Logic")
    if condition_enabled:
        target_question = st.selectbox("Target Question", options, index=0)
        condition_value = st.text_input("Condition Value (e.g., Option A)")
        st.write(f"**Conditional Logic:**  If the answer to the previous question is '{condition_value}', then the following question will be shown:")
        # ... (Implement logic to show/hide questions dynamically) ...

    # Store the created question in the database
    if st.button("Add Question"):
        question_data = {
            "type": question_type,
            "text": question_text,
            "options": options if options else None,
            "condition": {
                "enabled": condition_enabled,
                "target_question": target_question if condition_enabled else None,
                "value": condition_value if condition_enabled else None
            }
        }
        responses_collection.insert_one(question_data)  # Insert the question to the MongoDB collection
        st.success("Question added successfully.")
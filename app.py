import streamlit as st
from shl_recommender import recommend_assessments, print_results

st.set_page_config(page_title="SHL Assessment Recommendation Engine", layout="centered")

st.title("🔍 SHL Assessment Recommendation Engine")

st.write("Enter job details below to get recommended assessments:")

job_title = st.text_input("Job Title", placeholder="e.g., Graduate Software Engineer")

seniority = st.selectbox("Seniority Level", ["entry", "mid", "senior", "leadership"])

use_case = st.selectbox("Use Case", ["hiring_screening", "development", "talent_review"])

if st.button("Get Recommendations"):
    results = recommend_assessments(job_title, seniority, use_case)
    st.subheader("Recommended Assessments")

    if not results:
        st.write("No matching recommendations.")
    else:
        for score, a in results:
            st.markdown(f"### **{a['name']}**  (Score: {score})")
            st.write(f"**Category:** {a['category']}")
            st.write(f"**Best for:** {', '.join(a['best_for_roles'])}")
            st.write(f"**Levels:** {', '.join(a['level'])}")
            st.write(f"**Use cases:** {', '.join(a['use_cases'])}")
            st.write(f"**Duration:** {a['duration_min']} minutes")
            st.write(f"**Description:** {a['description']}")
            st.write("---")
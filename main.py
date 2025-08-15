import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


# --- Page Config ---
st.set_page_config(
    page_title="Course Advisor - OdumareTech",
    page_icon="🎓",
    layout="centered",
)

# --- Custom CSS Styling (matching OdumareTech theme) ---
st.markdown("""
<style>
/* Page background */
body {
    background-color: #F4F7FA;  /* Light gray background */
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #102B3F;  /* Dark text for readability */
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #102B3F;
    font-weight: 600;
}

/* Uniform input and dropdown styling */
textarea, input[type="text"], select {
    background-color: #FFFFFF !important; /* White background */
    color: #102B3F !important;            /* Dark text */
    border: 2px solid #F8D64E !important; /* Gold accent border */
    border-radius: 8px;
    padding: 10px;
    font-size: 16px;
    width: 100%;
}

/* Dropdown options styling */
select option {
    background-color: #FFFFFF !important;
    color: #102B3F !important;
}

/* Recommendation card */
.recommendation-card {
    background-color: #FFFFFF;
    border: 2px solid #F8D64E;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton>button {
    background-color: #F8D64E;
    color: #102B3F;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #e6c640;
    color: #102B3F;
}
</style>
""", unsafe_allow_html=True)

# --- Load PDF once ---
@st.cache_resource
def load_course_data():
    loader = PyPDFLoader("courses/detailed_courses.pdf")
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])

course_text = load_course_data()

# --- Prompt Template ---
template = """
You are a course advisor. Based on the student's preferences, recommend the most suitable course from the list below.

{course_data}

Student preferences:
- Interest: {interest}
- Goal: {goal}
- Coding experience: {experience}

Recommend the best course with a short explanation in a professional, clear, and friendly tone.
"""
prompt_template = PromptTemplate.from_template(template)

# --- Streamlit UI ---
st.title("🎓 OdumareTech Course Advisor")
st.write(
    "Get the **best course recommendation** based on your interests, goals, and experience level. "
    "Our AI advisor helps you pick courses tailored just for you."
)

with st.form("course_form"):
    interest = st.text_input("What is your area of interest?")
    
    goal = st.selectbox(
        "What is your main goal for taking a course?",
        ["Learn a skill for a job", "Learn for school", "Not sure yet"]
    )
    
    experience = st.selectbox(
        "What is your coding experience level?",
        ["Beginner", "Intermediate", "Advanced"]
    )
    
    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    if not interest:
        st.error("Please fill in your area of interest.")
    else:
        with st.spinner("Thinking... 🤔"):
            llm = ChatOpenAI(model_name="gpt-3.5-turbo")
            prompt = prompt_template.format(
                course_data=course_text,
                interest=interest,
                goal=goal,
                experience=experience
            )
            try:
                response = llm.invoke(prompt)
                st.markdown(f"""
                <div class="recommendation-card">
                    <h3>📚 Recommended Course</h3>
                    <p>{response.content}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

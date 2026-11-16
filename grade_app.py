
import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f5ff, #f9f5ff);
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #263b70;
        text-align: center;
        padding: 15px;
    }

    .sub-title {
        text-align: center;
        color: #687594;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #344675;
        font-size: 23px;
        font-weight: 700;
        margin-top: 20px;
    }

    div.stButton > button {
        background-color: #536dce;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #354fa8;
        color: white;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(50, 70, 120, 0.08);
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "students" not in st.session_state:
    st.session_state.students = []


# ---------------- GRADING FUNCTION ----------------
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🎓 Student Grade Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Manage student marks and monitor class performance</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- ADD STUDENT FORM ----------------
st.markdown('<div class="section-title">➕ Add New Student</div>',
            unsafe_allow_html=True)

with st.form("add_student", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name", placeholder="Enter student name")

    with col2:
        mark = st.number_input(
            "Student Mark",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

    submitted = st.form_submit_button("Add Student")

    if submitted:
        if not name.strip():
            st.error("Please enter the student's name.")
        else:
            student = {
                "Name": name.strip(),
                "Mark": int(mark),
                "Grade": get_grade(mark)
            }

            st.session_state.students.append(student)

            st.success(f"Student {name.strip()} added successfully!")


st.divider()


# ---------------- STUDENT TABLE ----------------
st.markdown('<div class="section-title">📋 Student Records</div>',
            unsafe_allow_html=True)

if st.session_state.students:

    st.dataframe(
        st.session_state.students,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- CLASS CALCULATIONS ----------------
    marks = [student["Mark"] for student in st.session_state.students]

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)
    total = len(marks)

    # ---------------- METRICS ----------------
    st.markdown(
        '<div class="section-title">📊 Class Performance</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Marks", f"{average:.1f}")
    col2.metric("Highest Marks", highest)
    col3.metric("Lowest Marks", lowest)
    col4.metric("Total Students", total)

else:
    st.info("No students added yet. Add your first student above!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Marks", "—")
    col2.metric("Highest Marks", "—")
    col3.metric("Lowest Marks", "—")


# ---------------- FOOTER ----------------
st.divider()

st.caption("Student Grade Manager | Built with Python and Streamlit")

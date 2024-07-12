import streamlit as st
import importlib

exercise_scripts = {
    "Bicep rod curls": "BicepRodCurl.py",
    "Leg extensions": "leg extensions.py",
    "Hammer curls": "Hammer curls.py",
    "Side raises": "Side raises.py",
    "Left dumbbell rows": "dumbbell rows left.py",
    "Right dumbbell rows": "dumbbell rows right.py"
}


def main():
    st.title("GymWallah")

    page = st.sidebar.selectbox("Select a Page", ["Welcome", "Exercise"])

    if page == "Welcome":
        st.header("Welcome to GymWallah")
        st.write("Caution : Place the camera in front of body, at least two meters away such that whole body"
                 "fits in frame.")
        st.write("Note: Do press 'q' (lowercase) button on the keyboard in order to close the webcam window after"
                 " using it.")
        st.write("Select an exercise to start tracking your reps:")

        for exercise in exercise_scripts.keys():
            if st.button(exercise):
                st.session_state["selected_exercise"] = exercise
                st.rerun()

    elif page == "Exercise":
        if "selected_exercise" in st.session_state:
            exercise = st.session_state["selected_exercise"]
            st.header(exercise)
            run_exercise(exercise)
        else:
            st.write("Please select an exercise from the Welcome page.")


def run_exercise(exercise_name):
    script_name = exercise_scripts[exercise_name]
    module = importlib.import_module(script_name.replace('.py', ''))
    module.main()


if __name__ == "__main__":
    main()

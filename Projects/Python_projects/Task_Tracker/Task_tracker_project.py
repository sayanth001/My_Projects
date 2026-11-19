import datetime
import streamlit as st


class Task:
    def __init__(self, task_id: int, title, discription):
        self.id = task_id
        self.title = title
        self.discription = discription
        self.status = "Task Not Completed ⌛︎"
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_completed(self):
        self.status = "Task Completed ✓"

    def get_details(self):
        return (
            f"**Task ID:** {self.id} | **Status:** {self.status}\n\n"
            f"**Title:** {self.title}\n\n"
            f"**Description:** {self.discription}\n\n"
            f"**Creation Time:** {self.created_at}"
        )


def main():
    st.set_page_config(page_title="Task Tracker", page_icon="📝", layout="centered")

    # Inject CSS for 5% Sky Blue Glassy background & Dark Green dynamic accents
    st.markdown(
        """
        <style>
        /* CSS Variables adapt dynamically based on dark/light mode */
        :root {
            --dark-green-primary: #1e4620;
            --dark-green-hover: #2d6a30;
            --dark-green-text: #ffffff;
            --dark-green-bg: #e8f5e9;
            --glass-bg: rgba(135, 206, 235, 0.05); /* 5% Sky Blue Tint */
            --glass-border: rgba(135, 206, 235, 0.15);
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --dark-green-primary: #2e7d32;
                --dark-green-hover: #388e3c;
                --dark-green-text: #ffffff;
                --dark-green-bg: #1b381e;
                --glass-bg: rgba(135, 206, 235, 0.05); /* 5% Sky Blue Tint for Dark Mode */
                --glass-border: rgba(255, 255, 255, 0.1);
            }
        }

        /* Target Streamlit Main App Container for Sky Blue Glassy Effect */
        .stApp {
            background-color: var(--glass-bg) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        /* Subtle glassy border and card background for main form block */
        div[data-testid="stForm"], div[data-testid="stExpander"] {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        /* Top Menu & Button Styling */
        div.stButton > button:first-child {
            background-color: var(--dark-green-primary) !important;
            color: var(--dark-green-text) !important;
            border: none !important;
            border-radius: 8px !important;
        }
        
        div.stButton > button:first-child:hover {
            background-color: var(--dark-green-hover) !important;
        }

        /* Custom top nav bar radio menu styling */
        div[data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        
        /* Form Submit Button Theme */
        button[kind="primary"], button[data-testid="baseButton-secondaryFormSubmit"] {
            background-color: var(--dark-green-primary) !important;
            color: var(--dark-green-text) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🗒 Task Tracker")
    st.write("Manage your tasks efficiently with this Streamlit application.")

    # Initialize session state for task tracker persistence
    if "tasks" not in st.session_state:
        st.session_state.tasks = {}
    if "next_id" not in st.session_state:
        st.session_state.next_id = 1

    # Top Area Menu Bar
    menu = ["Add Task", "View All Tasks", "Mark as Complete", "Delete Task"]
    
    # Render navigation as top-level radio pills horizontally
    choice = st.radio(
        "Navigation",
        menu,
        horizontal=True,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([3, 1])
    with col2:
        st.info(f"Total Tasks: {len(st.session_state.tasks)}")

    st.markdown("---")

    # 1. Add Task
    if choice == "Add Task":
        st.subheader("✚ Add a New Task")
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("Task Title").strip()
            description = st.text_area("Task Description").strip()
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if title:
                    task_obj = Task(st.session_state.next_id, title, description)
                    st.session_state.tasks[st.session_state.next_id] = task_obj
                    st.success(
                        f"Task '{title}' added successfully with Task ID {st.session_state.next_id}."
                    )
                    st.session_state.next_id += 1
                else:
                    st.error("Error: Title cannot be empty.")

    # 2. View All Tasks
    elif choice == "View All Tasks":
        st.subheader("⫶☰ All Tasks")
        if not st.session_state.tasks:
            st.info("No tasks found!")
        else:
            for task_id, t in st.session_state.tasks.items():
                with st.container():
                    st.markdown(t.get_details())
                    st.markdown("---")

    # 3. Mark as Complete
    elif choice == "Mark as Complete":
        st.subheader("☑ Mark Task as Complete")
        if not st.session_state.tasks:
            st.info("No tasks available to complete.")
        else:
            task_ids = list(st.session_state.tasks.keys())
            selected_id = st.selectbox(
                "Select Task ID to Complete",
                task_ids,
                format_func=lambda x: f"ID {x}: {st.session_state.tasks[x].title}",
            )

            if st.button("Mark as Complete"):
                task_obj = st.session_state.tasks.get(selected_id)
                if task_obj:
                    task_obj.mark_completed()
                    current_time = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    st.success(
                        f"Task ID {selected_id} marked as Completed on {current_time}."
                    )
                else:
                    st.error(f"Error: Task ID {selected_id} not found.")

    # 4. Delete Task
    elif choice == "Delete Task":
        st.subheader("🗑 Delete Task")
        if not st.session_state.tasks:
            st.info("No tasks available to delete.")
        else:
            task_ids = list(st.session_state.tasks.keys())
            selected_id = st.selectbox(
                "Select Task ID to Delete",
                task_ids,
                format_func=lambda x: f"ID {x}: {st.session_state.tasks[x].title}",
            )

            if st.button("Delete Task"):
                if selected_id in st.session_state.tasks:
                    removed_task = st.session_state.tasks.pop(selected_id)
                    st.success(f"Task '{removed_task.title}' deleted successfully.")
                    st.rerun()
                else:
                    st.error(f"Error: Task ID {selected_id} not found.")


if __name__ == "__main__":
    main()
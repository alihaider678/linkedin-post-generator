import streamlit as st
from post_generator import generate_post
import sqlite3

# Options for length, language, and tone
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = ["Professional", "Casual", "Friendly"]

# Custom CSS styling for Streamlit app
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Overall App Styling */
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to right, #f8f9fa, #ffffff);
        }

        /* Title Styling */
        .title {
            color: #2E86C1;
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }

        /* Subheader Styling */
        .subheader {
            color: #1F618D;
            font-size: 1.5em;
            margin-bottom: 20px;
        }

        /* Chatbot Section */
        .chatbot-section {
            background-color: #EAF2F8;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
        }

        /* Generated and Refined Posts */
        .post-box {
            background-color: #F8F9F9;
            border-left: 5px solid #2ECC71;
            padding: 20px;
            border-radius: 10px;
            margin-top: 15px;
            margin-bottom: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Refine Button */
        .stButton button {
            background: linear-gradient(to right, #1F618D, #2E86C1);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
        }

        /* Fix Unnecessary Blank Spaces */
        .stMarkdown { margin: 0 !important; padding: 0 !important; }
        .stTextInput { margin-top: 10px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def fetch_tags():
    """Fetch unique tags from the database."""
    connection = sqlite3.connect("linkedin_posts.db")
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT tags FROM influencer_posts")
    tags_data = cursor.fetchall()
    connection.close()

    # Flatten the tags into a unique list
    tags = set()
    for tag_row in tags_data:
        tag_list = tag_row[0].split(", ")
        tags.update(tag_list)

    return sorted(tags)


# Main app layout
def main():
    # Add custom CSS
    add_custom_css()

    # Title and description
    st.markdown('<div class="title">LinkedIn Post Generator 💼🤖</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Generate professional posts tailored to your needs!</div>', unsafe_allow_html=True)

    # Create three columns for dropdowns
    col1, col2, col3 = st.columns(3)

    # Fetch tags dynamically from the database
    tags = fetch_tags()

    with col1:
        selected_tag = st.selectbox("Topic 🎯", options=tags)

    with col2:
        selected_length = st.selectbox("Length 📏", options=length_options)

    with col3:
        selected_language = st.selectbox("Language 🌍", options=language_options)

    # Add Tone Selector
    selected_tone = st.radio("Select Tone 🖋️", options=tone_options, horizontal=True)

    # Generate Button
    if st.button("Generate Post 🚀"):
        st.session_state["generated_post"] = generate_post(selected_length, selected_language, selected_tag, selected_tone)
        st.session_state["refined_post"] = None  # Reset refined post on new generation

    # Display generated post if available
    if "generated_post" in st.session_state and st.session_state["generated_post"]:
        #st.markdown('<div class="post-box">', unsafe_allow_html=True)
        st.markdown("### Initial AI-Generated Draft 📋")
        st.success(st.session_state["generated_post"])
        st.markdown('</div>', unsafe_allow_html=True)

        # Add refinement section
        refine_post()


def refine_post():
    """Interactive chatbot feature for refining the post."""
    #st.markdown('<div class="chatbot-section">', unsafe_allow_html=True)
    st.write("### AI Refinement Assistant 🤖: Ready to improve your post?")
    st.write("👤 Type your request to refine the post:")

    user_feedback = st.text_input("E.g., 'Make it more engaging with emojis' 👤")

    if st.button("Refine Post 🔄"):
        if user_feedback:
            refined_prompt = f'''
            Refine the following post based on this feedback: "{user_feedback}".

            Original Post:
            {st.session_state["generated_post"]}
            '''
            refined_post = generate_post_with_feedback(refined_prompt)
            st.session_state["refined_post"] = refined_post
        else:
            st.warning("Please provide feedback to refine the post.")

    if "refined_post" in st.session_state and st.session_state["refined_post"]:
        #st.markdown('<div class="post-box">', unsafe_allow_html=True)
        st.markdown("### 🤖 Refined Post")
        st.success(st.session_state["refined_post"])
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def generate_post_with_feedback(prompt):
    """Send feedback prompt to LLM for refinement."""
    from llm_helper import llm
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    main()

import sqlite3
from llm_helper import llm


def get_length_str(length):
    """Convert length to a human-readable format."""
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def fetch_filtered_posts(length, language, tag):
    """Fetch filtered posts based on user input."""
    connection = sqlite3.connect("linkedin_posts.db")
    cursor = connection.cursor()

    # Filter posts based on the input
    query = '''
        SELECT text, tags, engagement, language
        FROM influencer_posts
        WHERE line_count BETWEEN ? AND ?
          AND language = ?
          AND tags LIKE ?
        ORDER BY engagement DESC
        LIMIT 2
    '''
    line_count_range = {
        "Short": (1, 5),
        "Medium": (6, 10),
        "Long": (11, 15)
    }
    min_lines, max_lines = line_count_range[length]
    cursor.execute(query, (min_lines, max_lines, language, f"%{tag}%"))
    posts = cursor.fetchall()

    connection.close()
    return posts


def generate_post(length, language, tag, tone="Professional"):
    """Generate a LinkedIn post using the LLM."""
    prompt = get_prompt(length, language, tag, tone)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, tone):
    """Build a prompt for the LLM."""
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the following details. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    4) Tone: {tone}
    If Language is Hinglish, mix Hindi and English but use English script.
    '''
    
    examples = fetch_filtered_posts(length, language, tag)

    if examples:
        prompt += "\n\n5) Use the writing style based on these examples:"
        for i, (text, tags, engagement, post_language) in enumerate(examples):
            prompt += f'\n\nExample {i + 1}:\n{text}'

    return prompt


if __name__ == "__main__":
    # Test the post generator
    print(generate_post("Medium", "English", "Career", "Friendly"))

import sqlite3
import json
import re
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def clean_surrogate_characters(text):
    """Removes invalid Unicode surrogate characters from text."""
    return re.sub(r'[\ud800-\udfff]', '', text)


def fetch_posts_from_db():
    """Fetch posts from the database."""
    connection = sqlite3.connect("linkedin_posts.db")
    cursor = connection.cursor()

    # Fetch all posts
    cursor.execute("SELECT id, text FROM influencer_posts")
    posts = cursor.fetchall()

    connection.close()
    return posts


def update_post_metadata(post_id, metadata):
    """Update processed metadata back to the database."""
    connection = sqlite3.connect("linkedin_posts.db")
    cursor = connection.cursor()

    # Update the database with processed metadata
    cursor.execute('''
        UPDATE influencer_posts
        SET line_count = ?, language = ?, tags = ?
        WHERE id = ?
    ''', (metadata["line_count"], metadata["language"], ', '.join(metadata["tags"]), post_id))

    connection.commit()
    connection.close()


def extract_metadata(post_text):
    """Extract metadata from a post using the LLM."""
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post, and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language, and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means Hindi + English).
    
    Here is the actual post on which you need to perform this task:
    {post_text}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post_text": post_text})

    try:
        json_parser = JsonOutputParser()
        return json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Unable to parse the response. Check the LLM input/output.")


def process_posts():
    """Process posts by fetching, extracting metadata, and updating the database."""
    posts = fetch_posts_from_db()

    for post_id, text in posts:
        clean_text = clean_surrogate_characters(text)
        metadata = extract_metadata(clean_text)
        update_post_metadata(post_id, metadata)

    print("Posts have been successfully processed and metadata updated in the database.")


if __name__ == "__main__":
    process_posts()

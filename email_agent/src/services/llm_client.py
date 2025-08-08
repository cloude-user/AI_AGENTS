import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def classify_email(subject, body):
    prompt = f"""
    You are an email classification AI.
    Categories: Important, Promotional, Spam.
    Classify the following email and return only one word category:
    Subject: {subject}
    Body: {body}
    """
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message["content"].strip()

def generate_reply(subject, body):
    prompt = f"""
    You are an assistant drafting polite professional email replies.
    Reply to the following email appropriately:
    Subject: {subject}
    Body: {body}
    """
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message["content"].strip()

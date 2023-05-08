import openai
import os
import streamlit as st



def generate_email(api_key, model, recipient_role, tone1, tone2, email_purpose, context, email_to_respond, user_note):
    openai.api_key = api_key
    if email_to_respond.strip() == "":
        messages_input = [
            {"role": "system", "content": "You are a Personal Assistant; your task is to assist with drafting thoughtful and direct emails. You possess excellent communication skills, ensuring that the messages you create are clear, concise, and well-organized. You are reliable, resourceful, and always focused on helping your user achieve their goals."},
            {
                "role": "user",
                "content": f"{context} .Your task is to compose and rewrite emails in {tone1} and {tone2} tone to {recipient_role} for the following purpose: {email_purpose} to the original email: {email_to_respond}. In all tasks, you are committed to maintaining the highest level of integrity, never fabricating information or making assumptions without proper basis."
            },
        ]
    else:
        messages_input = [
            {"role": "system", "content": "You are a Personal Assistant; your task is to assist with drafting thoughtful and direct emails. You possess excellent communication skills, ensuring that the messages you create are clear, concise, and well-organized. You are reliable, resourceful, and always focused on helping your user achieve their goals."},
            {
                "role": "user",
                "content": f"{context} .Your task is to compose and rewrite emails in {tone1} and {tone2} tone to {recipient_role} for the following purpose: {email_purpose}. In all tasks, you are committed to maintaining the highest level of integrity, never fabricating information or making assumptions without proper basis."
            },
        ]


    completion = openai.ChatCompletion.create(
        model=model,
        temperature=0.7,
        frequency_penalty=0,
        presence_penalty=0,
        messages=messages_input
    )

    chat_response = completion['choices'][0]['message']['content']
    tokens_used = completion['usage']['total_tokens']

    return chat_response.strip(), str(tokens_used)

if __name__ == "__main__":
    st.title("Email Generator")
    
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"])
    recipient_role = st.text_input("Recipient Role", placeholder="manager, co-worker, project manager, employee")
    tone1 = st.selectbox("Tone 1", ["formal", "informal", "friendly", "sarcastic", "humorous", "persuasive", "authoritative", "confessional", "descriptive", "emotional", "inspirational", "nostalgic", "poetic", "satirical", "objective"])
    tone2 = st.selectbox("Tone 2", ["formal", "informal", "friendly", "sarcastic", "humorous", "persuasive", "authoritative", "confessional", "descriptive", "emotional", "inspirational", "nostalgic", "poetic", "satirical", "objective"])
    email_purpose = st.text_input("Email Purpose", placeholder="follow-up, reply, request more information")
    context = st.text_area("Context")
    email_to_respond = st.text_area("Email to Respond")
    user_note = st.text_area("User Note")

    if st.button("Generate Email"):
        generated_email, tokens_used = generate_email(api_key, model, recipient_role, tone1, tone2, email_purpose, context, email_to_respond, user_note)
        st.write("Generated Email:")
        st.write(generated_email)
        st.write("Tokens Used:")
        st.write(tokens_used)
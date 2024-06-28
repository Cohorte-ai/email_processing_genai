import streamlit as st
import requests
import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from PIL import Image
import os
import pandas as pd
from datetime import datetime

# Load environment variables
import dotenv
dotenv.load_dotenv()

def load_css(file_name):
    with open(file_name) as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Load your CSS
load_css('style.css')

# Load your image
image = Image.open('logo.png')
# Display the image in the sidebar at the top left
st.image(image, width=40)

# Function to get emails based on search prompt
def get_emails(search_prompt):
    url = "https://actions.zapier.com/api/v2/ai-actions/01J06T8Q6TM4EVE9F3NYW1Z292/execute/"
    payload = {
        "instructions": search_prompt,
        "params_constraints": {},
        "preview_only": False
    }
    headers = {
        "X-API-Key": os.getenv('ZAPIER_NLA_API_KEY'),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response_json = json.loads(response.text)
    return response_json["full_results"]

# Function to query LlamaIndex for invoice summary
def summarize_invoices(email_body):
    documents = SimpleDirectoryReader("pdf").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(f"""
    Summarize the invoice information from the following email chain:
    {email_body}
    
    Extract and provide the following information in a structured format:
| Invoice Number | Invoice Amount | Due Date   | Current Status (Paid, Promise, or Dispute) | Next Action                          | Summary  |
|----------------|----------------|------------|--------------------------------------------|---------------------------------------|-------------------|
|                |                |            |                                            |                                       |                   |


    Email status is paid if the invoice is already paid. Status is promise if the invoice is expected to be paid soon by the client. Status is dispute if there is some discrepancy or dispute related to the invoice that is yet to be resolved.
    Provide the information in a markdown table format.
    """)
    return response

# Function to get the latest email from each thread
import email.utils
from datetime import datetime

def get_latest_emails(emails):
    thread_dict = {}
    for email_data in emails:
        if email_data['_zap_search_was_found_status']:
            thread_id = email_data.get('thread_id', email_data['id'])  # Use thread_id if available, else use email id
            
            # Parse the date string using email.utils.parsedate_to_datetime
            date = email.utils.parsedate_to_datetime(email_data['date'])
            
            if thread_id not in thread_dict or date > thread_dict[thread_id]['date']:
                thread_dict[thread_id] = {
                    'date': date,
                    'subject': email_data['subject'],
                    'body_plain': email_data['body_plain'],
                    'from_email': email_data['from']['email']
                }
    
    return [{'Subject': v['subject'], 'Body': v['body_plain'], 'FromEmail': v['from_email']} 
            for v in thread_dict.values()]

# Streamlit UI
st.title("Invoice Status Tracker")

search_prompt = st.text_input("Enter search prompt:", value="Get all emails in inbox with 'Invoices' in the subject")
if st.button("Search Emails"):
    with st.spinner("Searching emails based on the search prompt"):
        if search_prompt:
            emails = get_emails(search_prompt)
            if emails:
                # Get only the latest email from each thread
                email_data = get_latest_emails(emails)
                
                if email_data:
                    # Store email data in session state
                    st.session_state.email_data = email_data
                else:
                    st.markdown('No emails match the search criteria')

# Display the email data if it exists in session state
if 'email_data' in st.session_state:
    st.subheader("Found Emails (Latest from each thread)")
    for email in st.session_state.email_data:
        st.markdown(f"**Subject:** {email['Subject']}")
        st.markdown(f"**From:** {email['FromEmail']}")
        with st.expander("View Email Body"):
            st.text(email['Body'])
        st.markdown("---")

    # Button to summarize invoices
    if st.button("Summarize Invoice Statuses"):
        with st.spinner('Analyzing emails and summarizing invoice statuses'):
            all_invoice_data = []
            for email in st.session_state.email_data:
                response = summarize_invoices(email['Body'])
                st.markdown(response.response)
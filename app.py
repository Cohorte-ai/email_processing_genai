import streamlit as st
import requests
import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from PIL import Image

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
        "X-API-Key": "sk-ak-BmfKoMdhReB7wp430okrdcL0nu",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response_json = json.loads(response.text)
    return response_json["full_results"]

def draft_email_reply(thread, body, to):
    url = "https://actions.zapier.com/api/v2/ai-actions/01J09PBZ62KMPFG55J4CFZC0MR/execute/"
    payload = {
        "instructions": 'Draft a reply with the given body',
        "Thread": thread,
        "Body": body,
        "To": to,
        "preview_only": False
    }
    headers = {
        "X-API-Key": "sk-ak-BmfKoMdhReB7wp430okrdcL0nu",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    # st.write(response.status_code)
    # response_json = json.loads(response.text)
    return response

# Function to query LlamaIndex
def query_llamaindex(email_body):
    documents = SimpleDirectoryReader("pdf").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(email_body)
    return response

# Streamlit UI
st.title("Email Search and Query with LlamaIndex")

search_prompt = st.text_input("Enter search prompt:", value="Get all emails in inbox with 'Customer Query' in the subject")
if st.button("Search Emails"):
    with st.spinner("Searching emails based on the search prompt"):
        if search_prompt:
            emails = get_emails(search_prompt)
            # st.write(emails)
            if emails:
                email_data = []
                for email in emails:
                    if email['_zap_search_was_found_status']:
                        subject = email["subject"]
                        body_plain = email["body_plain"]
                        from_email = email["from"]["email"]
                        email_data.append({"Subject": subject, "Body": body_plain, "FromEmail": from_email})
                    else:
                        email_data.append('No emails match the search criteria')
                
                # Store email data in session state
                st.session_state.email_data = email_data

# Display the email data if it exists in session state
if 'email_data' in st.session_state:
    st.table(st.session_state.email_data)

    # Button to generate replies
    if st.button("Generate Reply Using AI"):
        with st.spinner('Querying the LLM to generate replies'):
            # Query LlamaIndex for each email body
            st.subheader("LlamaIndex Query Results")
            for email in st.session_state.email_data:
                # st.markdown(email)
                response = query_llamaindex(f"""Reply to a customer query as Samsung Customer Care by drafting a well formated email reply only based on information provided. The email should have a proper format with greeting, main body and signoff. Following is the customer query: {email["Body"]}""")
                st.markdown(f"**Customer Email Subject:** `{email['Subject']}`")
                st.markdown("**Response:**")
                st.code(response.response, language='markdown')
                draft_response = draft_email_reply(email['Subject'], response.response, email['FromEmail'])
                if(draft_response.status_code==200):
                    st.success("Draft email sucessfully created in the 'Drafts' folder")

# Email Search and Query with LlamaIndex

Welcome to the Email Search and Query project! This application integrates Gmail with Zapier AI Actions and OpenAI's GPT-3.5 to streamline the process of managing customer support emails. It reads customer support emails, filters them based on specific criteria, and generates replies using Retrieval-Augmented Generation (RAG) from our company's knowledge base. The application also ensures that the draft email appears in the Gmail draft folder, ready for review and sending by customer support staff.

## Features

- **Natural Language Processing:** Understands and processes natural language queries to filter emails.
- **Email Retrieval:** Retrieves emails based on specified search criteria.
- **Automated Reply Generation:** Uses LlamaIndex and OpenAI's GPT-3.5 to draft well-formatted replies.
- **Gmail Integration:** Creates draft replies directly in the Gmail draft folder.
- **User-Friendly Interface:** Built with Streamlit for a simple and intuitive user experience.
- **Scalability:** The workflow can be fully automated without human intervention if needed.

## Tools and Technologies Used

- **LLM:** OpenAI's GPT-3.5
- **LLM Orchestration:** LlamaIndex
- **UI Framework:** Streamlit
- **Automation Platform:** Zapier

## Project Structure

- `app.py`: The main application script for the Streamlit app.
- `Dockerfile`: Contains the Docker configuration for building and running the app.
- `requirements.txt`: Lists the Python packages required for this project.
- `.env`: File to include necessary API keys for authentication.
- `style.css`: CSS file for custom styling.
- `logo.png`: Image file for the application logo.

## Setup and Usage

### Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo.git
```
### Install Required Packages
```bash
pip install -r requirements.txt
```
### Run the Streamlit App
```bash
python -m streamlit run app.py
```

## Docker Support
To build and run the application using Docker, follow these steps:

### Build the Docker Image
```bash
docker build -t email_query_app .
```

### Run the Docker Container
```bash
docker run -p 8501:8501 --env-file .env email_query_app
```
Note: Ensure you have the .env file containing the necessary API keys in your project directory before running the Docker container.

## How to Activate Gmail Integrations with Zapier AI Actions

### Step 1: Log in to Zapier
Go to [Zapier.com](https://www.zapier.com) and log in with your account credentials.

### Step 2: Set Up AI Actions
Visit [Zapier AI Actions Demo](https://actions.zapier.com/demo/) to begin the setup process.

### Step 3: Follow the Below Steps to Integrate your Gmail

1. **Open the Action Setup Window** 
   - Click on the "Open action setup window" button.

2. **Allow Zapier to Access Your Account** 
   - Click "Allow" to give Zapier the necessary permissions.

3. **Set Up Your Custom Action** 
   - In the "Action" field, type the action you want to set up.

4. **Select Gmail: Find Email Action** 
   - Choose "Gmail: Find Email" from the list of actions.

5. **Connect Your Gmail Account** 
   - Click "Connect a new Gmail account" to start the authorization process.

6. **Allow Zapier to Access Your Gmail Account** 
   - Click "Yes, Continue to Gmail" to proceed.

7. **Sign In to Your Google Account** 
   - Enter your email or phone and click "Next."

8. **Confirm Sign-In to Zapier** 
   - Click "Continue" after verifying your Google account.

9. **Grant Permissions to Zapier** 
   - Click "Allow" to grant Zapier access to your Gmail account.

10. **Complete the Action Setup** 
    - Enter the search string in the "Search String" field.
    - Click "Enable action" to complete the setup.

### Step 4: Get Zapier API Key
Go to [Zapier AI Actions Credentials](https://actions.zapier.com/credentials/) to obtain your Zapier API Key.
Use this API key in your code to integrate Zapier AI Actions with your Gmail account.

By following these steps, you will successfully activate and set up Gmail integrations with Zapier AI Actions, allowing you to automate email-related tasks seamlessly.

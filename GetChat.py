from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

def chat (message):
   
    load_dotenv()


    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT_CHAT')
    api_key = os.getenv('AZURE_OPENAI_API_KEY_CHAT')
    deployment_id = 'gpt-4o'  # Example: "gpt-4"
    s = endpoint + ' ' + api_key + " "
    # return('reached step1')
    # Create a client for Azure OpenAI
    try:
        client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, azure_deployment=deployment_id, api_version='2025-02-01-preview')
    except Exception as e:
        return "some error happened"

    
    # Create the conversation request
    messages = [
      
        {"role": "user", "content": message}

    ]
  
    try:
        s = s+"reached level 2 "
        response = client.chat.completions.create(
            messages=messages,
            model=deployment_id,
            temperature=0.2
        )
        s = s + "reached level 3"
        return response.choices[0].message.content
    except Exception as e:
        import traceback
        error_message = f"{e} {s}\n{traceback.format_exc()}"
        return error_message
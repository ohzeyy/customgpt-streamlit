import streamlit as st
import requests
import json
from streamlit.logger import get_logger
from bs4 import BeautifulSoup

# URL to test: https://refactored-space-umbrella-56p4pv46994h4q67-8501.app.github.dev/

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Arc'y Product Guide",
        page_icon="🧗",
    )

    st.write("# Arc'teryx Chatbot")

    # st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Arc'y is a CustomGPT-powered AI Product Expert.
        Have any questions about Arc'teryx and their products? Ask Arc'y!
        Arc'y can provide general info about the Arc'teryx company and their mission, as well as provide product recommendations based on your needs.
        **Try asking what jacket is best for you.** 
        - All data is from https://arcteryx.com/us/en/
    """)
    reply = ""
    query = st.chat_input("Ask me anything...")
    if query:
      reply = sendMessageReturnReply(query)
      st.write(f"{reply}")
      st.image(get_open_graph_data_imageURL("https://www.nike.com/t/sportswear-tech-fleece-windrunner-mens-full-zip-hoodie-rznlBf/FB7921-010"))
    
    

def sendMessageReturnReply(query):
  projectID = "15146"
  conversationID = "ea411e40-4d8c-4755-957f-0dc158fde42e"

  url = "https://app.customgpt.ai/api/v1/projects/15146/conversations/5cc72e38-6a92-4552-a49b-1a5e48e9ed6b/messages?stream=false&lang=en"

  # query = "I'm a male living in Boston and I wear size M, what jackets do you recommend for me?"

  payload = { "prompt": query }
  headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 2206|B6zA5s7IkHY7CtUqReUWhSkwcRip3n9DGFhrO6uc"
  }

  response = requests.post(url, json=payload, headers=headers)
  reply = ""

  # Check if the request was successful
  if response.status_code == 200:
    try:
      response_json = json.loads(response.text)
      openai_response = response_json.get("data", {}).get("openai_response")
        
      if openai_response:
        print("OpenAI Response:", openai_response)
        reply = openai_response
            
      else:
        print("No 'openai_response' found in the JSON response.")
        reply = "Response Error"
    except json.JSONDecodeError:
        print("Invalid JSON response.")
        reply = "JSON Error"
  else:
    print(f"Request failed with status code {response.status_code}")
    reply = "Request Error"
  
  return reply

  from bs4 import BeautifulSoup

def get_open_graph_data_imageURL(url):
    try:
        # Set the User-Agent header to mimic a web browser request.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Send an HTTP GET request to the URL with the specified headers.
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200).
        if response.status_code == 200:
            html_content = response.text

            # Parse the HTML content using BeautifulSoup.
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the Open Graph meta tags within the HTML head.
            og_data = {}
            for tag in soup.find_all('meta', attrs={'property': 'og:title'}):
                og_data['title'] = tag['content']
            for tag in soup.find_all('meta', attrs={'property': 'og:description'}):
                og_data['description'] = tag['content']
            for tag in soup.find_all('meta', attrs={'property': 'og:image'}):
                og_data['image'] = tag['content']
            # You can extract more Open Graph properties as needed.

            return og_data.get('image', 'N/A')

        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None

if __name__ == "__main__":
    run()

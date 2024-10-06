import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from .env
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("API_KEY")  # Get API key from environment variable
)

# Function to interact with the OpenAI Chat API
def chatbot_response(user_input):
    try:
        # Call to the OpenAI API with streaming enabled
        response_text = ""
        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.5,
            max_tokens=150,
            stream=True
        )
        
        # Accumulate the streamed response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
        
        return response_text.strip()  # Return the accumulated response
    except Exception as e:
        return f"Error: {str(e)}"

# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Chatbot Interface")
    
    chatbot_input = gr.Textbox(label="You:", placeholder="Type your message here...")
    chatbot_output = gr.Textbox(label="Chatbot:", interactive=False)

    submit_button = gr.Button("Send")

    # Connect button to the response function
    submit_button.click(chatbot_response, inputs=chatbot_input, outputs=chatbot_output)

# Run the Gradio app
demo.launch()
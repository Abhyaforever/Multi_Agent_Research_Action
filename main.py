import os
from dotenv import load_dotenv
import autogen
from flask import Flask, request, render_template

# Load environment variables
load_dotenv()

# Configure OpenAI (actually OpenRouter) settings
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("BASE_URL")

# Create Flask app
app = Flask(__name__)

# Correctly configure agent settings for OpenRouter
config_list = [{
    "model": "gpt-4",  # or gpt-3.5-turbo if you want faster cheaper
    "api_key": openai.api_key,
    "base_url": openai.api_base,  # <-- Important!
}]

# Create agents with corrected config
coordinator = autogen.AssistantAgent(
    name="Coordinator",
    llm_config={
        "config_list": config_list,
        "temperature": 0.3
    }
)

research_worker = autogen.AssistantAgent(
    name="ResearchWorker",
    llm_config={
        "config_list": config_list,
        "temperature": 0.3
    }
)

# Configure user proxy
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={"work_dir": "code", "use_docker": False}
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query = request.form["query"]
        task = f"User wants to research about: {query}. Break it down and assign to ResearchWorker."
        try:
            import logging
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            
            logger.info(f"Initiating chat with query: {query}")
            chat_result = user_proxy.initiate_chat(
                coordinator,
                message=task,
                receivers=[research_worker]
            )
            
            # Get last assistant message
            final_answer = ""
            for message in chat_result.chat_history:
                if message["role"] == "assistant":
                    final_answer = message["content"]
                    logger.info(f"Received response: {final_answer[:100]}...")

            result = f"✅ Research Result: {final_answer}"
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"Error occurred: {str(e)}\n{error_trace}")
            result = f"⚠️ Error details: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

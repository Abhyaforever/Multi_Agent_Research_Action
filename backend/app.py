from flask import Flask, request, jsonify, render_template
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.coordinator_agent import CoordinatorAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.communication_agent import CommunicationAgent

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent.parent / "templates"),
    static_folder=str(Path(__file__).parent.parent / "static")
)
load_dotenv()

# Initialize agents with centralized OpenRouter configuration
from config.settings import OpenRouterConfig

llm_config = {
    "config_list": [{
        "model": OpenRouterConfig.DEFAULT_MODEL,
        "api_key": OpenRouterConfig.API_KEY,
        "base_url": OpenRouterConfig.BASE_URL,
        "api_type": "openrouter",
        "context_length": OpenRouterConfig.MAX_TOKENS,
        "headers": OpenRouterConfig.get_headers()
    }],
    "temperature": OpenRouterConfig.TEMPERATURE
}

coordinator = CoordinatorAgent(name="Coordinator", llm_config=llm_config)
research_worker = ResearchAgent(name="ResearchWorker", llm_config=llm_config)
analysis_worker = AnalysisAgent(name="AnalysisWorker", llm_config=llm_config)
communication_worker = CommunicationAgent(name="CommunicationWorker", llm_config=llm_config)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/research", methods=["POST"])
async def handle_research():
    try:
        data = request.json
        task = data.get("query")
        
        if not task:
            return jsonify({"error": "No query provided"}), 400
            
        # Break down task
        subtasks = coordinator.break_down_task(task)
        
        # 🛡️ Filter valid subtasks only
        valid_subtasks = []
        for subtask in subtasks:
            if not any(x in subtask.lower() for x in ["<html", "<head", "<body", "<script>", "<style>", ":root", "--bprogress"]):
                valid_subtasks.append(subtask)

        if not valid_subtasks:
            return jsonify({"error": "No valid subtasks generated. Try a simpler query."}), 400
        
        # Assign subtasks and get results
        results = await coordinator.assign_subtasks(valid_subtasks, [research_worker])
        
        # Collect and organize results
        final_report = coordinator.collect_results(results)
        
        return jsonify(final_report)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error occurred: {str(e)}\n{error_trace}")
        return jsonify({"error": str(e)}), 500




# Uncomment the following lines to enable the analysis and communication agents
# @app.route("/research", methods=["POST"])
# async def handle_research():
#     try:
#         data = request.json
#         task = data.get("query")
        
#         if not task:
#             return jsonify({"error": "No query provided"}), 400
            
#         # Break down task
#         subtasks = coordinator.break_down_task(task)
        
#         # Assign subtasks and get results
#         results = await coordinator.assign_subtasks(subtasks, [research_worker])
        
#         # Demonstrate analysis agent usage (stub)
#         analysis_results = []
#         for subtask in subtasks:
#             analysis_results.append(await analysis_worker.perform_task(subtask))
        
#         # Demonstrate communication agent usage (stub)
#         comms = []
#         for result in analysis_results:
#             comms.append(await communication_worker.perform_task(result, recipient="user@example.com"))
        
#         # Collect and organize results
#         final_report = coordinator.collect_results(results)
#         final_report["analysis"] = analysis_results
#         final_report["communications"] = comms
        
#         return jsonify(final_report)
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

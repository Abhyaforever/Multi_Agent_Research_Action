import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion
from tools.web_search_tool import perform_web_search
from dotenv import load_dotenv
from config.settings import OpenRouterConfig

class ResearchAgent:
    def __init__(self, name, llm_config):
        self.name = name
        self.llm_config = llm_config
        load_dotenv()  # Load environment variables

        # Initialize Semantic Kernel
        self.kernel = sk.Kernel()

        # Configure OpenAITextCompletion settings
        completion_config = {
            "ai_model_id": OpenRouterConfig.DEFAULT_MODEL,
            "api_key": OpenRouterConfig.API_KEY,
            "default_headers": OpenRouterConfig.get_headers()
        }

        # Create OpenAITextCompletion service
        text_completion = OpenAITextCompletion(
            ai_model_id=completion_config["ai_model_id"],
            api_key=completion_config["api_key"],
            default_headers=completion_config["default_headers"]
        )
        # Override endpoint for OpenRouter (must include /chat/completions)
        text_completion.client.base_url = OpenRouterConfig.BASE_URL + "/chat/completions"

        # Add the service to the kernel
        self.kernel.add_service(text_completion)

    async def perform_task(self, task):
        try:
            # Perform web search
            search_results = perform_web_search(task)

            if isinstance(search_results, str):
                # If search_results is an error string
                return f"Web Search Error: {search_results}"

            if not search_results:
                return "No relevant search results found."

            # Create context for analysis
            context = f"Task: {task}\n\nSearch Results:\n"
            for result in search_results:
                context += f"- {result['title']}\n  {result['snippet']}\n  Source: {result['link']}\n\n"

            # Define the prompt for semantic analysis
            prompt = """
            Analyze the following research results and provide a detailed summary:
            {{$input}}
            
            Please structure your response as follows:
            1. Key Findings
            2. Important Details
            3. Relevant Examples
            4. Conclusions
            
            Keep the response focused, accurate, and well-organized.
            """

            # Create semantic function
            semantic_function = self.kernel.create_semantic_function(
                prompt=prompt,
                service_id="openrouter",
                max_tokens=1000,
                temperature=0.3
            )

            # Generate analysis using the context
            context_vars = sk.ContextVariables(context)
            result = await semantic_function.invoke_async(variables=context_vars)
            return str(result.result)

        except Exception as e:
            return f"Error in research task: {str(e)}"
    #    # Uncomment the following lines if you want to use the perform_web_search function directly
    # async def perform_task(self, task):
    #     try:
    #         # Perform web search
    #         search_results = perform_web_search(task)

    #         # Create context for analysis
    #         context = f"Task: {task}\n\nSearch Results:\n"
    #         for result in search_results:
    #             context += f"- {result['title']}\n  {result['snippet']}\n  Source: {result['link']}\n\n"

    #         # Define the prompt for semantic analysis
    #         prompt = """
    #         Analyze the following research results and provide a detailed summary:
    #         {{$input}}
            
    #         Please structure your response as follows:
    #         1. Key Findings
    #         2. Important Details
    #         3. Relevant Examples
    #         4. Conclusions
            
    #         Keep the response focused, accurate, and well-organized.
    #         """

    #         # Create semantic function
    #         semantic_function = self.kernel.create_semantic_function(
    #             prompt=prompt,
    #             service_id="openrouter",
    #             max_tokens=1000,
    #             temperature=0.3
    #         )

    #         # Generate analysis using the context
    #         context_vars = sk.ContextVariables(context)
    #         result = await semantic_function.invoke_async(variables=context_vars)
    #         return str(result.result)

    #     except Exception as e:
    #         return f"Error in research task: {str(e)}"

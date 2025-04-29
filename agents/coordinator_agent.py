# Coordinator Agent
import openai
import json
import asyncio
from config.settings import OpenRouterConfig

import os
from openai import OpenAI

class CoordinatorAgent:
    def __init__(self, name, llm_config):
        self.name = name
        self.llm_config = llm_config
        # Configure OpenAI client with OpenRouter settings
        openai.api_key = OpenRouterConfig.API_KEY
        openai.base_url = OpenRouterConfig.BASE_URL
        self.headers = OpenRouterConfig.get_headers()

    from openai import OpenAI
    import os

    def break_down_task(self, task: str, max_subtasks: int = 5) -> list:
        try:
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("BASE_URL")
            )

            prompt = f"""
            You are a research assistant. Break this into {max_subtasks} subtasks. Avoid repetition.

            Task: {task}

            Return only a numbered list of subtasks.
            """

            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )

            text = response.choices[0].message.content.strip()
            lines = text.split("\n")
            subtasks = [line.split(".", 1)[-1].strip() for line in lines if "." in line]

            return subtasks[:max_subtasks]

        except Exception as e:
            print(f"[Coordinator] Subtask generation failed: {e}")
            return [task]



    # uncomment the following method if you want to use LLM for task breakdown
    # def break_down_task(self, task):
    #     """Break down a complex task into smaller, focused subtasks"""
    #     prompt = f"""
    #     Break down the following research task into 2-4 specific subtasks:
    #     Task: {task}
        
    #     Each subtask should be focused, specific, and contribute to the overall goal.
    #     Return only the list of subtasks, one per line.
    #     """
    
    #     response = openai.chat.completions.create(
    #         **OpenRouterConfig.get_completion_config(),
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     print('DEBUG break_down_task response:', response)
    #     # Handle both string and object response types
    #     if isinstance(response, str):
    #         content = response
    #     elif hasattr(response, 'choices'):
    #         content = response.choices[0].message.content
    #     elif isinstance(response, dict) and 'choices' in response:
    #         content = response['choices'][0]['message']['content']
    #     else:
    #         raise ValueError(f"Unexpected response type: {type(response)}")
    #     subtasks = content.strip().split('\n')
    #     return [task.strip() for task in subtasks if task.strip()]

    async def assign_subtasks(self, subtasks, workers):
        """Assign subtasks to workers and collect results asynchronously"""
        tasks = []
        for subtask in subtasks:
            task = workers[0].perform_task(subtask)  # Using first worker for now
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results    

    def generate_conclusion(self, subtasks, results):
        try:
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("BASE_URL")
            )

            content = "\n".join(results)
            prompt = f"""
            Given the following research subtasks and their findings, generate a detailed, intelligent conclusion that gives useful recommendations to the user:

            Subtasks:
            {subtasks}

            Results:
            {content}

            Respond in clear, concise, paragraph form.
            """

            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a research assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Final conclusion could not be generated: {str(e)}"


    def collect_results(self, results, subtasks=None):
        sections = []
        for idx, result in enumerate(results):
            if not result:
                continue  # skip failed subtasks

            title = subtasks[idx] if subtasks and idx < len(subtasks) else f"Subtask {idx + 1}"
            sections.append({
                "title": title,
                "content": result
            })

        conclusion = self.generate_conclusion([s['title'] for s in sections], [s['content'] for s in sections])
        return {
            "sections": sections,
            "conclusion": conclusion
        }



    #### Uncomment the following method if you want to use LLM for result collection
    # def collect_results(self, results):
    #     """Organize and summarize the results into a coherent report"""
    #     combined_results = "\n\n".join(results)
        
    #     prompt = f"""
    #     Based on the research results below, create a comprehensive report with clear sections and a conclusion. Include specific examples and insights where relevant.

    #     Research Results:
    #     {combined_results}
        
    #     Create a well-structured report with:
    #     1. Clear sections for each major topic
    #     2. A comprehensive conclusion
        
    #     Format the response as a JSON object with this structure:
    #     {{
    #         "sections": [
    #             {{"title": "Section Title", "content": "Section content"}},
    #             ...
    #         ],
    #         "conclusion": "Overall summary and key takeaways"
    #     }}
    #     """
        
    #     response = openai.chat.completions.create(
    #         **OpenRouterConfig.get_completion_config(),
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     print('DEBUG collect_results response:', response)
    #     # Handle both string and object response types
    #     if isinstance(response, str):
    #         content = response
    #     elif hasattr(response, 'choices'):
    #         content = response.choices[0].message.content
    #     elif isinstance(response, dict) and 'choices' in response:
    #         content = response['choices'][0]['message']['content']
    #     else:
    #         raise ValueError(f"Unexpected response type: {type(response)}")
    #     try:
    #         return json.loads(content)
    #     except json.JSONDecodeError:
    #         # Fallback in case of JSON parsing error
    #         return {
    #             "sections": [{
    #                 "title": "Research Results",
    #                 "content": content
    #             }],
    #             "conclusion": "Unable to format results in structured format."
    #         }

    


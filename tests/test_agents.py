# tests/test_agents.py

import unittest
import asyncio
from agents.coordinator_agent import CoordinatorAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.communication_agent import CommunicationAgent

class TestAgents(unittest.TestCase):
    def test_coordinator(self):
        coordinator = CoordinatorAgent(name="Coordinator", llm_config={})
        subtasks = coordinator.break_down_task("Compare iOS and Android")
        self.assertGreaterEqual(len(subtasks), 2)

    def test_research_agent(self):
        async def run():
            research_worker = ResearchAgent(name="ResearchWorker", llm_config={})
            result = await research_worker.perform_task("Compare iOS and Android")
            return result

        result = asyncio.run(run())
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 10)

    def test_analysis_agent(self):
        async def run():
            analysis_worker = AnalysisAgent(name="AnalysisWorker", llm_config={})
            result = await analysis_worker.perform_task("Test Analysis Task")
            return result

        result = asyncio.run(run())
        self.assertIn("Analysis", result)

    def test_communication_agent(self):
        async def run():
            communication_worker = CommunicationAgent(name="CommunicationWorker", llm_config={})
            result = await communication_worker.perform_task("Test Message", recipient="test@example.com")
            return result

        result = asyncio.run(run())
        self.assertIn("Message to test@example.com", result)

if __name__ == "__main__":
    unittest.main()

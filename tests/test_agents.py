# Unit Tests for Agents
import unittest
from agents.coordinator_agent import CoordinatorAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.communication_agent import CommunicationAgent

class TestAgents(unittest.TestCase):
    def test_coordinator(self):
        coordinator = CoordinatorAgent(name="Coordinator", llm_config={})
        subtasks = coordinator.break_down_task("Test Task")
        self.assertEqual(len(subtasks), 2)

    def test_research_agent(self):
        research_worker = ResearchAgent(name="ResearchWorker", llm_config={})
        result = research_worker.perform_task("Test Subtask")
        self.assertIn("Summary", result)

    def test_analysis_agent(self):
        analysis_worker = AnalysisAgent(name="AnalysisWorker", llm_config={})
        import asyncio
        result = asyncio.run(analysis_worker.perform_task("Test Analysis Task"))
        self.assertIn("Analysis for", result)

    def test_communication_agent(self):
        communication_worker = CommunicationAgent(name="CommunicationWorker", llm_config={})
        import asyncio
        result = asyncio.run(communication_worker.perform_task("Test Message", recipient="test@example.com"))
        self.assertIn("Message to test@example.com", result)

if __name__ == "__main__":
    unittest.main()

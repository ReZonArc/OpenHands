"""Unit tests for OpenCog Agent implementation."""

import pytest
from unittest.mock import Mock, patch

from openhands.agenthub.opencog_agent.opencog_agent import OpenCogAgent
from openhands.controller.state.state import State
from openhands.core.config import AgentConfig, LLMConfig
from openhands.core.config.openhands_config import OpenHandsConfig
from openhands.events.action import MessageAction
from openhands.events.event import EventSource
from openhands.llm.llm_registry import LLMRegistry


@pytest.fixture
def create_llm_registry():
    """Create LLM registry for testing."""
    def _get_registry(llm_config):
        config = OpenHandsConfig()
        config.set_llm_config(llm_config)
        return LLMRegistry(config=config)
    return _get_registry


@pytest.fixture
def opencog_agent(create_llm_registry):
    """Create OpenCog agent instance for testing."""
    llm_config = LLMConfig(model='gpt-4o', api_key='test_key')
    config = AgentConfig()
    agent = OpenCogAgent(config=config, llm_registry=create_llm_registry(llm_config))
    # Mock the LLM to avoid actual API calls
    agent.llm = Mock()
    return agent


@pytest.fixture
def mock_state():
    """Create mock state for testing."""
    state = Mock(spec=State)
    state.history = []
    state.extra_data = {}
    state.iteration_flag = Mock()
    state.iteration_flag.current_value = 1
    return state


class TestOpenCogAgent:
    """Test cases for the OpenCogAgent class."""
    
    def test_agent_initialization(self, opencog_agent):
        """Test that the agent initializes correctly."""
        assert isinstance(opencog_agent, OpenCogAgent)
        assert opencog_agent.VERSION == '1.0'
        assert len(opencog_agent.tools) == 3  # AtomSpace, Reasoning, PatternMatching
        assert opencog_agent._atomspace == {}
        assert opencog_agent._knowledge_base == {}
        assert opencog_agent._reasoning_history == []
    
    def test_agent_tools(self, opencog_agent):
        """Test that the agent has correct tools."""
        tool_names = [tool['function']['name'] for tool in opencog_agent.tools]
        expected_tools = ['atomspace_operation', 'cognitive_reasoning', 'pattern_matching']
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
    
    def test_extract_user_message_with_user_message(self, opencog_agent, mock_state):
        """Test extracting user message from state history."""
        user_msg = MessageAction(content="Hello, implement OpenCog")
        user_msg._source = EventSource.USER
        
        agent_msg = MessageAction(content="I'll help you")
        agent_msg._source = EventSource.AGENT
        
        mock_state.history = [user_msg, agent_msg]
        
        result = opencog_agent._extract_user_message(mock_state)
        assert result == "Hello, implement OpenCog"
    
    def test_extract_user_message_without_user_message(self, opencog_agent, mock_state):
        """Test extracting user message when none exists."""
        agent_msg = MessageAction(content="I'll help you")
        agent_msg._source = EventSource.AGENT
        
        mock_state.history = [agent_msg]
        
        result = opencog_agent._extract_user_message(mock_state)
        assert result == ""
    
    def test_pattern_recognition_task_request(self, opencog_agent):
        """Test pattern recognition for task requests."""
        message = "Please implement a new feature for me"
        patterns = opencog_agent._recognize_patterns(message)
        
        task_pattern = next((p for p in patterns if p['type'] == 'task_request'), None)
        assert task_pattern is not None
        assert task_pattern['confidence'] == 0.8
    
    def test_pattern_recognition_question(self, opencog_agent):
        """Test pattern recognition for questions."""
        message = "What is OpenCog?"
        patterns = opencog_agent._recognize_patterns(message)
        
        question_pattern = next((p for p in patterns if p['type'] == 'information_request'), None)
        assert question_pattern is not None
        assert question_pattern['confidence'] == 0.9
    
    def test_pattern_recognition_problem_solving(self, opencog_agent):
        """Test pattern recognition for problem solving requests."""
        message = "I have an error in my code, please help debug it"
        patterns = opencog_agent._recognize_patterns(message)
        
        problem_pattern = next((p for p in patterns if p['type'] == 'problem_solving'), None)
        assert problem_pattern is not None
        assert problem_pattern['confidence'] == 0.85
    
    def test_inference_with_context(self, opencog_agent):
        """Test inference with previous context."""
        # Add some reasoning history
        opencog_agent._reasoning_history.append({
            'input_message': 'Tell me about OpenCog',
            'timestamp': 0
        })
        
        message = "More about OpenCog please"
        inferences = opencog_agent._perform_inference(message)
        
        # Should find context similarity
        context_inference = next((inf for inf in inferences if inf['type'] == 'context_similarity'), None)
        assert context_inference is not None
    
    def test_inference_domain_expertise(self, opencog_agent):
        """Test domain-specific inference."""
        message = "Explain OpenCog architecture"
        inferences = opencog_agent._perform_inference(message)
        
        domain_inference = next((inf for inf in inferences if inf['type'] == 'domain_expertise'), None)
        assert domain_inference is not None
        assert domain_inference['confidence'] == 0.95
    
    def test_attention_allocation(self, opencog_agent):
        """Test attention allocation mechanism."""
        message = "Urgent! Fix this code bug"
        attention = opencog_agent._allocate_attention(message)
        
        # Should allocate more attention to urgency
        assert attention['urgency'] > 0.1  # Base value
        assert sum(attention.values()) == pytest.approx(1.0, rel=1e-2)
    
    def test_goal_identification_implementation(self, opencog_agent):
        """Test goal identification for implementation tasks."""
        message = "Create a new OpenCog agent"
        goals = opencog_agent._identify_goals(message)
        
        impl_goal = next((g for g in goals if g['type'] == 'implementation'), None)
        assert impl_goal is not None
        assert impl_goal['priority'] == 'high'
    
    def test_goal_identification_learning(self, opencog_agent):
        """Test goal identification for learning tasks."""
        message = "Help me understand cognitive architectures"
        goals = opencog_agent._identify_goals(message)
        
        learning_goal = next((g for g in goals if g['type'] == 'learning'), None)
        assert learning_goal is not None
        assert learning_goal['priority'] == 'medium'
    
    def test_confidence_calculation(self, opencog_agent):
        """Test confidence calculation."""
        # Short, unclear message
        low_conf = opencog_agent._calculate_confidence("help")
        assert low_conf < 0.8
        
        # Clear, domain-specific message
        high_conf = opencog_agent._calculate_confidence("Explain OpenCog AtomSpace knowledge representation")
        assert high_conf > 0.8
    
    def test_cognitive_reasoning_integration(self, opencog_agent, mock_state):
        """Test the complete cognitive reasoning pipeline."""
        message = "Implement OpenCog reasoning in my project"
        
        reasoning_result = opencog_agent._apply_cognitive_reasoning(message, mock_state)
        
        assert 'input_message' in reasoning_result
        assert 'patterns_recognized' in reasoning_result
        assert 'inferences' in reasoning_result
        assert 'attention_focus' in reasoning_result
        assert 'goals_identified' in reasoning_result
        assert 'confidence' in reasoning_result
        assert 'timestamp' in reasoning_result
        
        assert reasoning_result['input_message'] == message
        assert len(opencog_agent._reasoning_history) == 1
    
    def test_response_generation(self, opencog_agent):
        """Test cognitive response generation."""
        reasoning_result = {
            'patterns_recognized': [
                {'type': 'task_request', 'confidence': 0.9}
            ],
            'goals_identified': [
                {'type': 'implementation', 'priority': 'high'}
            ],
            'confidence': 0.85
        }
        
        response = opencog_agent._generate_cognitive_response(reasoning_result)
        
        assert "understand your request clearly" in response.lower()
        assert "implement" in response.lower()
        assert "opencog" in response.lower()
    
    def test_knowledge_base_update(self, opencog_agent):
        """Test knowledge base updating mechanism."""
        message = "Test message"
        reasoning = {
            'patterns_recognized': [{'type': 'test', 'confidence': 0.8}],
            'confidence': 0.7
        }
        response = "Test response"
        
        initial_kb_size = len(opencog_agent._knowledge_base)
        initial_atomspace_size = len(opencog_agent._atomspace)
        
        opencog_agent._update_knowledge_base(message, reasoning, response)
        
        # Should update both knowledge base and atomspace
        assert len(opencog_agent._atomspace) == initial_atomspace_size + 1
        
        # Should add to knowledge base if new pattern type
        if 'test' not in opencog_agent._knowledge_base:
            assert len(opencog_agent._knowledge_base) > initial_kb_size
    
    def test_step_with_user_message(self, opencog_agent, mock_state):
        """Test agent step with valid user message."""
        user_msg = MessageAction(content="Explain OpenCog cognitive architecture")
        user_msg._source = EventSource.USER
        mock_state.history = [user_msg]
        
        action = opencog_agent.step(mock_state)
        
        assert isinstance(action, MessageAction)
        assert "opencog" in action.content.lower()
        assert len(opencog_agent._reasoning_history) == 1
    
    def test_step_without_user_message(self, opencog_agent, mock_state):
        """Test agent step without user message."""
        mock_state.history = []
        
        action = opencog_agent.step(mock_state)
        
        # Should finish when no user message found
        from openhands.events.action import AgentFinishAction
        assert isinstance(action, AgentFinishAction)
        assert "no user message" in action.thought.lower()
    
    def test_step_with_exception(self, opencog_agent, mock_state):
        """Test agent step when exception occurs."""
        # Mock a method to raise an exception
        with patch.object(opencog_agent, '_extract_user_message', side_effect=Exception("Test error")):
            action = opencog_agent.step(mock_state)
            
            from openhands.events.action import AgentFinishAction
            assert isinstance(action, AgentFinishAction)
            assert "error occurred" in action.thought.lower()
    
    def test_reset_preserves_knowledge(self, opencog_agent):
        """Test that reset preserves learned knowledge."""
        # Add some knowledge
        opencog_agent._knowledge_base['test'] = ['data']
        opencog_agent._reasoning_history.append({'test': 'data'})
        
        opencog_agent.reset()
        
        # Knowledge should be preserved
        assert 'test' in opencog_agent._knowledge_base
        assert len(opencog_agent._reasoning_history) == 1
        # But agent state should be reset
        assert not opencog_agent.complete


class TestOpenCogAgentTools:
    """Test cases for OpenCog agent tools."""
    
    def test_atomspace_tool_structure(self):
        """Test AtomSpace tool structure."""
        from openhands.agenthub.opencog_agent.tools.atomspace import AtomSpaceTool
        
        assert AtomSpaceTool['type'] == 'function'
        assert AtomSpaceTool['function']['name'] == 'atomspace_operation'
        
        params = AtomSpaceTool['function']['parameters']['properties']
        assert 'operation' in params
        assert 'data' in params
        assert 'context' in params
        
        # Check required parameters
        required = AtomSpaceTool['function']['parameters']['required']
        assert 'operation' in required
        assert 'data' in required
    
    def test_reasoning_tool_structure(self):
        """Test Reasoning tool structure."""
        from openhands.agenthub.opencog_agent.tools.reasoning import ReasoningTool
        
        assert ReasoningTool['type'] == 'function'
        assert ReasoningTool['function']['name'] == 'cognitive_reasoning'
        
        params = ReasoningTool['function']['parameters']['properties']
        assert 'reasoning_type' in params
        assert 'premises' in params
        assert 'goal' in params
        
        # Check reasoning types
        reasoning_types = params['reasoning_type']['enum']
        expected_types = ['deductive', 'inductive', 'abductive', 'analogical', 'causal', 'meta']
        for rtype in expected_types:
            assert rtype in reasoning_types
    
    def test_pattern_matching_tool_structure(self):
        """Test Pattern Matching tool structure."""
        from openhands.agenthub.opencog_agent.tools.pattern_matching import PatternMatchingTool
        
        assert PatternMatchingTool['type'] == 'function'
        assert PatternMatchingTool['function']['name'] == 'pattern_matching'
        
        params = PatternMatchingTool['function']['parameters']['properties']
        assert 'pattern_type' in params
        assert 'pattern_specification' in params
        
        # Check pattern types
        pattern_types = params['pattern_type']['enum']
        expected_types = ['structural', 'temporal', 'semantic', 'behavioral', 'fuzzy', 'compositional']
        for ptype in expected_types:
            assert ptype in pattern_types
"""Reasoning tool for OpenCog cognitive inference.

This tool provides access to OpenCog's reasoning capabilities including
probabilistic logic programming, pattern matching, and cognitive inference.
"""

from typing import Any, Dict

# Tool definition for OpenCog reasoning operations
ReasoningTool = {
    'type': 'function',
    'function': {
        'name': 'cognitive_reasoning',
        'description': """Perform cognitive reasoning operations using OpenCog's inference engines.
        
        This tool provides access to OpenCog's sophisticated reasoning capabilities:
        
        - Probabilistic Logic Networks (PLN) for uncertain reasoning
        - Forward and backward chaining inference
        - Abductive reasoning for hypothesis generation
        - Analogical reasoning for pattern transfer
        - Causal reasoning for understanding relationships
        - Meta-reasoning about reasoning processes
        
        Reasoning types available:
        - 'deductive': Apply logical rules to derive conclusions
        - 'inductive': Generalize from specific examples
        - 'abductive': Generate hypotheses to explain observations
        - 'analogical': Reason by analogy with known patterns
        - 'causal': Analyze cause-effect relationships
        - 'meta': Reason about reasoning processes themselves
        """,
        'parameters': {
            'type': 'object',
            'properties': {
                'reasoning_type': {
                    'type': 'string',
                    'enum': ['deductive', 'inductive', 'abductive', 'analogical', 'causal', 'meta'],
                    'description': 'The type of reasoning to perform'
                },
                'premises': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Input premises or facts for reasoning'
                },
                'goal': {
                    'type': 'string',
                    'description': 'Reasoning goal or question to answer'
                },
                'confidence_threshold': {
                    'type': 'number',
                    'minimum': 0.0,
                    'maximum': 1.0,
                    'default': 0.7,
                    'description': 'Minimum confidence level for conclusions'
                },
                'max_steps': {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 100,
                    'default': 10,
                    'description': 'Maximum reasoning steps to perform'
                }
            },
            'required': ['reasoning_type', 'premises', 'goal']
        }
    }
}
"""Pattern matching tool for OpenCog cognitive pattern recognition.

This tool provides sophisticated pattern matching capabilities based on
OpenCog's pattern matcher for knowledge discovery and reasoning.
"""

from typing import Any, Dict

# Tool definition for pattern matching operations
PatternMatchingTool = {
    'type': 'function',
    'function': {
        'name': 'pattern_matching',
        'description': """Perform advanced pattern matching using OpenCog's pattern matcher.
        
        OpenCog's pattern matcher can find complex patterns in knowledge graphs,
        enabling sophisticated cognitive pattern recognition and knowledge discovery:
        
        - Graph pattern matching in AtomSpace
        - Fuzzy pattern matching with confidence values
        - Temporal pattern recognition
        - Hierarchical pattern structures
        - Variable binding and unification
        - Pattern composition and decomposition
        
        Pattern types supported:
        - 'structural': Match structural patterns in knowledge graphs
        - 'temporal': Match temporal sequences and patterns
        - 'semantic': Match semantic relationships and meanings
        - 'behavioral': Match behavioral patterns and sequences
        - 'fuzzy': Fuzzy pattern matching with similarity measures
        - 'compositional': Match complex compositional patterns
        """,
        'parameters': {
            'type': 'object',
            'properties': {
                'pattern_type': {
                    'type': 'string',
                    'enum': ['structural', 'temporal', 'semantic', 'behavioral', 'fuzzy', 'compositional'],
                    'description': 'The type of pattern matching to perform'
                },
                'pattern_specification': {
                    'type': 'object',
                    'description': 'Detailed specification of the pattern to match'
                },
                'search_space': {
                    'type': 'string',
                    'description': 'Domain or context to search for patterns (optional)'
                },
                'similarity_threshold': {
                    'type': 'number',
                    'minimum': 0.0,
                    'maximum': 1.0,
                    'default': 0.8,
                    'description': 'Minimum similarity for fuzzy pattern matching'
                },
                'max_results': {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 100,
                    'default': 10,
                    'description': 'Maximum number of pattern matches to return'
                },
                'include_confidence': {
                    'type': 'boolean',
                    'default': True,
                    'description': 'Whether to include confidence scores with results'
                }
            },
            'required': ['pattern_type', 'pattern_specification']
        }
    }
}
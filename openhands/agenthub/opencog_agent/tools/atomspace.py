"""AtomSpace tool for OpenCog integration.

This tool provides access to AtomSpace operations for knowledge representation
and manipulation within the OpenCog cognitive architecture.
"""

from typing import Any, Dict

# Tool definition for AtomSpace operations
AtomSpaceTool = {
    'type': 'function',
    'function': {
        'name': 'atomspace_operation',
        'description': """Perform operations on the OpenCog AtomSpace knowledge representation system.
        
        The AtomSpace is OpenCog's main knowledge representation framework that stores
        knowledge as a hypergraph of atoms (nodes and links). This tool allows you to:
        
        - Create new atoms (concepts, predicates, relationships)
        - Query existing knowledge structures
        - Perform pattern matching on knowledge graphs
        - Update knowledge with new information
        - Analyze knowledge relationships and dependencies
        
        Operations available:
        - 'create_concept': Create a new concept node
        - 'create_link': Create a link between atoms  
        - 'query': Query the AtomSpace for patterns
        - 'update': Update existing atoms
        - 'analyze': Analyze knowledge structures
        """,
        'parameters': {
            'type': 'object',
            'properties': {
                'operation': {
                    'type': 'string',
                    'enum': ['create_concept', 'create_link', 'query', 'update', 'analyze'],
                    'description': 'The type of AtomSpace operation to perform'
                },
                'data': {
                    'type': 'object',
                    'description': 'Operation-specific data (concept name, link definition, query pattern, etc.)'
                },
                'context': {
                    'type': 'string',
                    'description': 'Context or domain for the operation (optional)'
                }
            },
            'required': ['operation', 'data']
        }
    }
}
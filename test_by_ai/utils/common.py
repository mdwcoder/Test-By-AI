from typing import Any, Dict

def generate_dummy_value(schema: Dict[str, Any]) -> Any:
    """Generate a dummy value based on OpenAPI schema."""
    if not schema:
        return None
        
    type_ = schema.get('type')
    
    if 'example' in schema:
        return schema['example']
    if 'default' in schema:
        return schema['default']

    if type_ == 'string':
        return "string_value"
    elif type_ == 'integer':
        return 1
    elif type_ == 'number':
        return 1.0
    elif type_ == 'boolean':
        return True
    elif type_ == 'array':
        items = schema.get('items', {})
        return [generate_dummy_value(items)]
    elif type_ == 'object':
        props = schema.get('properties', {})
        return {k: generate_dummy_value(v) for k, v in props.items()}
    
    return None

def simple_path_replace(path: str) -> str:
    import re
    return re.sub(r'\{.*?\}', '1', path)

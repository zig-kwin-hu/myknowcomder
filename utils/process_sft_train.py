import json
from collections import defaultdict
from typing import Dict, Set
from tqdm import tqdm
def create_default_stats():
    return {
        'types': set(),           # set of all types encountered for this key
        'count': 0,              # number of times this key appears
        'null_count': 0,         # number of times this key has null value
        'example_values': set(),  # set of example values (limited to 5)
        'min_value': None,       # for numeric values
        'max_value': None        # for numeric values
    }

class JsonStructureAnalyzer:
    def __init__(self, output_file_path=None):
        self.all_paths = defaultdict(create_default_stats)
        self.output_file_path = output_file_path
    def update_stats(self, path: str, value) -> None:
        """Update statistics for a given path and value"""
        stats = self.all_paths[path]
        stats['count'] += 1
        
        # Update type information
        value_type = type(value).__name__
        stats['types'].add(value_type)
        
        # Handle null values
        if value is None or (isinstance(value, str) and value.lower() in ["null", "none"]) \
            or (isinstance(value, list) and len(value) == 0) or (isinstance(value, str) and len(value) == 0):
            stats['null_count'] += 1
            return
            
        # Store example values (limit to 5)
        if len(stats['example_values']) < 5 and value is not None:
            stats['example_values'].add(str(value))
        
        # Update min/max for numeric values
        if isinstance(value, (int, float)):
            if stats['min_value'] is None or value < stats['min_value']:
                stats['min_value'] = value
            if stats['max_value'] is None or value > stats['max_value']:
                stats['max_value'] = value

    def analyze_dict(self, d: Dict, prefix: str = "") -> None:
        """Recursively analyze dictionary structure and store paths"""
        for key, value in d.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                self.all_paths[current_path]['types'].add("dict")
                self.analyze_dict(value, current_path)
            else:
                self.update_stats(current_path, value)

    def print_structure(self) -> None:
        """Print the structure in a tree-like format"""
        towrite = []
        for path in sorted(self.all_paths.keys()):
            depth = path.count('.')
            indent = "  " * depth
            stats = self.all_paths[path]
            
            # Prepare statistics string
            types_str = ", ".join(sorted(stats['types']))
            count_str = f"count: {stats['count']}"
            null_str = f"null: {stats['null_count']}"
            
            # Add min/max for numeric fields
            minmax_str = ""
            if stats['min_value'] is not None:
                minmax_str = f"min: {stats['min_value']}, max: {stats['max_value']}"
            
            # Add example values
            examples_str = ""
            if stats['example_values']:
                examples = list(stats['example_values'])
                if len(examples) > 0:
                    examples_str = f"examples: [{', '.join(examples[:1])}]"
            
            # Combine all statistics
            stats_parts = [s for s in [types_str, count_str, null_str, minmax_str, examples_str] if s]
            stats_str = " | ".join(stats_parts)
            
            print(f"{indent}├─ {path.split('.')[-1]} ({stats_str})")
            towrite.append(f"{indent}├─ {path.split('.')[-1]} ({stats_str})\n")
        if self.output_file_path is not None:
            with open(self.output_file_path, 'w') as f:
                f.writelines(towrite)

def analyze_json_files(input_file_path, output_file_path) -> None:
    analyzer = JsonStructureAnalyzer(output_file_path)
    input_file = open(input_file_path, 'r')
    # show tqdm progress bar
    for line in tqdm(input_file):
        try:
            data = json.loads(line)
            analyzer.analyze_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON line: {e}")
            continue
    
    print("JSON Structure Analysis:")
    print("=======================")
    analyzer.print_structure()

# Example usage
if __name__ == "__main__":
    # Example input
    #input_file_path = "SFT_data/train/sft2_aligned_uie_prompt_v20_guideline_import_v1-ner-all-re-ee-repeat.jsonl"
    tasks = ['EAE','ED','NER','RE']
    for task in tasks:
        input_file_path = f"SFT_data/benchmark/{task}/test-prompt.json"
        output_file_path = f"SFT_data/benchmark/{task}/test-prompt_structure.txt"
        analyze_json_files(input_file_path, output_file_path)
    

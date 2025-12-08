#!/usr/bin/env python3
"""
Script to analyze Python files for unused imports and code elements.
"""

import ast
import sys
from pathlib import Path
from typing import Set, List, Tuple

class UnusedCodeAnalyzer(ast.NodeVisitor):
    """Analyze Python code for unused imports and variables."""

    def __init__(self, filename):
        self.filename = filename
        self.imports = {}  # name -> (lineno, alias)
        self.used_names = set()
        self.functions = {}  # name -> lineno
        self.classes = {}  # name -> lineno
        self.variables = {}  # name -> lineno
        self.used_in_string = set()  # Names used in strings (for dynamic usage)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                self.imports[name] = node.lineno
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions[node.name] = node.lineno
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes[node.name] = node.lineno
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = node.lineno
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Track attribute access
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)

    def analyze(self):
        """Parse and analyze the file."""
        try:
            with open(self.filename, 'r') as f:
                content = f.read()

            tree = ast.parse(content)
            self.visit(tree)

            # Check for unused imports
            unused_imports = []
            for name, lineno in self.imports.items():
                if name not in self.used_names and name not in self.used_in_string:
                    unused_imports.append((name, lineno))

            # Check for unused functions (that aren't entry points)
            unused_functions = []
            entry_points = ['main', 'validate_skill', 'package_skill', 'init_skill',
                          'get_state_manager', 'create_initial_state', 'execute_workflow',
                          'generate_project_id', 'create_project_structure', 'title_case_skill_name']

            for name, lineno in self.functions.items():
                # Skip if used as callable
                if name not in self.used_names and name not in entry_points:
                    unused_functions.append((name, lineno))

            # Check for unused classes
            unused_classes = []
            for name, lineno in self.classes.items():
                if name not in self.used_names:
                    unused_classes.append((name, lineno))

            # Check for unused variables (only simple top-level ones)
            unused_variables = []
            for name, lineno in self.variables.items():
                if name not in self.used_names:
                    # Skip special variables
                    if not name.startswith('_'):
                        unused_variables.append((name, lineno))

            return {
                'unused_imports': unused_imports,
                'unused_functions': unused_functions,
                'unused_classes': unused_classes,
                'unused_variables': unused_variables
            }

        except Exception as e:
            return {'error': str(e)}


def analyze_file(filepath):
    """Analyze a single Python file."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath}")
    print('='*60)

    analyzer = UnusedCodeAnalyzer(filepath)
    results = analyzer.analyze()

    if 'error' in results:
        print(f"Error: {results['error']}")
        return results

    # Display results
    if results['unused_imports']:
        print(f"\nUnused Imports ({len(results['unused_imports'])}):")
        for name, lineno in results['unused_imports']:
            print(f"  Line {lineno}: {name}")

    if results['unused_functions']:
        print(f"\nUnused Functions ({len(results['unused_functions'])}):")
        for name, lineno in results['unused_functions']:
            print(f"  Line {lineno}: {name}")

    if results['unused_classes']:
        print(f"\nUnused Classes ({len(results['unused_classes'])}):")
        for name, lineno in results['unused_classes']:
            print(f"  Line {lineno}: {name}")

    if results['unused_variables']:
        print(f"\nUnused Variables ({len(results['unused_variables'])}):")
        for name, lineno in results['unused_variables']:
            print(f"  Line {lineno}: {name}")

    if not any(results.values()):
        print("\n✓ No unused code found!")

    return results


if __name__ == "__main__":
    python_files = [
        "/d/project/agents/.claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py",
        "/d/project/agents/.claude/skills/blog-master-orchestrator/scripts/state_manager.py",
        "/d/project/agents/.claude/skills/skill-creator/scripts/init_skill.py",
        "/d/project/agents/.claude/skills/skill-creator/scripts/package_skill.py",
        "/d/project/agents/.claude/skills/skill-creator/scripts/quick_validate.py"
    ]

    all_results = {}
    for filepath in python_files:
        results = analyze_file(filepath)
        all_results[filepath] = results

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    total_unused = sum(len(r.get('unused_imports', [])) + len(r.get('unused_functions', []))
                      + len(r.get('unused_classes', [])) + len(r.get('unused_variables', []))
                      for r in all_results.values() if isinstance(r, dict))
    print(f"Total unused code elements found: {total_unused}")

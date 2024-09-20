import os
import re

def read_files_from_directory(directory: str, file_extension: str = '.md') -> list[str]:
    file_contents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents.append(content)
    return file_contents

def extract_ingredients_from_recipes():
    recipes_list = []
    docs_directory = 'docs'

    file_contents = read_files_from_directory(docs_directory)

    for content in file_contents:
        recipe_ingredients = []
        parse_ingredients(content, recipe_ingredients)
        recipes_list.append(recipe_ingredients)

    return recipes_list

def parse_ingredients(content: str, recipe_ingredients: list):
    ingredients_section = False

    for line in content.split('\n'):
        if line.strip().startswith('| Ингредиенты'):
            ingredients_section = True
            continue
        if ingredients_section:
            if line.strip().startswith('|'):
                parts = line.split('|')
                if len(parts) >= 3:
                    name = parts[1].strip()
                    quantity_unit = parts[2].strip()
                    if name and quantity_unit and name != 'Ингредиенты' and not re.search(r'--+', name):
                        quantity_unit_parts = quantity_unit.split()
                        if len(quantity_unit_parts) >= 2:
                            quantity = quantity_unit_parts[0]
                            unit = ' '.join(quantity_unit_parts[1:])
                            recipe_ingredients.append((name, quantity, unit))
                        else:
                            print(f"Error: {name}... {quantity_unit}")
            elif not line.strip():
                break

def extract_steps_from_recipes():
    steps = []
    docs_directory = 'docs'

    file_contents = read_files_from_directory(docs_directory)

    for content in file_contents:
        steps += parse_steps(content)

    return steps

def parse_steps(content: str):
    steps_section = False
    steps = []

    for line in content.split('\n'):
        if line.strip().startswith('### Шаги'):
            steps_section = True
            continue
        if steps_section:
            if re.match(r'\d+\.', line.strip()):
                step_number = int(re.match(r'\d+', line.strip()).group())
                description = line.strip().split('.', 1)[1].strip()
                steps.append((step_number, description))
    return steps

def extract_servings_from_recipes():

    servings_list = []
    docs_directory = 'docs'

    file_contents = read_files_from_directory(docs_directory)

    for content in file_contents:
        servings = parse_servings(content)
        servings_list.append(servings)

    return servings_list

def parse_servings(content: str) -> int:
    servings = 1
    for line in content.split('\n'):
        if 'порций' in line.lower() or 'порции' in line.lower():
            servings_str = re.search(r'(\d+)', line)
            if servings_str:
                servings = int(servings_str.group(1))
            break
    return servings


import os
import re
from src.utils.validator import Validator
from src.core.abstract_logic import abstract_logic
from src.models.recipe import recipe_model
from src.models.ingredient import ingredient_model
from src.models.range import range_model
from src.models.step import step_model
from src.models.nomenclature import nomenclature_model
from src.models.group import group_model
from src.utils.custom_exceptions import NotFoundException, ArgumentException

class recipe_manager(abstract_logic):
    def __init__(self, docs_directory: str = 'docs', file_extension: str = '.md'):
        Validator.validate_not_none(docs_directory, "docs_directory")
        Validator.validate_non_empty(docs_directory, "docs_directory")
        Validator.validate_non_empty(file_extension, "file_extension")
        self.docs_directory = docs_directory
        self.file_extension = file_extension
        self.nomenclature_cache = {}
        self.unit_cache = {}

    def read_files(self) -> list[str]:
        """Чтение всех файлов с рецептами из директории с тщательной проверкой ошибок."""
        file_contents = []
        Validator.validate_exists(self.docs_directory, "Директория")
        Validator.validate_is_directory(self.docs_directory, "Директория")

        for root, _, files in os.walk(self.docs_directory):
            for file in files:
                Validator.validate_file_extension(file, self.file_extension)
                file_path = os.path.join(root, file)
                Validator.validate_read_permission(file_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_contents.append(content)
                except FileNotFoundError:
                    raise NotFoundException(f"Файл '{file_path}' не найден")
                except PermissionError:
                    raise PermissionError(f"Нет прав для чтения файла: {file_path}")
                except Exception as ex:
                    raise ArgumentException(file_path, f"Ошибка при чтении файла: {str(ex)}")

        return file_contents

    def extract_title(self, content: str) -> str:
        """Извлечение названия рецепта из содержимого."""
        for line in content.split('\n'):
            if line.strip().startswith('# '):
                return line.strip()[2:]
        return "Неизвестный рецепт"



    def extract_nomenclature(self) -> dict[str, range_model]:
        """Извлечение номенклатуры и их единиц измерения из всех рецептов."""
        nomenclature_dict = {}
        file_contents = self.read_files()

        for content in file_contents:
            recipe_ingredients = []
            self.parse_ingredients(content, recipe_ingredients)

            for ingredient in recipe_ingredients:
                name, _, unit_name = ingredient

                if name not in self.nomenclature_cache:
                    nomenclature = nomenclature_model()
                    nomenclature.name = name
                    self.nomenclature_cache[name] = nomenclature
                else:
                    nomenclature = self.nomenclature_cache[name]

                if unit_name not in self.unit_cache:
                    unit = range_model()
                    unit.name = unit_name
                    self.unit_cache[unit_name] = unit
                else:
                    unit = self.unit_cache[unit_name]

                nomenclature_dict[name] = unit

        return nomenclature_dict

    def extract_ingredients(self) -> list[list[tuple[str, str, str]]]:
        """Извлечение ингредиентов из всех рецептов."""
        recipes_list = []
        file_contents = self.read_files()

        for content in file_contents:
            recipe_ingredients = []
            self.parse_ingredients(content, recipe_ingredients)
            recipes_list.append(recipe_ingredients)

        return recipes_list

    def parse_ingredients(self, content: str, recipe_ingredients: list):
        """Парсинг ингредиентов из содержимого одного рецепта."""
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

                        if re.search(r'----+', quantity_unit) or re.search(r'----+', name):
                            continue

                        Validator.validate_non_empty(name, "Название ингредиента")
                        Validator.validate_non_empty(quantity_unit, "Количество и единица измерения")
                        
                        quantity_unit_parts = quantity_unit.split()
                        Validator.validate_quantity_unit_format(quantity_unit_parts, "Количество и единица измерения")
                        quantity = quantity_unit_parts[0]
                        unit = ' '.join(quantity_unit_parts[1:])
                        
                        Validator.validate_positive_float(float(quantity), "Количество")
                        recipe_ingredients.append((name, quantity, unit))
                elif not line.strip():
                    break

    def extract_steps(self) -> list[tuple[int, str]]:
        """Извлечение шагов приготовления из всех рецептов."""
        steps = []
        file_contents = self.read_files()

        for content in file_contents:
            steps += self.parse_steps(content)

        return steps

    def parse_steps(self, content: str) -> list[tuple[int, str]]:
        """Парсинг шагов приготовления из содержимого одного рецепта."""
        steps_section = False
        steps = []

        for line in content.split('\n'):
            if line.strip().startswith('## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ'):
                steps_section = True
                continue
            if steps_section:
                if re.match(r'\d+\.', line.strip()):
                    step_number = int(re.match(r'\d+', line.strip()).group())
                    description = line.strip().split('.', 1)[1].strip()
                    steps.append((step_number, description))
        return steps

    def extract_servings(self) -> list[int]:
        """Извлечение количества порций из всех рецептов."""
        servings_list = []
        file_contents = self.read_files()

        for content in file_contents:
            servings = self.parse_servings(content)
            servings_list.append(servings)

        return servings_list

    def parse_servings(self, content: str) -> int:
        """Парсинг количества порций из содержимого одного рецепта."""
        servings = 1
        for line in content.split('\n'):
            if 'порций' in line.lower() or 'порции' in line.lower():
                servings_str = re.search(r'(\d+)', line)
                if servings_str:
                    servings = int(servings_str.group(1))
                break
        return servings

    def load_all_recipes(self) -> list[dict]:
        """Загрузка всех рецептов, включая ингредиенты, шаги и порции."""
        file_contents = self.read_files()
        all_recipes = []

        for content in file_contents:
            recipe_data = {
                'name': self.extract_title(content),
                'ingredients': [],
                'steps': [],
                'servings': self.parse_servings(content),
            }

            self.parse_ingredients(content, recipe_data['ingredients'])
            recipe_data['steps'] = self.parse_steps(content)

            all_recipes.append(recipe_data)

        return all_recipes
    
    def create_recipes(self, recipe_data_list: list[dict]) -> list[recipe_model]:
        recipes = []

        for recipe_data in recipe_data_list:
            recipe = recipe_model()
            recipe.name = recipe_data.get('name', "Неизвестный рецепт")
            recipe.servings = recipe_data.get('servings', 1)

            for ingredient_info in recipe_data.get('ingredients', []):
                name, quantity, unit_name = ingredient_info

                nomenclature = self.nomenclature_cache.get(name)
                if not nomenclature:
                    nomenclature = nomenclature_model()
                    nomenclature.name = name
                    self.nomenclature_cache[name] = nomenclature

                unit = self.unit_cache.get(unit_name)
                if not unit:
                    unit = range_model()
                    unit.name = unit_name
                    self.unit_cache[unit_name] = unit

                ingredient = ingredient_model()
                ingredient.nomenclature = nomenclature
                ingredient.quantity = quantity

                recipe.add_ingredient(ingredient)

            for step_number, description in recipe_data.get('steps', []):
                step = step_model()
                step.step_number = step_number
                step.description = description
                recipe.add_step(step)

            recipes.append(recipe)

        return recipes

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

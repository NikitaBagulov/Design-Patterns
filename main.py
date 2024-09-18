from src.settings_manager import settings_manager
manager1 = settings_manager()
if not manager1.open("settings.json"):
    print("Настройки не загружены!")

print(f"settings1: {manager1.settings.organization_name}")


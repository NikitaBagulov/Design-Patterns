from settings_manager import settings_manager
manager1 = settings_manager()
if not manager1.open("settings.json"):
    print("Настройки не загружены!")

print(f"settings1: {manager1.settings.organization_name}")

manager2 = settings_manager()
print(f"settings2: {manager2.settings.organization_name}")

import requests
import json

# Адрес вашего Flask-сервера и секретный ключ (должен совпадать с сервером)
URL = "http://127.0.11:5000/admincontrol"
HEADERS = {
    "X-Admin-Token": "MIL$|7*kHN93",
    "Content-Type": "application/json"
}

print("=== ВНЕШНЯЯ АДМИНИСТРАТИВНАЯ КОНСОЛЬ ЧАТА ===")
print("Введите 'status', 'save', 'msg <текст>' или 'exit' для выхода.\n")

while True:
    cmd = input("Admin >>> ").strip()

    if not cmd:
        continue
        
    if cmd.lower() == "exit":
        print("Закрытие консоли.")
        break
        
    # Формируем JSON-пакет данных
    payload = {"command": cmd}
    
    try:
        # Отправляем HTTP POST пакет на сервер
        response = requests.post(URL, data=json.dumps(payload), headers=HEADERS)
        
        # Разбираем ответ от сервера
        if response.status_code == 200:
            result = response.json()
            print(f"[СЕРВЕР]: {json.dumps(result, indent=2, ensure_ascii=False)}")
        elif response.status_code == 403:
            print("[ОШИБКА]: Ошибка авторизации. Неверный секретный ключ!")
        else:
            print(f"[ОШИБКА]: Сервер вернул код {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("[ОШИБКА]: Не удалось подключиться к серверу. Убедитесь, что Flask запущен!")
    print() # Пустая строка для красоты

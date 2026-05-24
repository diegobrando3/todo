import sys
import json
from datetime import datetime

DOSYA = "todos.json"

# Görevleri oku
def load_todos():
    try:
        with open(DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []   # dosya yoksa veya hata olursa boş liste dön

# Görevleri kaydet
def save_todos(todos):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

# ===================== ANA KISIM =====================
todos = load_todos()

if len(sys.argv) < 2:
    print("Kullanım: python main.py add | list | done | delete | clear")
    sys.exit()

komut = sys.argv[1].lower()

if komut == "add":
    if len(sys.argv) < 3:
        print("Görev yaz: python main.py add \"Görev içeriği\"")
    else:
        gorev = " ".join(sys.argv[2:])
        todos.append({
            "id": len(todos) + 1,
            "gorev": gorev,
            "tamam": False,
            "tarih": datetime.now().strftime("%d.%m %H:%M")
        })
        save_todos(todos)
        print(f"✅ Eklendi: {gorev}")

elif komut == "list":
    if not todos:
        print("Henüz görev yok")
    else:
        for t in todos:
            isaret = "✅" if t["tamam"] else "⬜"
            print(f"{t['id']:2d}. {isaret} {t['gorev']}  ({t['tarih']})")

elif komut == "done":
    if len(sys.argv) > 2:
        try:
            id = int(sys.argv[2])
            for t in todos:
                if t["id"] == id:
                    t["tamam"] = True
                    print(f"✅ Tamamlandı: {t['gorev']}")
                    save_todos(todos)
                    break
        except:
            print("Geçerli sayı gir lan")

elif komut == "delete":
    if len(sys.argv) > 2:
        try:
            id = int(sys.argv[2])
            todos = [t for t in todos if t["id"] != id]
            save_todos(todos)
            print(f"🗑️ {id} numaralı görev silindi")
        except:
            print("Geçerli id gir")

elif komut == "clear":
    confirm = input("Tüm görevleri silmek istediğinden emin misin? (e/h): ")
    if confirm.lower() == "e":
        todos.clear()
        save_todos(todos)
        print("Her şey silindi.")

else:
    print("Bilinmeyen komut. add, list, done, delete, clear yaz")

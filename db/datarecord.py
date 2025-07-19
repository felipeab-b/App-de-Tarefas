import json
import os

users_file = 'db/users.json'

# === Vai ler os dados do json e usar o .load para transformar em um dict ===
def load_users():
    if not os.path.exists(users_file):
        return {}
    with open(users_file, 'r') as f:
        return json.load(f)

# === Função que vai abrir o dict dos users no mode de write(w) e vai voltar para json ===
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# === Linha para testar ===
# users = load_users()
# print(f"Caminho do arquivo: {os.path.abspath(users_file)}")
# print(users)

# === As mesmas funções mas agora tratando do json das tasks ===

tasks_file = 'db/tasks.json'

def load_tasks():
    if not os.path.exists(tasks_file):
        return {}
    with open(tasks_file, 'r') as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=4)
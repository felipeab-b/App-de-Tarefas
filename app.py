from flask import Flask, render_template, request, session, redirect, url_for
from db.datarecord import load_users, save_users, load_tasks, save_tasks

app = Flask(__name__)
app.secret_key = 'segredo'

@app.route('/')
def home():
    return render_template("home.html")

# === Rota aceita GET para "chamar a página" e POST para enviar o formulario ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    # === Se o form for enviado (requisição POST), recebe as entradas dos inputs ===
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        users = load_users()

        # === Verifica se o usuario existe dentro do json e se a senha corresponde a entrada do input ===
        # === Caso sim, guarda o user na session, é como uma var global que dura enquanto estiver logado ===
        if user in users and users[user]['password'] == password:
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

    # === Resultado da requisição GET
    return render_template("login.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # === Verifica se o user tem uma session, portanto está logado, e caso não, retorna o login ===
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    tasks = load_tasks()
    tasks_user = tasks.get(user, [])

    if request.method == 'POST':
        task = request.form['add']
        feito = False
        tasks[user].append({
            'title':task,
            'feito':feito
        })
        save_tasks(tasks)
        return redirect(url_for('dashboard'))

    total_de_tasks = len(tasks_user)
    total_de_feitas = sum(1 for t in tasks_user if t.get('feito'))
    porcentagem = int((total_de_feitas/total_de_tasks) * 100) if total_de_tasks > 0 else 0

    return render_template("dashboard.html", user=user, tasks=tasks_user, total=total_de_tasks, feitas=total_de_feitas,porcentagem=porcentagem)

@app.route('/feito', methods=['POST'])
def feito():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    tasks = load_tasks()
    # === Pega do form o valor do index da tarefa ===
    task_index = int(request.form['task_idx'])

    # === Verifica se o user existe no json das taks e se o idx é válido ===
    if user in tasks and 0 <= task_index < len(tasks[user]):
        tasks[user][task_index]['feito'] = not tasks[user][task_index]['feito']
        save_tasks(tasks)

    return redirect(url_for('dashboard'))

@app.route('/apagar', methods=['POST'])
def apagar():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    tasks = load_tasks()
    index = int(request.form['task-idx'])

    if user in tasks and 0 <= index < len(tasks[user]):
        tasks[user].pop(index)
        save_tasks(tasks)

    return redirect(url_for('dashboard'))

@app.route('/editar', methods=['POST'])
def editar_nome():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    tasks = load_tasks()
    new_title = request.form['input-new-name']
    index = int(request.form['task-idx'])

    if user in tasks and 0 <= index < len(tasks[user]):
        tasks[user][index]['title'] = new_title
        save_tasks(tasks)

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        users = load_users()

        if user in users:
            return 'Usuário já existe!'
        else:
            # === Escreve os novos dados no json, que foi transformado em dict pelo metodo load ===
            users[user] = {
                'username':user,
                'password':password
            }
            # === Salva os novos dados do dict, e transforma de volta para json ===
            save_users(users)
            return redirect(url_for('login'))

    return render_template("registro.html")

@app.route('/stats')
def stats():
    return 'stats'

if __name__ == "__main__":
    app.run(debug=True)
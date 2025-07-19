from flask import Flask, render_template, request, session, redirect, url_for
from db.datarecord import load_users, save_users, load_tasks

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

@app.route('/dashboard')
def dashboard():
    # === Verifica se o user tem uma session, portanto está logado, e caso não, retorna o login ===
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    tasks = load_tasks()
    tasks_user = tasks.get(user, [])

    return render_template("dashboard.html", user=user, tasks=tasks_user)

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
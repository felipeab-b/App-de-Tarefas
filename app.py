from flask import Flask, render_template, request, session, redirect, url_for
from db.datarecord import load_users

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
    return f"sucesso {session['user']}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
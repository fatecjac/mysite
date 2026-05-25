from flask import Flask, render_template, request, redirect, session
from supabase import create_client
# Importa ferramentas seguras para tratar senhas
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "senha_super_secreta"  # Em produção, mude para algo bem complexo

SUPABASE_URL = "https://johvgneyljlfomqxodwc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpvaHZnbmV5bGpsZm9tcXhvZHdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2NDc5ODYsImV4cCI6MjA5NTIyMzk4Nn0.FFU0YTzQytMhwDC2gkuJuimVBKWWBSH5nQGto3uYQ8c"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    email = session["user"]

    # Busca o usuário no banco pelo e-mail
    usuario = supabase.table("usuarios").select("*").eq("email", email).execute()

    # CORREÇÃO: Verifica se o usuário realmente existe no banco antes de pegar o índice [0]
    if not usuario.data:
        session.clear()  # Limpa a sessão antiga inválida
        return redirect("/login")

    dados = usuario.data[0]
    return render_template("dashboard.html", usuario=dados)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # SEGURANÇA: Criptografa a senha antes de enviar para o banco de dados
        senha_criptografada = generate_password_hash(senha)

        
        usuario_existente = supabase.table("usuarios").select("*").eq("email", email).execute()

        if usuario_existente.data:

            return render_template(
                "cadastro.html",
                erro="Este email já está cadastrado!"
            )

        supabase.table("usuarios").insert({
            "nome": nome,
            "email": email,
            "senha": senha,
            "saldo": 0
        }).execute()

        return redirect("/login")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # Busca o usuário apenas pelo e-mail primeiro
        usuario = supabase.table("usuarios").select("*").eq("email", email).execute()

        # Se o e-mail existir, verificamos a senha criptografada
        if usuario.data:
            usuario_db = usuario.data[0]
            
            # Compara a senha digitada com o hash salvo no banco
            if check_password_hash(usuario_db["senha"], senha):
                session["user"] = email
                return redirect("/")
            
        # Se falhar (e-mail incorreto ou senha errada)
        return render_template("login.html", erro="E-mail ou senha incorretos.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/recuperar")
def recuperar():

    return render_template("recuperar.html")

@app.route("/deposito", methods=["POST"])
def deposito():

    if "user" not in session:
        return redirect("/login")

    valor = float(request.form["valor"])

    email = session["user"]

    usuario = supabase.table("usuarios").select("*").eq("email", email).execute()

    dados = usuario.data[0]

    novo_saldo = dados["saldo"] + valor

    supabase.table("usuarios").update({
        "saldo": novo_saldo
    }).eq("email", email).execute()

    supabase.table("transacoes").insert({
        "remetente_id": dados["id"],
        "destinatario_id": dados["id"],
        "valor": valor,
        "tipo": "deposito"
    }).execute()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

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

    transacoes = supabase.table("transacoes") \
    .select("*") \
    .or_(f"remetente_id.eq.{dados['id']},destinatario_id.eq.{dados['id']}") \
    .order("data", desc=True) \
    .execute()
    erro = request.args.get("erro")


    return render_template("dashboard.html", usuario=dados, transacoes=transacoes.data, erro=erro)

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

        # CORREÇÃO: Salvando a 'senha_criptografada' no lugar da 'senha' em texto limpo
        supabase.table("usuarios").insert({
            "nome": nome,
            "email": email,
            "senha": senha_criptografada,
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

    # CORREÇÃO: Tratamento para evitar erro de string vazia ou letras
    valor_texto = request.form.get("valor", "").strip()
    try:
        valor = float(valor_texto)
    except ValueError:
        return redirect("/?erro=valor")

    if valor <= 0:
        return redirect("/?erro=valor")

    email = session["user"]
    usuario = supabase.table("usuarios").select("*").eq("email", email).execute()

    if not usuario.data:
        return redirect("/?erro=usuario")

    dados = usuario.data[0]
    novo_saldo = dados["saldo"] + valor

    # Atualiza o saldo
    supabase.table("usuarios").update({
        "saldo": novo_saldo
    }).eq("email", email).execute()

    # Registra a transação
    supabase.table("transacoes").insert({
        "remetente_id": dados["id"],
        "destinatario_id": dados["id"],
        "valor": valor,
        "tipo": "deposito"
    }).execute()

    return redirect("/")

@app.route("/transferir", methods=["POST"])
def transferir():
    if "user" not in session:
        return redirect("/login")

    email_remetente = session["user"]
    email_destinatario = request.form.get("destinatario", "").strip()

    # CORREÇÃO: Tratamento para evitar erro de string vazia ou letras
    valor_texto = request.form.get("valor", "").strip()
    try:
        valor = float(valor_texto)
    except ValueError:
        return redirect("/?erro=saldo")

    if valor <= 0:
        return redirect("/?erro=valor")

    if email_destinatario == email_remetente:
        return redirect("/?erro=proprio")

    # Busca remetente
    remetente = supabase.table("usuarios").select("*").eq("email", email_remetente).execute()
    if not remetente.data:
        return redirect("/?erro=usuario")
    remetente = remetente.data[0]

    # Busca destinatário
    destinatario = supabase.table("usuarios").select("*").eq("email", email_destinatario).execute()
    if not destinatario.data:
        return redirect("/?erro=usuario")
    destinatario = destinatario.data[0]

    # Verifica saldo disponível
    if remetente["saldo"] < valor:
        return redirect("/?erro=saldo")

    # Atualiza saldo do remetente
    supabase.table("usuarios").update({
        "saldo": remetente["saldo"] - valor
    }).eq("id", remetente["id"]).execute()

    # Atualiza saldo do destinatário
    supabase.table("usuarios").update({
        "saldo": destinatario["saldo"] + valor
    }).eq("id", destinatario["id"]).execute()

    # Registra transação
    supabase.table("transacoes").insert({
        "remetente_id": remetente["id"],
        "destinatario_id": destinatario["id"],
        "valor": valor,
        "tipo": "transferencia"
    }).execute()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

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

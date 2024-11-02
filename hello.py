from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app = Flask(__name__)
app.secret_key = "peixefrito123"  #senha para os cookies de sessão

# Configuração do servidor de e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'xxxx@gmail.com'
app.config['MAIL_PASSWORD'] = 'código 16 dígitos do google'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Serializador para gerar os tokens seguros
s = URLSafeTimedSerializer(app.secret_key)

# Código Principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para solicitar redefinição de senha
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Aqui vocês irão verificar no BD se o email recebido é válido,
        # ou seja, se é um usuário do sistema

        # preparação e envio do email
        token = s.dumps(email, salt='password_recovery')
        msg = Message('Redefinição de senha', \
                      sender='xxx@gmail.com', \
                      recipients=[email])
        link = url_for('reset_password', token=token, _external=True)
        msg.body = f'Clique no link para redefinir a sua senha: {link}'
        mail.send(msg)

        flash('Um link de recuperação de senha foi enviado para o seu email', \
              category='success')

        return redirect(url_for('index'))

    return render_template('forgot_password.html')

# Rota para redefinir a senha
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password_recovery', max_age=3600) # 1h
    except SignatureExpired:
        return '<h1>O link de redefinição de senha expirou</h1>'
    except BadSignature:
        return '<h1>Token inválido</h1>'
    if request.method == 'POST':
        new_password = request.form['password']
        # Neste ponto você faria um update no registro do usuário com a nova senha
        flash('Sua senha foi redefinida com sucesso!!', category='success')
        return redirect(url_for('index'))
    return render_template('reset_password.html')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verification_code = random.randint(100000, 999999)

        conn = get_db_connection()
        conn.execute('INSERT INTO users (email, password, verification_code, verified) VALUES (?, ?, ?, ?)', 
                     (email, generate_password_hash(password, method='sha256'), verification_code, False))
        conn.commit()
        conn.close()
        
        send_verification_code(email, verification_code)
        
        session['email'] = email
        flash('Se ha enviado un código de verificación a tu correo.', 'info')
        return redirect(url_for('verify'))
    return render_template('register.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        email = session.get('email')
        code = request.form['code']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND verification_code = ?', (email, code)).fetchone()
        
        if user:
            conn.execute('UPDATE users SET verified = 1 WHERE email = ?', (email,))
            conn.commit()
            conn.close()
            flash('Tu correo ha sido verificado. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Código de verificación inválido. Inténtalo de nuevo.', 'danger')
    return render_template('verify.html')
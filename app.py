from flask import Flask, request, render_template, redirect, url_for 
from config import Config
from flask_mysqldb import MySQL


app = Flask(__name__)

#config
app.config.from_object(Config)
mysql = MySQL(app)

#Data Read
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM student_data ")
    student_data = cur.fetchall()
    cur.close()
    return render_template('index.html', student_data = student_data)

#Data Add
@app.route('/add', methods=['GET','POST'])
def add_students():
    if request.method == "POST":
        id= request.form.get('id')
        name= request.form.get('name')
        email= request.form.get('email')
        course= request.form.get('course')
        
        cur= mysql.connection.cursor()
        cur.execute(
            "INSERT INTO student_data(id, name, email, course) VALUE(%s, %s, %s, %s)",
            (id, name, email, course)
        )
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))

    return render_template('add.html')

#Data  Update
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_students(id):
    cur= mysql.connection.cursor()

    if request.method == 'POST':
        name= request.form.get('name')
        email= request.form.get('email')
        course= request.form.get('course')

        cur.execute(
            """
                UPDATE student_data 
                SET name=%s, email=%s, course=%s
                WHERE id=%s

            """,(name,email,course, id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur.execute(" SELECT * FROM student_data WHERE id = %s", (id,))

        student_data= cur.fetchone()
        cur.close
    return render_template('edit.html', student_data= student_data)

#Data Delete
@app.route('/delete/<int:id>')
def delete_students(id):
    cur= mysql.connection.cursor()
    cur.execute(" DELETE FROM student_data WHERE id= %s ", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
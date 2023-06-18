from flask import Flask, render_template, request
import mysql.connector
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nagasai12p",
    database="pnm"
)

cursor = db.cursor()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("INSERT INTO employees (name, email) VALUES (%s, %s)", (name, email))
        db.commit()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    return render_template('employees.html', employees=employees)

@app.route('/payroll', methods=['GET', 'POST'])
def payroll():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        hours_worked = float(request.form['hours_worked'])
        hourly_rate = float(request.form['hourly_rate'])
        deductions = float(request.form['deductions'])
        pay_date = datetime.date.today().strftime('%Y-%m-%d')

        gross_salary = hours_worked * hourly_rate
        net_salary = gross_salary - deductions

        cursor.execute("INSERT INTO payroll (employee_id, hours_worked, hourly_rate, deductions, gross_salary, net_salary, pay_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               (employee_id, hours_worked, hourly_rate, deductions, gross_salary, net_salary, pay_date))
        db.commit()

    cursor.execute("SELECT employees.id, employees.name, employees.email, payroll.hours_worked, payroll.hourly_rate, payroll.deductions, payroll.gross_salary, payroll.net_salary, payroll.pay_date FROM employees INNER JOIN payroll ON employees.id = payroll.employee_id")
    payroll = cursor.fetchall()

    return render_template('payroll.html', payroll=payroll)

if __name__ == '__main__':
    app.run(debug=True)
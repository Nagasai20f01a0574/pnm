from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date

app = Flask(__name__)

# MySQL database connection configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nagasai12p",
    database="pnm"
)
cursor = db.cursor()


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Add Employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = float(request.form['salary'])

        # Insert employee data into the database
        query = "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)"
        values = (name, position, salary)
        cursor.execute(query, values)
        db.commit()

        return redirect('/employees')
    return render_template('add_employee.html')


# Employees List
@app.route('/employees')
def employees():
    query = "SELECT * FROM employees"
    cursor.execute(query)
    employees = cursor.fetchall()
    return render_template('employees.html', employees=employees)


# Payroll Calculation
@app.route('/payroll', methods=['GET', 'POST'])
def calculate_payroll():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        hours_worked = float(request.form['hours_worked'])
        deductions = float(request.form['deductions'])

        # Fetch employee salary from the database
        query = "SELECT salary FROM employees WHERE id = %s"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()

        if result:
            salary = float(result[0])
            gross_salary = hours_worked * salary
            net_salary = gross_salary - deductions
            pay_date = date.today()
            # Insert payroll data into the database
            query = "INSERT INTO payroll (employee_id, hours_worked, hourly_rate, deductions, gross_salary, net_salary, pay_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (employee_id, hours_worked, salary, deductions, gross_salary, net_salary, pay_date)
            cursor.execute(query, values)
            db.commit()

            return redirect('/payroll')
        else:
            return "Employee not found"
    
    query = "SELECT p.*, e.name FROM payroll p JOIN employees e ON p.employee_id = e.id"
    cursor.execute(query)
    payroll_data = cursor.fetchall()
    return render_template('payroll.html', payroll_data=payroll_data)


if __name__ == '__main__':
    app.run(debug=True)
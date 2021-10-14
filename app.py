from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abcdef'

# initialize database
db = SQLAlchemy(app)

#  Crete db model


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    departmentId = db.Column(db.Integer, nullable=True)


class Department(db.Model):
    __tablename__ = 'departments'
    departmentId = db.Column(db.Integer, primary_key=True)
    departmentname = db.Column(db.String(50), nullable=True)


def __rep__(self):
    return '<Name>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        employeeid = request.form['employeeId']
        try:
            employees = Employee.query.get_or_404(employeeid)
        except:
            message = 'No Employee Exist'
            return render_template("index.html", message=message)
        try:
            department = Department.query.get_or_404(employees.departmentId)
        except:
            return render_template("index.html", employeeName=employees.name)

        return render_template("index.html", employeeName=employees.name, departmentName=department.departmentname)

    else:
        return render_template("index.html")


@app.route('/addEmployee', methods=['GET', 'POST'])
def addEmployee():
    employees = Employee.query.filter().all()
    if request.method == "POST":
        id = request.form['employeeId']
        name = request.form['employeeName']
        depId = request.form['departmentId']

        new_employee = Employee(id=id, name=name, departmentId=depId)

        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect('/addEmployee')
        except:
            return "There was an error while adding employee"
    else:
        return render_template("addEmployee.html", employees=employees)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    employeeid = Employee.query.get_or_404(id)
    if request.method == "POST":
        employeeid.name = request.form['employeeName']
        employeeid.departmentId = request.form['departmentId']
        try:
            db.session.commit()
            return redirect('/addEmployee')
        except:
            return "There was an error while updating employee"
    else:
        return render_template("updateEmployee.html", employee=employeeid)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    employee_tp_delete = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee_tp_delete)
        db.session.commit()
        return redirect('/addEmployee')
    except:
        return "There was an error while deleting employee"


@app.route('/addDepartment', methods=['GET', 'POST'])
def addDepartment():
    departments = Department.query.filter().all()
    if request.method == "POST":
        id = request.form['departmentId']
        name = request.form['departmentName']

        new_department = Department(departmentId=id, departmentname=name)

        try:
            db.session.add(new_department)
            db.session.commit()
            return redirect('/addDepartment')
        except:
            return "There was an error while adding department"
    else:
        return render_template("addDepartment.html", departments=departments)


@app.route('/updateDep/<int:id>', methods=['GET', 'POST'])
def updateDep(id):
    departmentid = Department.query.get_or_404(id)
    if request.method == "POST":
        departmentid.departmentname = request.form['departmentName']
        try:
            db.session.commit()
            return redirect('/addDepartment')
        except:
            return "There was an error while updating department"
    else:
        return render_template("updateDepartment.html", department=departmentid)


@app.route('/deleteDep/<int:id>', methods=['GET', 'POST'])
def deleteDep(id):
    department_to_delete = Department.query.get_or_404(id)
    try:
        db.session.delete(department_to_delete)
        db.session.commit()
        return redirect('/addDepartment')
    except:
        return "There was an error while deleting department"


if __name__ == '__main__':
    app.run(debug=True)

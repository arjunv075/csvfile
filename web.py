import flask
from flask import render_template,request,redirect,url_for
from flask_cors import CORS
import models
from sqlalchemy import func


app = flask.Flask("hrms")
CORS(app)
db = models.SQLAlchemy(model_class = models.HRDBBase)

@app.route("/")
def index():
  if flask.request.method == "GET":
    return flask.render_template("index.html")
  
 
@app.route("/employees")
def employees():
    employees = db.select(models.Employee).order_by(models.Employee.firstname)
    users = db.session.execute(employees).scalars()
    ret =[]
    for user in users:
       emp_list= {
                      "id": user.empid,
                      "firstname" : user.firstname,
                      "lastname" : user.lastname,
                      "title" : user.title.title,
                      "email" : user.email,
                      "phone" : user.ph_no}
       ret.append(emp_list)
    return flask.jsonify(ret)

  
@app.route("/employees/<int:empid>")
def employee_details(empid):
  employees = db.select(models.Employee).where(models.Employee.empid == empid)
  user = db.session.execute(employees).scalar()
  emp_count = db.select(func.count(models.Employee.empid)).join(models.Leaves,models.Employee.empid == models.Leaves.empid).where(models.Employee.empid==empid)
  leaves = db.session.execute(emp_count).scalar()
  leave_count = db.select(models.Designation.max_leaves).where(models.Designation.jobid == models.Employee.title_id, models.Employee.empid==empid)
  max_leaves = db.session.execute(leave_count).scalar()
  ret=[]
  emp_details = {"employee_id" : user.empid,
         "firstname" : user.firstname,
         "lastname" : user.lastname,
         "title" : user.title.title,
         "email" : user.email,
         "phone" : user.ph_no,
         "leaves": leaves,
         "max_leaves" : max_leaves
  }
  ret.append(emp_details)
  return flask.jsonify(ret)

@app.errorhandler(500)   
def page_not_found(error):
    return render_template('500.html'), 500

@app.errorhandler(404)   
def page_not_found(error):
    return render_template('404.html'), 404


@app.route("/leave/<int:empid>", methods=["GET", "POST"])
def addleave(empid):
  if request.method == "POST":
    data = request.get_json()
    date = data.get('date')
    reason = data.get('reason')
    if not date or not reason:
       return flask.jsonify({'error': 'Enter data'}), 400
    insert_data = models.Leaves(empid=empid ,date=date, reason=reason)
    db.session.add(insert_data)
    db.session.commit()
    return flask.jsonify({'message': 'Leave Posted'}), 200
  return flask.jsonify({'error': 'Function Not Allowed'}), 405
  
@app.route("/about")
def about():
  return render_template("about.html")

  
from flask import Blueprint, jsonify, request
import json

from ..database.prototype_database import db, Random, AppMetrics

test_routes = Blueprint('test_routes',__name__)

@test_routes.route("/testone", methods=['POST'])
def test_one():
  new_data = request.data
  print(new_data.decode("utf-8"))
  test_one = Random(msg=new_data.decode("utf-8"))

  db.session.add(test_one)
  db.session.commit()

  return "Data added successfully"

@test_routes.route("/testget")
def test_get():
  data = Random.query.all()

  final = []
  first = True
  for d in data:
    final.append({"id": d.id, "message": d.msg})


  return jsonify({
    "description": "Random Messages",
    "content": final
  })

@test_routes.route("/testdata")
def test_data():
  result = jsonify({
    "content": "Data Stream",
    "machine": "WinNet01",
    "app_metrics": [
      {"app_name": "Discord","app_cpu": "50%","app_ram": "13%"},
      {"app_name": "Word","app_cpu": "3%","app_ram": "7%"},
      {"app_name": "Chrome","app_cpu": "1%","app_ram": "All of it"}
    ],
    "sys_metrics": {"cpu": "72%","ram": "65%","disk_read": "20%","disk_write": "6%","network": "24%"}
  })

  #final = json.loads(result.get_data().decode("utf-8"))
  return result

@test_routes.route("/getmachines")
def get_machines():
  result = jsonify({
    "description": "Connected Machines",
    "content": [
      {"id": "1", "machine_name": "miz007","machine_type": "windows","time": "14:53:38, 09/04/2021", "status": "Connected","ip_address": "127.0.0.1", "cpu": "22","ram": "45"},
      {"id": "2", "machine_name": "Brock-PC","machine_type": "linux", "time": "14:53:38, 09/04/2021","status": "Connected","ip_address": "127.0.0.2", "cpu": "37","ram": "55"},
      {"id": "3", "machine_name": "keeganator","machine_type": "linux", "time": "14:53:38, 09/04/2021","status": "Disconnected","ip_address": "127.0.0.4", "cpu": "52","ram": "35"},
      {"id": "4", "machine_name": "AlexCompSci","machine_type": "windows", "time": "14:53:38, 09/04/2021","status": "Connected","ip_address": "127.0.0.5", "cpu": "12","ram": "26"},
      {"id": "5", "machine_name": "Voidlord13","machine_type": "linux", "time": "14:53:38, 09/04/2021","status": "Disconnected","ip_address": "127.0.0.6", "cpu": "42","ram": "15"},
      {"id": "6", "machine_name": "Myron-PC","machine_type": "linux", "time": "14:53:38, 09/04/2021","status": "Disconnected","ip_address": "127.0.0.6", "cpu": "42","ram": "15"},
    ]
  })
  return result

@test_routes.route("/addmetrics", methods=["POST"])
def add_metrics():
  new_metrics = request.data
  final_metrics = new_metrics.decode("utf-8")

  obj = json.loads(final_metrics)

  print(obj["machine_name"])

  for app in obj["app_metrics"]:
    db_metric = AppMetrics(machine_name=obj["machine_name"],timestamp=obj["collection_time"],app_name=app["name"],app_cpu=app["cpu"],app_ram=app["ram"])
    db.session.add(db_metric)

  db.session.commit()

  return "New Metrics Successfully added"

@test_routes.route("/getmetrics", methods=["GET"])
def get_metrics():
  data = AppMetrics.query.all()

  final = []
  for d in data:
    final.append({"id": d.id, "machine_name": d.machine_name, "time": d.timestamp, "app_name": d.app_name, "app_cpu": d.app_cpu, "app_ram": d.app_ram})


  return jsonify({
    "description": "Application Machine Metrics",
    "content": final
  })

  return "Metrics received!!"

#
#  This file holds all the relevant routes and functionality
#  for the commands page in the React frontend and command handling on the agent
#

#Import from third party modules
from flask import Blueprint, jsonify, request
import json, ipaddress, socket, time
from datetime import datetime

#Import from in house modules
from ..database.database_tables import db, ClientMachines, Command
from ..sockets.data_transfer import sendSocketData, receiveSocketData
from ..database.database_tables import db, ClientMachines, AppMetrics, AppDetails

#Setup the blueprint for the command routes
command_routes = Blueprint('command_routes',__name__)

#Route: main route for the commands
#   - The route is /commands, supporting the GET, POST, PUT & DELETE methods
#   - It will return the main route for commands
@command_routes.route("/", methods=['GET','POST','PUT','DELETE'])
def command():
  return "The command routes are: /availableMachines - to get connected machines, /send - to send a command, /sendfile - to send a file"

#Route: to get a list of all machines tied to the application
#   - The route is /commands/availableMachines, supporting the GET method
#   - It will return the machine for running commands
@command_routes.route("/availableMachines", methods=['GET'])
def getAvailableMachines():
    #Get a list of everything in the machines database
    machineList = ClientMachines.query.all()
    finalList = []

    #Append data to the list for return
    for mach in machineList:
      finalList.append({
      "id": mach.id,
      "name": mach.name,
      "host_name": mach.host_name,
      "mac_address": mach.mac_address,
      "machine_id": mach.id,
    })

    return jsonify({
      "description": "A list of all of the available machines",
      "content": finalList
    })


#Route: to get list of apps for a specified machine
#   - The route is /commands/machineapps/<mac>, supporting the GET method
#   - It will return all the apps collected for a machine identified via the mac variable
@command_routes.route('/machineapps/<mac>', methods=['GET'])
def getAvailableApps(mac):
  final_apps_avail = []

  machAppsList = AppDetails.query.filter_by(machine_id=mac).all()

  for app in machAppsList:
    final_apps_avail.append({
    "id": app.id,
    "app_name": app.name,
    "pid": app.pid,
    "machine_id": app.machine_id
    })
  return jsonify({
    "description": "A list of available applications for a machine",
    "content": final_apps_avail
  })

#Route: to get the past 20~ commands
#   - The route is /commands/pastcommands, supporting the GET method
#   - It will return a histroy of the latest 25 commands
@command_routes.route("/pastcommands", methods=['GET'])
def getPastCommands():
    #Get a list of everything in the machines database
    commandList = Command.query.order_by(Command.id.desc()).limit(25).all()
    finalList = []

    for cmd in commandList:
      finalList.append({
      "id": cmd.id,
      "machine_name": cmd.machine.name,
      "command_type": cmd.type,
      "command_input": cmd.command_input,
      "output": cmd.output,
      "timestamp": datetime.fromtimestamp(cmd.timestamp).strftime('%Y-%m-%d %H:%M'),
    })

    return jsonify({
      "description": "A list of the past 25 commands sent",
      "content": finalList
    })

#Route: to send a command to the agent and get a response back
#   - The route is /commands/send, supporting the POST method
#   - It will attempt to send a command to the machine
@command_routes.route("/send", methods=['POST'])
def sendCommand():
  #Gets the body request - JSON structure for commands
  req = request.json
  sock = socket.socket()

  #Getting machine_id for the first machine in the table Client_machines
  agent_machine = ClientMachines.query.filter_by(id=req["machine_id"]).first() 
  ip = str(ipaddress.IPv4Address(agent_machine.ip_address))
  port = int(agent_machine.ports.split(",")[0])
  
  print("IP and port coupling: " + ip + " - " + str(port))

  sock.connect((ip, port)) #Connecting to socket

  try:
    #Create a new table entry object using request data
    command_data = Command(
      machine = agent_machine,
      timestamp = time.time(),
      type = req["type"],
      output = 'waiting...')

    if req["type"] == 'custom_command':
      command_data.command_input = req["parameters"]["custom_command"]
    db.session.add(command_data) #Stores the data in the database
    db.session.commit()

    print("Command Data saved to database")
  except Exception as err_msg:
    print(err_msg)

  json_var = {}

  #Storing the data in a json object from the body request.
  machine_id = req["machine_id"] 
  machine_name = req["machine_name"] 
  type = req["type"]
  json_var["machine_id"] = machine_id
  json_var["machine_name"] = machine_name
  json_var["type"] = type
  params_send = req["parameters"]

  json_var["parameters"] = params_send
    
  json_data = json.dumps(json_var)  #Creating a json object
  sendSocketData(sock, json_data) #Sending JSON Object to agent via sockets

  data = receiveSocketData(sock) #Receving the response from agent

  if data: # Runs if a response was returned from the agent
      command_data.result = True 
      command_data.output = data.decode()
      db.session.commit() #Updates the database
  else:
    print("No data received")
  

  return jsonify({"desc": "Return of the message from the socket", "content": str(data.decode())}) #Returns the output from the agent in a JSON format
from flask import Flask, render_template, request, url_for, redirect
import os
import logging
import sys

app = Flask(__name__)
log = logging.getLogger('werkzeug') 
log.setLevel(logging.ERROR)

@app.route("/", methods=["POST", "GET"])
def home():
    data = jsons.load("jsons_data/data.json")
    if "name" not in data["cache"]:
            if request.method == "POST":
             data["cache"]["name"] = request.form.get("name")
             data["cache"]["birthday"] = request.form.get("birthday")
             data["cache"]["qm"] = False
             data["cache"]["nm"] = False
             data["cache"]["logs"] = False
             jsons.dump("jsons_data/data.json", data)

            else:
             return render_template("register.html")
 
    active_plugin = request.args.get("active_plugin")
    active_plugin_name = active_plugin
    active_plugin = (data["plugins"][active_plugin] if active_plugin else None)
    active_command = request.args.get("active_command")
    active_command_name = active_command
    active_command = (data["commands"][active_command_name] if active_command_name else None)
    return render_template("index.html", data = data["cache"], plugins = data["plugins"], commands = data["commands"], active_plugin = active_plugin,active_plugin_name = active_plugin_name, active_command = active_command, active_command_name = active_command_name, sounds=os.listdir("Sounds"))

@app.route("/plugin", methods=["POST"])
def plugins():
    plugins = jsons.load("jsons_data/data.json")
    if request.form.get("action") == "plugin_save":
     if request.form.get("plugin") != "Не выбрано" and not request.form.get("plugin_name"):
         active_plugin = request.form.get("plugin")
         return redirect(url_for("home", active_plugin = active_plugin))
       
     else:
        if request.form.get("plugin_name"):
         plugins["plugins"][request.form.get("plugin_name")] = {"data" : request.form.get("plugin_args"), "do" : request.form.get("plugin_do").strip()}
         jsons.dump("jsons_data/data.json", plugins)
    
    else:
        del plugins["plugins"][request.form.get("plugin")]
        jsons.dump("jsons_data/data.json", plugins)
    
    return redirect(url_for("home"))

@app.route("/command", methods=["POST"])
def commands():
    commands = jsons.load("jsons_data/data.json")
    if request.form.get("action") == "command_save":
     if request.form.get("command") != "Не выбрано" and not request.form.get("command_name"):
         active_command = request.form.get("command")
         return redirect(url_for("home", active_command = active_command))
     
     else:
       if request.form.get("command_name") not in commands and request.form.get("command_name") or request.form.get("command") != "Не выбрано" and request.form.get("command_name"):
           commands["commands"][request.form.get("command_name")] = {
               "name" : request.form.get("command_name"), 
               "act_phrase" : data_of_list_strip(request.form.get("command_act").split(","), output=list),
               "plugin" : request.form.getlist("plugin_for_command"), 
               "jarvis_answer" : request.form.get("answer_for_command")
               }
           jsons.dump("jsons_data/data.json", commands)
       
    else:
        if request.form.get("command"):
         del commands["commands"][request.form.get("command")]
         jsons.dump("jsons_data/data.json", commands)
        
    return redirect(url_for("home"))

@app.route("/config", methods=["POST"])
def config():
   data = jsons.load("jsons_data/data.json")
   data["cache"]["qm"] = True if request.form.get("qm") else False
   data["cache"]["nm"] =  True if request.form.get("nm") else False
   data["cache"]["logs"] =  True if request.form.get("logs") else False
   jsons.dump("jsons_data/data.json", data)
   return redirect(url_for("home"))


def data_of_list_strip(data:list, output):
    clear_data = []
    for d in data:
        if d != '':
         clear_data.append(d.strip())
     
    if clear_data != []:
     return clear_data if output == list else {clear_data[0] : clear_data[1]}
    
    return [] if output == list else {}

def run_server():
    print("Settings on http://127.0.0.1:256")
    app.run(port=256)

if __name__ == "__main__":
    import jsons
    run_server()

else:
    import Panel.jsons as jsons
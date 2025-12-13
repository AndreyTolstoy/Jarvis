
         #?==Jarvis==
         #?==by AT==


from panel.jsons import load, dump
from ATS_v5.main import bridge
from panel import server
from outside_panel_get import outside_get

import speech_recognition
import pyglet
import random
import threading

#Для функции hb - happy birthday
import webbrowser
import datetime

config=None


def hb():
    data = load("cache.json")
    if data == {}:
        data["hp_status"] = False
        dump("cache.json", data)
    
    if load("panel/data.json") != {}:
     if datetime.datetime.strptime(load("panel/data.json")["birthday"], "%Y-%m-%d").strftime("%m-%d") == datetime.datetime.now().strftime("%m-%d") and load("cache.json")["hp_status"] != True:
        webbrowser.open("https://youtu.be/Dm2nj8GBASY?si=SBfgscwgE-57bvGG")
        Commands().answer(name="Поздравляю сэр.wav")
        data["hp_status"] = True
        dump("cache.json", data)

def listen():
        with speech_recognition.Microphone() as mic:
            try:
                sr = speech_recognition.Recognizer()
                sr.pause_threshold = 1
                sr.adjust_for_ambient_noise(source=mic, duration=1)
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                print(f"Вы сказали: {query}")
                return query
            except Exception as e:
                return ""
            
class Commands:
    def __init__(self, name=None, act_phrase=[], plugin=[], plugin_args={}, priority=None):
        self.name = name
        self.act_phrase = act_phrase
        self.plugin = plugin
        self.plugin_args = plugin_args
        self.priority = priority
    
    def plugin_run(self):
        if config and config["ats"] != False or not config:
         if self.plugin != []:
            for plugin_name in self.plugin:
                 plugin_code = load("plugins.json")[plugin_name]["data"]
                 if plugin_code:
                  try:
                   bridge(plugin_code, self.plugin_args)
                   print(f"ATS v5.0 {plugin_name} ✅")
                  
                  except Exception:
                      print(f"ATS v5.0 {plugin_name} Syntax Error ❌")

    def answer(self, name=None): 
        answers = (random.choice(["Всегда к вашим услугам сэр.wav", "Да сэр.wav", "Да сэр(второй).wav", "Есть.wav", "К вашим услугам сэр.wav", "Запрос выполнен сэр.wav"]) if not name else name)
        answer = pyglet.resource.media("Sounds/" + answers)
        answer.play()
        pyglet.app.exit()
                         

    
class CommandDetector(Commands):
  def __init__(self, name=None, act_phrase=None, open=None, plugin=None, priority=None):
      super().__init__(name, act_phrase, open, plugin, priority)

  def main(self):
   global config
   hb()
   while True:
    config = load("panel/data.json")
    commands = load("commands.json")
    plugins = load("plugins.json")

    if config and config["outside"] != False:
     h3 = threading.Thread(target=outside_get, daemon=True).start()
     
    if not commands:
        commands["commands"] = {}
        
    if "панель" not in commands["commands"]:
        commands["commands"]["панель"] = {"name" : "панель", "act_phrase" : ["открой панель управления", "панель управления"], "plugin" : ["панель"], "plugin_param" : {}, "priority" : 5}
        plugins["панель"] = {"data" : "webb.open'http://127.0.0.1:5000'", "do" : "open"}
        dump("commands.json", commands)
        dump("plugins.json", plugins)

    text = listen()
    if text: 
        commands_find = []
        for command in commands["commands"]:
                command = commands["commands"][command]
                command = Commands(command["name"], command["act_phrase"], command["plugin"], command["plugin_param"], int(command["priority"]))
                if any(f"джарвис" and phrase in text for phrase in command.act_phrase): #any(phrase in text for phrase in command.act_phrase) or
                    command.plugin_args["sr_text"] = text #New. Добавляем в список параметров системный параметр для того, чтобы пользователь мог использовать распознанный текст в своих плагинах
                    command.plugin_args["command_name"] = command.name #New. Добавляем в список параметров системный параметр для того, чтобы пользователь мог использовать имя распознанной команды в своих плагинах
                    commands_find.append(command)
        
        for command in sorted(commands_find, key=lambda p: p.priority, reverse=True):
            command.answer()
            command.plugin_run()
        
        

h1 = threading.Thread(target=server.run_server, daemon=True).start()
run = CommandDetector()
run.main()

         #?==Jarvis==
         #?==by AT==


from Panel.jsons import load, dump
from Jarvis.plugin_run import plugin_run

import speech_recognition
import winsound
import random
import os

#Для hb & gm
import webbrowser
import datetime

text = ""
def hb():
    data = load("jsons_data\\data.json")

    if "birthday" in data["cache"] and datetime.datetime.strptime(data["cache"]["birthday"], "%Y-%m-%d").strftime("%m-%d") == datetime.datetime.now().strftime("%m-%d") and data["cache"]["last_hp"] != datetime.datetime.now().strftime("%Y"):
       webbrowser.open("https://youtu.be/Dm2nj8GBASY?si=tXQ_RDV4naWigUct&t=0")
       Commands(jarvis_answer="Поздравляю сэр.wav").answer()
       data["cache"]["last_hp"] = datetime.datetime.now().strftime("%Y") #*записываем что в этом году уже поздравили
       dump("jsons_data\\data.json", data)

def gm():
    if int(datetime.datetime.now().strftime("%H")) < 11:
        Commands(jarvis_answer="Доброе утро.wav").answer() #*Good morning New-Yorkers

def listen():
        global text
        while True:
         with speech_recognition.Microphone() as mic:
             try:
                 sr = speech_recognition.Recognizer()
                 sr.pause_threshold = 0.5
                 sr.adjust_for_ambient_noise(source=mic)
                 audio = sr.listen(source=mic, timeout=5)
                 query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                 print(f"Вы сказали: {query}")
                 text = query
                 
             except Exception:
                 pass
            
class Commands:
    def __init__(self, name=None, act_phrase=[], plugin=[], jarvis_answer=None):
        self.name = name
        self.act_phrase = act_phrase
        self.plugin = plugin
        self.jarvis_answer = jarvis_answer

    def answer(self):
        if self.jarvis_answer == "random":
         answer = random.choice(["Всегда к вашим услугам сэр.wav", "Да сэр.wav", "Да сэр(второй).wav", "Есть.wav", "К вашим услугам сэр.wav", "Запрос выполнен сэр.wav"])
        
        else:
            answer = self.jarvis_answer

        winsound.PlaySound(os.path.dirname(__file__)[:-6] + "\\" + f"Sounds\\{answer}", winsound.SND_FILENAME | winsound.SND_ASYNC)

    def command_detector_algorithm(self, text, nm):
            if nm == True and "джарвис" in text or nm == False:
                if any(phrase in text for phrase in self.act_phrase) or any(phrase[:-1] in text for phrase in self.act_phrase):
                  return True
                
                for phrases in self.act_phrase:
                        accuracy = 0
                        for phrase in phrases.split(" "):
                         if phrase in text:
                            accuracy += 1

                         elif phrase[:-2] in text:
                             accuracy +=1

                if accuracy == 2:
                    return True

                else:
                     self.Jarvis_logs(f"Команда {self.name} не распознана ❌")

        #*Алгоритм максимально простой, но изначально кажется, что из-за него у джарвиса появится более большая задержка перед выполненим команды, но на самом деле, разницы я не заметил ВООБЩЕ

    def Jarvis_logs(self, log):
        data = load("jsons_data/data.json")["cache"]
        if "logs" in data and data["logs"] == True:
            print(log)

   
class Main(Commands):
  def __init__(self, name=None, act_phrase=None, plugin=None):
      super().__init__(name, act_phrase, plugin)
      
  def main(self):
   global text
   hb() #?happy birthday
   gm() #?good morning XD
       
   data = load("jsons_data\\data.json")
   if "панель" not in data["commands"]:
        data["commands"]["панель"] = {"name" : "панель", "act_phrase" : ["панель управления"], "plugin" : ["панель"], "jarvis_answer" : "random"}
        data["plugins"]["панель"] = {"data" : "http://127.0.0.1:256", "do" : "open"}
        dump("jsons_data\\data.json", data)
        data = load("jsons_data\\data.json")

   while True:
    data = load("jsons_data\\data.json")
    self.Jarvis_logs(f"Чтение данных завершено ✅")
        
    if text: 
        answer_status = False #*Флаг для случаев, когда в одном запросе несколько команд, чтобы не отвечать "Да сэр" на каждую
        commands_find = []
        for command in data["commands"]:
                command = data["commands"][command]
                command = Commands(command["name"], command["act_phrase"], command["plugin"], command["jarvis_answer"])

                if command.command_detector_algorithm(text, data["cache"]["nm"]): #New. Вызов алгоритма, чтобы не писать длинные выражения в условии
                    self.Jarvis_logs(f"Команда {command.name} распознана ✅")
                    commands_find.append(command)
                    for phrase in command.act_phrase:
                        if text.count(phrase) > 1:
                            for _ in range(text.count(phrase) - 1): #-1 так как один раз мы ее уже записали сверху
                             commands_find.append(command)
         
        for command in commands_find:
            if not answer_status and data["cache"]["qm"] == False:
             command.answer()

            plugin_run(command.plugin)
            answer_status = True
        
        text = ""
        
        

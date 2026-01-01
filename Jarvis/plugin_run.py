from Panel.jsons import load
import os
import webbrowser
import keyboard
    

def plugin_run(plugins : list):
         if plugins != []:
            for plugin_name in plugins:
                 data = load("jsons_data/data.json")
                 plugin_args = data["plugins"][plugin_name]["data"]
                 plugin_do = data["plugins"][plugin_name]["do"]
                 if plugin_args:
                   try:
                    if plugin_do == "open":
                         if plugin_args.startswith("http"):
                               webbrowser.open(plugin_args)
                            
                         else:
                              os.startfile(plugin_args)
                    else:
                         keyboard.press_and_release(plugin_args)
                              
                   except Exception as e:
                        print("Error in run plugin: ", e, "❌")

                   if data["cache"]["logs"] == True:
                    print(f"Run {plugin_name} plguin✅")
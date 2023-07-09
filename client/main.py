from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
import threading
import client
ADDR = client.ADDR
print(ADDR)

class MainApp(App):
    connected_or_not = "Connecting"

    def build(self):

        self.ScreenM = ScreenManager()
        self.S1 = Screen()
        self.B = Button(text='The button is ' + str(self.connected_or_not))
        self.B.bind(on_touch_down=self.Hop)
        self.S1.add_widget(self.B)
        self.ScreenM.add_widget(self.S1)
        thread = threading.Thread(target=self.connect)
        thread.start()
        return self.ScreenM

    def connect(self):
        self.Connect_loop()
        
        self.Return_Message = client.send("Hello I'm Button")
        if self.Return_Message == "Message received!":
            self.connected_or_not= 'Connected'
            self.B.text = 'The button is ' + str(self.connected_or_not)

    def Connect_loop(self):
        try:
            client.Client.connect(client.ADDR)
            print('Connected')
        except:
            self.Connect_loop()

    def Hop(self, objs, args):
        client.send("Hop!")



if __name__ == "__main__":
   
    MainApp().run()
    



    #client.send(client.DISCONNECT_MSG)

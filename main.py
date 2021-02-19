from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.core.window import Window
from kivy.clock import Clock
#import time

from random import randint
from random import random as rand

from kivy.base import EventLoop

from kivy.core.audio import SoundLoader


import sqlite3

###database
conn = sqlite3.connect('highScore.db') 							#create if not exists and connect to the database named 'highScore.db'
c = conn.cursor()                      							#create a cursor object to add/manipulate the data in it, below operations
																					#are all done by cursor

c.execute('''Create TABLE if not exists highscore('high')''')	#create a table if not exists named 'highscore' with only one column 'high'
#c.execute("INSERT INTO highscore(high) VALUES(?)", [0]) #uncomment only when initially creating the database(running the script for first time		#initially adding value while creating db
c.execute("SELECT * FROM highscore")							#select all the the rows of the table named 'highscore'

rows_list = c.fetchall()										#Return the rows as list with each row is a list of cells in it											

highscore = int(rows_list[0][0])
conn.commit()
conn.close()

def score_update(new_score):
	global highscore
	conn = sqlite3.connect('highScore.db')
	c = conn.cursor()
	c.execute("SELECT * FROM highscore")
	rows = c.fetchall()												
	highscore = rows[0][0]
	if new_score > highscore:
		c.execute("DELETE FROM highscore")
		c.execute("INSERT INTO highscore(high) VALUES(?)", [new_score])
		highscore = new_score
	conn.commit()
	conn.close()
###database


#Important Note Always first set the device screen size 
#Window.size = (320, 550)
x_0, y_0 = Window.size

lime_green = (124/256, 252/256, 0/ 256, 1)

class MainApp(App):

	
	def build(self):
		
		self.sound1 = SoundLoader.load('oldschool_drums.wav')
		self.sound1.loop = True
		self.sound1.play()

		self.game_over_sound = SoundLoader.load('game_over.wav')
		self.game_over_sound.bind(on_stop=self.new_game)



		


		self.ScreenM = ScreenManager()
		self.s0 = Screen_begin(name='begin')
		self.ScreenM.add_widget(self.s0)

		self.ScreenM.bind(on_touch_down=self.update_0)

		self.name_ = '1'
		self.collision_first = False
		return self.ScreenM


	def update_0(self, par1, par2):
		if self.ScreenM.current_screen != self.ScreenM.screens[0]:
			return
                        
		self.s1 = Screen(name='first')
		self.game = FlappyGame()
		self.s1.add_widget(self.game)
		#Clock.schedule_interval(self.game.update, 1/60)
		Clock.schedule_interval(self.update, 1/60)
		self.ScreenM.add_widget(self.s1)
		
		
		self.ScreenM.current = self.ScreenM.screens[-1].name
		#del self.ScreenM.screens[-2]


	def update(self, dt):
		if self.collision_first == True:
			self.game_over()
			return

		
		
		if self.game.greenPipes.collided == True:
			self.game.bird.v_0 = 19
			self.game.bird.g = -20

			self.collision_first = True
			self.game.bird.collision_check = True
			score_update(self.game.bird.score)

			self.game_over()




	def game_over(self):
		self.sound1.stop()
		self.game_over_sound.play()
		#Clock.schedule_once(self.new_game, 3)
		
		
		if self.game.bird.Bird_.pos[1] > -10:
			self.game.bird.key_time = 0
			
		#else:
		#	self.new_game()
		

	def new_game(self, widget):

		self.name_ = str(int(self.name_)+1)
		self.game = FlappyGame()
		self.s2 = Screen(name=str('name')+self.name_)
		self.s2.add_widget(self.game)
		del self.ScreenM.screens[-1]
		self.ScreenM.add_widget(self.s2)
		self.ScreenM.current = self.ScreenM.screens[-1].name
		self.sound1.play()
		#game_over_sound.stop()
		self.collision_first = False
			


	

class Screen_begin(Screen):
	def __init__(self, **kwargs):
		super(Screen_begin, self).__init__(**kwargs)


		self.image = Image(source='./game_begin.png', keep_ratio=False, allow_stretch=True, pos=(0,0),size_hint=(None,None), size=(x_0,y_0))

		self.add_widget(self.image)

		self.label = Label(text="Tap to Begin", pos=(x_0*0.5-((x_0//1.5)*0.5),y_0*0.5-((y_0//4)*0.5)), size_hint=(None, None), size=(x_0//1.5, y_0//4))
		self.add_widget(self.label)
		self.play = False
		

	def Play(self, *largs):
		self.play = True

		

class GreenPipes(Widget):

	def __init__(self,bird, **kwargs):
		super(GreenPipes,self).__init__(*kwargs)
		self.bird = bird
		self.collided = False

 		#self.collided = False

		self.x = x_0
		self.y = 0

		self.size_x = x_0/7
		self.size_y_max = y_0/2.25

		self.pipes = []
		
		for i in range(6):
					#Color(0.195, 0.800, 00.195, 1)
			size_y_below = int(self.size_y_max*randint(65, 85)*0.01)
			####IMPORTANT nOTE ON IMAGES: KEEP RATIO FALSE AND STRECH TRUE THEN ONLY WHOLE SCREEN GETS OCCUPIED
			self.Pipe = Image(source="./down_pipe.png", keep_ratio=False,allow_stretch=True,pos=(self.x + (x_0*0.5*i), self.y),size_hint=(None, None), size=(self.size_x, size_y_below))
			self.Pipe_ = Image(source="./up_pipe.png", keep_ratio=False,allow_stretch=True,pos=(self.x + (x_0*0.5*i), y_0-(y_0 - (2*size_y_below))), size_hint=(None, None) ,size = (self.size_x, y_0 - (2*size_y_below)))
			self.add_widget(self.Pipe)
			self.add_widget(self.Pipe_)
			self.pipes.append((self.Pipe, self.Pipe_)) 

		Clock.schedule_interval(self.update, 1/60)



	def update(self, dt):

		if self.collided == True:
			return

		for i in self.pipes:
			if True == i[0].collide_widget(self.bird.Bird_) or True == i[1].collide_widget(self.bird.Bird_) or self.bird.Bird_.pos[1] < 0:#self.bird.Bird_.pos[0], self.bird.Bird_.pos[1]):

				self.collided = True
				

		

		for i in self.pipes:
			power = (self.bird.score//22) 
			

			x, y = i[0].pos
			x_, y_ = i[1].pos
			
			if x < -1*self.size_x:
				x = x_0 + (1.8*x_0)
				x_ = x_0 + (1.8*x_0)

			if x_0 < 320:
				neg = 1
			else:
				neg = int(x_0/320)* (1.2)**power

			#self.x = x - 1
			i[0].pos = (x-neg, y)
			i[1].pos = (x_-neg, y_)



class Bird(Widget):
	def __init__(self, **kwargs):
		super(Bird, self).__init__(**kwargs)
		#self.pipes = pipes
		#print(self.pipes)

		self.x = x_0/4
		self.y = y_0/2

		self.x_size = int(x_0/6.4)
		self.y_size = int(y_0/18.3)

		self.v_0 = 0
		self.g = -1*int((y_0/56.12))
		self.t = 0


		self.key_time = 0
		self.key_press = 0

		self.score =  00
		self.collision_check = False

		

		
		self.Bird_ = Image(source="./bird_down.png",keep_ratio=False,allow_stretch=True,pos=(self.x, self.y-(self.y_size/2)), size_hint= (None, None), size=(x_0//10, y_0//20))
		self.add_widget(self.Bird_)


		Clock.schedule_interval(self.update, 1/60)
		EventLoop.window.bind(on_touch_down=self.keyboard)



	
	def keyboard(self, *largs):


		if self.key_time <= 1 and self.key_press >= 3:
			return
		self.key_time = 0
		self.key_press += 1
		

		
			#print(key)
		self.v_0 = int((y_0/100))
		self.t = 0

	


	def update(self, dt):
		#print(self.pipes)
		#print(self.collide_widget(self.pipes))
	

		self.key_time += dt


		#y = y_0 + v_y(t) + a*t^2
		#v = v_0 + a*t
		if self.collision_check == False:
			self.score += (dt)

		

		self.t = self.t + dt
		
		self.v = self.v_0 + (self.g * self.t)
		
		if self.v >= 0:
			self.Bird_.source = "./bird_up.png"
		else:
			self.Bird_.source = "./bird_down.png"


		self.Bird_.pos =(self.Bird_.pos[0], self.Bird_.pos[1] + (self.v_0*self.t) + (0.5*(self.g *(self.t**2))) )


class FlappyGame(Widget):
	def __init__(self, **kwargs):
		super(FlappyGame, self).__init__(*kwargs)
		self.bird = Bird()
		self.greenPipes = GreenPipes(self.bird)
		self.add_widget(Image(source='./backdrop.png', keep_ratio= False, allow_stretch=True, size_hint=(None,None), size=(x_0, y_0)))
		self.add_widget(self.greenPipes)
		self.add_widget(self.bird)
		self.score = 00
		self.Score = Label(text='    Score: '+str(self.score), size= (x_0//1.6, y_0//5.2) , pos= (x_0-(x_0//1.7), y_0-(y_0//5.4)), font_size = y_0//20)
		self.add_widget(self.Score)
		self.HScore = Label(text='HighScore: '+str(int(highscore)), size= (x_0//1.6, y_0//5.2) , pos= (x_0-(x_0//1.7), y_0-(y_0//5.4)-(y_0//17)), font_size = y_0//20)
		self.add_widget(self.HScore)

		Clock.schedule_interval(self.score_update, 1/60)

	def score_update(self, dt):
		self.Score.text = '    Score: '+str(int(self.bird.score))
		


if __name__ == '__main__':

		
	MainApp().run()

# Keep Track of Violations
# You need a method that keeps scanning your buffers and checks if three immediate violations are recorded
# In python, you'll almost never need to use a singleton class, just define a module with global variables - they will be the singleton's attributes
# Then add some functions - you can define function within function in python - these will be the singleton's methods

# import tkinter

#Use functools' partial to pass argument(reference to the button) to change the color of that particular button only
#Or use lambda function within command to change color of the button as seen here: https://stackoverflow.com/questions/27198287/tkinter-create-multiple-buttons-with-different-command-function#comment87964033_27198298
#Other modules don't need to interact with the proctor status window at all, they just set its global variables that's all




# proctorstatus = tkinter.Tk()
# option = ['Eye: Left', 'Eye: Right', 'Eye: Up', 'Head: Down', 'Head: Up', 'Head: Right', 'Head: Left']
# buttons = []
# for i in range(len(option)):
# 	b = tkinter.Button(proctorstatus, height = 2, width = 10, text = option[i], bg = 'green', command = lambda i=i: buttons[i].config(bg='red'))
# 	b.grid(row=i//4,column=i%4)
# 	# b.pack()
# 	buttons.append(b)
# while True:
# 	proctorstatus.update()

# proctorstatus.mainloop()



# import tkinter as tk

# root = tk.Tk()
# button = tk.Button(root, text="This is a button")
# button.pack()

# while True:
#     root.update()



# x = 500	
# def trial():
	# global proctorstatus
# def setz(y):
# 	global x
# 	x = y
# def check():
# 	global x
# 	return x

	
# proctorstatus.mainloop()


# eyes = [[],[],[]]
# head = [[],[],[],[]]


# def violationTracker():
# 	global eyes
# 	global head
# 	global proctorstatus
# 	def track_eyes():
# 		if len(eyes[0])>3:
# 			print("EYES: LOOKING LEFT")
# 			eyes[0]=[]
# 		if len(eyes[1])>3:
# 			print("EYES: LOOKING RIGHT")
# 			eyes[1]=[]
# 		if len(eyes[2])>3:
# 			print("EYES: LOOKING UP")
# 			eyes[2]=[]
# 	def track_head():
# 		if len(head[0])>3:
# 			print("HEAD: LOOKING DOWN")
# 			head[0]=[]
# 		if len(head[1])>3:
# 			print("HEAD: LOOKING UP")
# 			head[1]=[]
# 		if len(head[2])>3:
# 			print("HEAD: LOOKING RIGHT")
# 			head[2]=[]
# 		if len(eyes[2])>3:
# 			print("HEAD: LOOKING LEFT")
# 			head[3]=[]
# 	def track():
# 		track_eyes()
# 		track_head()




import tkinter
import threading
import time

buttons = []
proctorstatus = ''
eyes = [[],[],[]]
head = [[],[],[],[]]
person = 1
phone = 0
# tab = 0
audio = 0

def create():
    global proctorstatus
    proctorstatus = tkinter.Tk()
    global buttons
    option = ['Eye: Left', 'Eye: Right', 'Eye: Up', 'Head: Down', 'Head: Up', 'Head: Right', 'Head: Left', '>1 Person', 'No Person', 'Phone', 'Tab Shift', 'Audio']
    buttons = []
    for i in range(len(option)):
        b = tkinter.Button(proctorstatus, height = 2, width = 10, text = option[i], bg = 'green', command = lambda i=i: buttons[i].config(bg='green'))
        b.grid(row=i//4,column=i%4)
        buttons.append(b)
    t2 = threading.Thread(target=violationTracker)
    t2.start()
    # t2.join()
    proctorstatus.mainloop()
    proctorstatus.quit()


def violationTracker():
	global eyes
	global head
	global proctorstatus
	global buttons
	global person, phone, tab, audio
	def track_eyes():
		for i in range(3):
			if len(eyes[i])>3:
				buttons[i].config(bg='red')
				eyes[i]=[]
		# if len(eyes[0])>3:
		# 	# print("EYES: LOOKING LEFT")
		# 	buttons[0].config(bg='red')
		# 	eyes[0]=[]
		# if len(eyes[1])>3:
		# 	# print("EYES: LOOKING RIGHT")
		# 	buttons[1].config(bg='red')
		# 	eyes[1]=[]
		# if len(eyes[2])>3:
		# 	# print("EYES: LOOKING UP")
		# 	buttons[2].config(bg='red')
		# 	eyes[2]=[]
	def track_head():
		for i in range(4):
			if len(head[i])>3:
				buttons[3+i].config(bg='red')
				head[i]=[]
		# if len(head[0])>3:
		# 	# print("HEAD: LOOKING DOWN")
		# 	buttons[3].config(bg='red')
		# 	head[0]=[]
		# if len(head[1])>3:
		# 	# print("HEAD: LOOKING UP")
		# 	buttons[4].config(bg='red')
		# 	head[1]=[]
		# if len(head[2])>3:
		# 	# print("HEAD: LOOKING RIGHT")
		# 	buttons[5].config(bg='red')
		# 	head[2]=[]
		# if len(eyes[2])>3:
		# 	# print("HEAD: LOOKING LEFT")
		# 	buttons[6].config(bg='red')
		# 	head[3]=[]
	while True:
		with open("tracktab.txt","r") as tracktab:
			tab = int(tracktab.read(1))
		# print("The value of tab is: ",tab)
		track_eyes()
		track_head()

		if person==0:
			buttons[8].config(bg='red')
			
		elif person>1:
			buttons[7].config(bg='red')
		person = 1

		if phone:
			buttons[9].config(bg='red')
			phone = 0

		if tab:
			# print("Activating tab")
			buttons[10].config(bg='red')
			with open("tracktab.txt",'w') as tracktab:
				tracktab.write('0')


		if audio:
			buttons[11].config(bg='red')
			audio = 0





def appendToViolation(which,pos):
	if which==0:
		global eyes
		eyes[pos].append(time.time())
	elif which==1:
		global head
		head[pos].append(time.time())
	elif which==2:
		global person
		person = pos
	elif which==3:
		global phone
		phone = 1
	elif which==4:
		with open("tracktab.txt",'w') as tracktab:
			tracktab.write('1')
	elif which==5:
		global audio
		audio = 1

		
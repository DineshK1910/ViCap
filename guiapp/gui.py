#createbutton(imgobj,btntext,(starcoord/center(of btn,text)),(endcoord/radius()of btn/text)),shape,(colourbtn,colourtxt),line,font,fontscale,(btnthickness,textthickness))

#Have to create photo-editing menu(shapes,colours,trackbar)
#have to join all options with their respective functions=>started
#Have to ensure proper and sequential working of windows=>Half done
#Try to write functions to lower the burden of creating buttons(find an easy generalization for button creation)
#can add more options to eah menu later,now ensure revision,not user-specific app
import cv2 as cv
import numpy as np
import pyautogui

#all use global variables
font=cv.FONT_HERSHEY_SIMPLEX
line=cv.LINE_AA

class main_menu:
	def __init__(self):
		self.menu=0
		self.create_menu()
		self.exit_flag=0
	def prog_start(self):			#main function
		self.disp_menu()
		while(True):
			if self.exit_flag==1:
				break
			else:
				cv.waitKey(1)
		cv.destroyAllWindows()
	def create_menu(self):
		self.menu=np.ones((512,512,3),np.uint8)
		self.menu*=255
		#WELCOME	
		cv.rectangle(self.menu,(100,20),(460,50),(0,100,255),-1)
		cv.putText(self.menu,'Welcome',(190,45),font,1,(0,255,255),4,line)
		#Open photo editor
		cv.rectangle(self.menu,(100,100),(460,130),(0,100,255),-1)
		cv.putText(self.menu,'1.Photo editor',(110,125),font,1,(0,255,255),4,line)
		#Open video editor
		cv.rectangle(self.menu,(100,140),(460,170),(0,100,255),-1)
		cv.putText(self.menu,'2.Video editor',(110,165),font,1,(0,255,255),4,line)
		#Exit
		cv.rectangle(self.menu,(100,180),(460,210),(0,100,255),-1)
		cv.putText(self.menu,'3.Exit',(110,205),font,1,(0,255,255),4,line)
		#load video
		#cv.rectangle(menu,(100,220),(460,250),(0,100,255),-1)
		#cv.putText(menu,'4.Load video',(110,245),font,1,(0,255,255),4,line)	
	def disp_menu(self):
		cv.imshow('Menu',self.menu)
		cv.setMouseCallback('Menu',self.mainmenu_callback)			

#callback functions to link gui with program
	def mainmenu_callback(self,event,x,y,flags,param):
		if(x<100 or x>460 or y<100 or y>210):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				if(y>=100 and y<=130):
					p=photo_editor()
					p.disp_menu()
				elif(y>=140 and y<=170):
					v=video_editor()
					v.disp_menu()
				elif(y>=180 and y<=210):
					self.exit_flag=1				
class photo_editor:
	def __init__(self):
		self.photo_board=0
		self.takepic_flag=0
		self.pmenu=0
		self.create_menu()
#menu creation functions
	def create_menu(self):
		global font,line
		self.pmenu=np.ones((512,512,3),np.uint8)
		self.pmenu*=255
		#photo-editing
		cv.rectangle(self.pmenu,(100,20),(460,50),(0,100,255),-1)
		cv.putText(self.pmenu,'Photo-Editor',(110,45),font,1,(0,255,255),4,line)
		#load a photo
		cv.rectangle(self.pmenu,(100,100),(460,130),(0,100,255),-1)
		cv.putText(self.pmenu,'1.Load photo',(110,125),font,1,(0,255,255),4,line)
		#Capture photo
		cv.rectangle(self.pmenu,(100,140),(460,170),(0,100,255),-1)
		cv.putText(self.pmenu,'2.Capture Photo',(110,165),font,1,(0,255,255),4,line)
		#Edit photo
		cv.rectangle(self.pmenu,(100,180),(460,210),(0,100,255),-1)
		cv.putText(self.pmenu,'3.Edit photo',(110,205),font,1,(0,255,255),4,line)
		#Save Photo
		cv.rectangle(self.pmenu,(100,220),(460,250),(0,100,255),-1)
		cv.putText(self.pmenu,'4.Save photo',(110,245),font,1,(0,255,255),4,line)
		#screenshot
		cv.rectangle(self.pmenu,(100,260),(460,290),(0,100,255),-1)
		cv.putText(self.pmenu,'5.Screenshot',(110,285),font,1,(0,255,255),4,line)
		#back
		cv.rectangle(self.pmenu,(100,300),(460,330),(0,100,255),-1)
		cv.putText(self.pmenu,'6.Back',(110,325),font,1,(0,255,255),4,line)
	
	def disp_menu(self):
		cv.destroyAllWindows()
		cv.imshow('Photo-Editor',self.pmenu)
		cv.setMouseCallback('Photo-Editor',self.peditor_callback)
#function for different options in menu
	def load_photo(self):
		filename=input("Enter the path(with filename and extension):").strip()
		self.photo_board=cv.imread(filename)
		cv.imshow('Photo-Board',self.photo_board)
	def capture_photo(self):
		global font,line
		cap=cv.VideoCapture(0)
		cv.namedWindow('Photo-Board')
		cv.setMouseCallback('Photo-Board',self.takepic_callback)
		while cap.isOpened():
			ret,self.photo_board=cap.read()
			if not ret:
				print('Frame not read(stream ended?)Exiting...')
				return
			pic=np.copy(self.photo_board)
			cv.rectangle(pic,(1,440),(640,480),(0,100,255),-1) #640x480 frames
			cv.putText(pic,'Capture',(250,465),font,1,(0,255,255),4,line)
			cv.imshow('Photo-Board',pic)
			cv.waitKey(1)	#To see the camera display,without it it's too fast for the window to even appear
			if self.takepic_flag==1:
				self.takepic_flag=0
				break
		cap.release()
		cv.imshow('Photo-Board',self.photo_board)
	def edit_photo(self):
		pass
	def save_photo(self):
		filename=input("Enter the filename:").strip()
		if('.' not in filename[-5:]):
			filename=filename+'.png'	
		cv.imwrite(filename,self.photo_board)
	def screenshot(self):
		img=pyautogui.screenshot()
		self.photo_board=np.array(img)
		self.photo_board=cv.cvtColor(self.photo_board,cv.COLOR_BGR2RGB)
		cv.namedWindow('Photo-Board',cv.WINDOW_NORMAL)
		cv.resizeWindow('Photo-Board',512,512)
		cv.imshow('Photo-Board',self.photo_board)	
#callback functions	
	def peditor_callback(self,event,x,y,flags,param):
		if(x<100 or y<100 or x>460 or y>330):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				if(y>=100 and y<=130):
					self.load_photo()
				if(y>=140 and y<=170):
					self.capture_photo()
				if(y>=180 and y<=210):
					self.edit_photo()
				if(y>=220 and y<=250):
					self.save_photo()
				if(y>=260 and y<=290):
					self.screenshot()
				elif(y>=300 and y<=330):
					cv.destroyAllWindows()
					m.disp_menu()

	def takepic_callback(self,event,x,y,flags,param):
		if event==cv.EVENT_LBUTTONUP:
			if(y>=440 and y<=480):
				self.takepic_flag=1
class video_editor:
	def __init__(self):
		self.vmenu=0
		self.create_menu()
#menu creation functions
	def create_menu(self):
		self.vmenu=np.ones((512,512,3),np.uint8)
		self.vmenu*=255
		#video-editing
		cv.rectangle(self.vmenu,(30,20),(460,50),(0,100,255),-1)
		cv.putText(self.vmenu,'Video-Editor',(35,45),font,1,(0,255,255),4,line)
		#Play video
		cv.rectangle(self.vmenu,(30,100),(460,130),(0,100,255),-1)
		cv.putText(self.vmenu,'1.Play A Video(muted)',(35,125),font,1,(0,255,255),4,line)
		#record video from cam
		cv.rectangle(self.vmenu,(30,140),(460,170),(0,100,255),-1)
		cv.putText(self.vmenu,'2.Record Camera(muted)',(35,165),font,1,(0,255,255),4,line)
		#record screen
		cv.rectangle(self.vmenu,(30,180),(460,210),(0,100,255),-1)
		cv.putText(self.vmenu,'3.Record Screen(muted)',(35,205),font,1,(0,255,255),4,line)
		#back
		cv.rectangle(self.vmenu,(30,220),(460,250),(0,100,255),-1)
		cv.putText(self.vmenu,'4.Back',(35,245),font,1,(0,255,255),4,line)
	def disp_menu(self):
		cv.destroyAllWindows()
		cv.imshow('Video-Editor',self.vmenu)
		cv.setMouseCallback('Video-Editor',self.veditor_callback)
#functions for different options in menu
#callback functions
	def veditor_callback(self,event,x,y,flags,param):
		if(x<30 or y<100 or x>460 or y>250):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				if(y>=100 and y<=130):
					pass
				if(y>=140 and y<=170):
					pass
				if(y>=180 and y<=210):
					pass
				elif(y>=220 and y<=250):
					cv.destroyAllWindows()
					m.disp_menu()
m=main_menu()
m.prog_start()

#createbutton(imgobj,btntext,(starcoord/center(of btn,text)),(endcoord/radius()of btn/text)),shape,(colourbtn,colourtxt),line,font,fontscale,(btnthickness,textthickness))
#--------------------------------------------------------------------------------->
#problems
#palette not working properly problem with starting(maybe too many threads are causing a problem)

import cv2 as cv
import numpy as np
import pyautogui
from math import *

#all use global variables
font=cv.FONT_HERSHEY_SIMPLEX
line=cv.LINE_AA
	
	###############################################################################################################
	#################			general purpose functions				##################
	###############################################################################################################

#general purpose functions to increase productivity
def generate_menu(img,options):
	for i in options:
			j,k=options[i]
			if(i!=('limits',None)):
				cv.rectangle(img,j[0],j[1],j[2],j[3])
				cv.putText(img,i[0],k[0],k[1],k[2],k[3],k[4],k[5])
def check_param(options,x,y,call=True):
	for i in options:
		if(i==('limits',None)):
			pass
		else:
			j,k=options[i]
			if(x>=j[0][0] and y>=j[0][1] and x<=j[1][0] and y<=j[1][1]):
				if(i[1]!=None):
					if(call):
						i[1]()
				return(i)
			
	return((None,None))
def limit_check(opt,x,y):
	if(x<opt[0][0] or x>opt[0][1] or y<opt[1][0] or y>opt[1][1]):
		return True
	else:
		return False
		
	###############################################################################################################
	############################			main classes			##################################
	###############################################################################################################

##############
#Main-Menu
#############
class main_menu:
	def __init__(self):
		self.options={
				('Welcome',None):([(100,20),(460,50),(0,100,255),-1],[(190,45),font,1,(0,255,255),4,line]),
				('1.Photo editor',self.open_photo_editor):([(100,100),(460,130),(0,100,255),-1],[(110,125),font,1,(0,255,255),4,line]),
				('2.Video editor',self.open_video_editor):([(100,140),(460,170),(0,100,255),-1],[(110,165),font,1,(0,255,255),4,line]),
				('3.Exit',self.back):([(100,180),(460,210),(0,100,255),-1],[(110,205),font,1,(0,255,255),4,line]),
				('limits',None):([100,460],[100,210])
				}
				#():([],[])
		self.menu=np.ones((512,512,3),np.uint8)
		self.menu*=255
		generate_menu(self.menu,self.options)
		self.exit_flag=0
#main function
##############	
	def prog_start(self):			
		self.disp_menu()
		while(True):
			if self.exit_flag==1:
				break
			else:
				cv.waitKey(1)
		cv.destroyAllWindows()
		
	def disp_menu(self):
		cv.imshow('Menu',self.menu)
		cv.setMouseCallback('Menu',self.mainmenu_callback)	
#functions for options
######################
	def open_photo_editor(self):
		p=photo_editor()
		p.disp_menu()
	def open_video_editor(self):
		v=video_editor()
		v.disp_menu()		
	def back(self):
		self.exit_flag=1				

#callback functions
###################
	def mainmenu_callback(self,event,x,y,flags,param):
		if(limit_check(self.options[('limits',None)],x,y)):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				check_param(self.options,x,y)									
################
#photo editor
################
class photo_editor:
	def __init__(self):
		global font,line
		self.photo_board=0
		self.takepic_flag=0
		self.options={
				('Photo-Editor',None):([(100,20),(460,50),(0,100,255),-1],[(110,45),font,1,(0,255,255),4,line]),
				('1.Load photo',self.load_photo):([(100,100),(460,130),(0,100,255),-1],[(110,125),font,1,(0,255,255),4,line]),
				('2.Capture photo',self.capture_photo):([(100,140),(460,170),(0,100,255),-1],[(110,165),font,1,(0,255,255),4,line]),
				('3.Screenshot',self.screenshot):([(100,180),(460,210),(0,100,255),-1],[(110,205),font,1,(0,255,255),4,line]),
				('4.New Photo',self.new_photo):([(100,220),(460,250),(0,100,255),-1],[(110,245),font,1,(0,255,255),4,line]),
				('5.Edit',self.open_edit_menu):([(100,260),(460,290),(0,100,255),-1],[(110,285),font,1,(0,255,255),4,line]),
				('6.Save',self.save_photo):([(100,300),(460,330),(0,100,255),-1],[(110,325),font,1,(0,255,255),4,line]),
				('7.Back',self.back):([(100,340),(460,370),(0,100,255),-1],[(110,365),font,1,(0,255,255),4,line]),
				('limits',None):([100,460],[100,370])
				}
		self.pmenu=np.ones((512,512,3),np.uint8)
		self.pmenu*=255
		generate_menu(self.pmenu,self.options)
		
	def disp_menu(self):
		cv.imshow('Menu',self.pmenu)
		cv.setMouseCallback('Menu',self.peditor_callback)
#functions for options
######################
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
	
	def screenshot(self):
		img=pyautogui.screenshot()
		self.photo_board=np.array(img)
		self.photo_board=cv.cvtColor(self.photo_board,cv.COLOR_BGR2RGB)
		cv.namedWindow('Photo-Board',cv.WINDOW_NORMAL)
		cv.resizeWindow('Photo-Board',512,512)
		cv.imshow('Photo-Board',self.photo_board)	

	def new_photo(self):
		self.photo_board=np.ones((512,512,3),np.uint8)
		self.photo_board*=255
		cv.imshow('Photo-Board',self.photo_board)
	def open_edit_menu(self):
		pe=photo_editing_options(self)
		pe.disp_menu()
	def save_photo(self):
		filename=input("Enter the filename:").strip()
		if('.' not in filename[-5:]):
			filename=filename+'.png'	
		cv.imwrite(filename,self.photo_board)	
	def back(self):
		cv.destroyAllWindows()
		m.disp_menu()
#callback functions
###################	
	def peditor_callback(self,event,x,y,flags,param):
		if(limit_check(self.options['limits',None],x,y)):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				check_param(self.options,x,y)
						
	def takepic_callback(self,event,x,y,flags,param):
		if event==cv.EVENT_LBUTTONUP:
			if(y>=440 and y<=480):
				self.takepic_flag=1
####################
#Photo-editing menu
####################
class photo_editing_options:
	def __init__(self,selfparent):
		global font,line
		self.pedit=0
		self.ix=0
		self.iy=0
		self.r=0
		self.g=0
		self.b=0
		self.rad=1
		self.pal=0
		self.pts=[]
		self.switch='1:ON\n0:OFF'
		self.selected_option=False
		self.drawing_flag=False
		self.enable_editing_flag=False
		self.enable_pal_flag=False
		self.parent=selfparent
		self.options={
			('Edit Menu',None):([(100,20),(300,50),(0,100,255),-1],[(110,45),font,1,(0,255,255),4,line]),
			('circle',self.draw_circle):([(100,100),(300,130),(0,100,225),-1],[(110,125),font,1,(0,255,255),4,line]),
			('rectangle',self.draw_rec):([(100,140),(300,170),(0,100,225),-1],[(110,165),font,1,(0,255,255),4,line]),
			('ellipse',self.draw_ellipse):([(100,180),(300,210),(0,100,225),-1],[(110,205),font,1,(0,255,255),4,line]),
			('line',self.draw_line):([(100,220),(300,250),(0,100,225),-1],[(110,245),font,1,(0,255,255),4,line]),
			('polygon',self.draw_polygon):([(100,260),(300,290),(0,100,225),-1],[(110,285),font,1,(0,255,255),4,line]),
			('polyline',self.draw_polyline):([(100,300),(300,330),(0,100,225),-1],[(110,325),font,1,(0,255,255),4,line]),
			('Eraser',self.draw_eraser):([(100,340),(300,370),(0,100,255),-1],[(110,365),font,1,(0,255,255),4,line]),
			('Palette',self.disp_palette):([(100,380),(300,410),(0,100,255),-1],[(110,405),font,1,(0,255,255),4,line]),
			('Back',self.back):([(100,420),(300,450),(0,100,255),-1],[(110,445),font,1,(0,255,255),4,line]),
			('limits',None):([100,300],[100,450])
			}
			#11:([],[]),
		self.pedit=np.ones((512,512,3),np.uint8)
		self.pedit*=255
		generate_menu(self.pedit,self.options)
		cv.setMouseCallback('Photo-Board',self.pboard_callback)
	def disp_menu(self):
		cv.imshow('Menu',self.pedit)
		cv.setMouseCallback('Menu',self.pedit_ops_callback)
		self.enable_editing_flag=True
#functions for options
######################
	def draw_circle(self,event,x,y):
		if event==cv.EVENT_LBUTTONDOWN:
			self.drawing_flag=True
			cv.circle(self.parent.photo_board,(x,y),self.rad,(self.b,self.g,self.r),-1)
		elif event==cv.EVENT_MOUSEMOVE:
			if self.drawing_flag==True:
				cv.circle(self.parent.photo_board,(x,y),self.rad,(self.b,self.g,self.r),-1)
		elif event==cv.EVENT_LBUTTONUP:
			self.drawing_flag=False
			cv.circle(self.parent.photo_board,(x,y),self.rad,(self.b,self.g,self.r),-1)
	def draw_rec(self,event,x,y):
		if event==cv.EVENT_LBUTTONDOWN:
			self.ix=x
			self.iy=y
		elif event==cv.EVENT_LBUTTONUP:
			cv.rectangle(self.parent.photo_board,(self.ix,self.iy),(x,y),(self.b,self.g,self.r),-1)
	def draw_ellipse(self,event,x,y):
		if event==cv.EVENT_RBUTTONUP:
			maj_axis=int(sqrt(pow(self.pts[2]-self.pts[0],2)+pow(self.pts[3]-self.pts[1],2)))
			min_axis=int(sqrt(pow(self.pts[4]-self.pts[0],2)+pow(self.pts[5]-self.pts[1],2)))
			cv.ellipse(self.parent.photo_board,(self.pts[0],self.pts[1]),(maj_axis,min_axis),0,0,360,(self.b,self.g,self.r),-1)
			self.pts=[]
		elif event==cv.EVENT_LBUTTONUP:
			self.pts+=[x,y]
		
	def draw_line(self,event,x,y):
		if event==cv.EVENT_LBUTTONDOWN:
			self.ix=x
			self.iy=y
		elif event==cv.EVENT_LBUTTONUP:
			cv.line(self.parent.photo_board,(self.ix,self.iy),(x,y),(self.b,self.g,self.r),self.rad)
	def draw_polyline(self,event,x,y):
		self.draw_polygon(event,x,y,False)
	def draw_polygon(self,event,x,y,flag=True):
		if event==cv.EVENT_RBUTTONUP:
			p=np.array(self.pts,np.int32)
			p=p.reshape((-1,1,2))
			cv.polylines(self.parent.photo_board,[p],flag,(self.b,self.g,self.r),self.rad)
			self.pts=[]
		elif event==cv.EVENT_LBUTTONUP:
			self.pts+=[[x,y]]
	def draw_eraser(self,event,x,y):
		if event==cv.EVENT_LBUTTONDOWN:
			self.drawing_flag=True
			cv.circle(self.parent.photo_board,(x,y),self.rad,(255,255,255),-1)
		elif event==cv.EVENT_MOUSEMOVE:
			if self.drawing_flag==True:
				cv.circle(self.parent.photo_board,(x,y),self.rad,(255,255,255),-1)
		elif event==cv.EVENT_LBUTTONUP:
			self.drawing_flag=False
			cv.circle(self.parent.photo_board,(x,y),self.rad,(255,255,255),-1)
	def disp_palette(self):
		self.pal=np.zeros((512,512,3),np.uint8)
		cv.namedWindow('Palette',cv.WINDOW_NORMAL)
		cv.createTrackbar('Red','Palette',0,255,self.get_red)
		cv.createTrackbar('Green','Palette',0,255,self.get_green)
		cv.createTrackbar('Blue','Palette',0,255,self.get_blue)
		cv.createTrackbar('Brush Radius','Palette',0,10,self.get_radius)
		cv.createTrackbar(self.switch,'Palette',0,1,self.get_switch)
		while True:
			cv.imshow('Palette',self.pal)
			if cv.waitKey(1)==ord('q'):
					break
			if self.enable_pal_flag==True:
				self.pal[:]=[self.b,self.g,self.r]
			else:
				self.pal[:]=[0,0,0]
		cv.destroyWindow('Palette')
		
	def back(self):
		self.enable_editing_flag=False
		self.parent.disp_menu()
	
#callback functions
###################
	def pedit_ops_callback(self,event,x,y,flags,param):	
		if(limit_check(self.options[('limits',None)],x,y)):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				self.selected_option=check_param(self.options,x,y,False)
				if(self.selected_option[0]=='Back'):
					self.selected_option[1]()
				elif(self.selected_option[0]=='Palette'):
					self.selected_option[1]()
	def pboard_callback(self,event,x,y,flags,param):
		if self.enable_editing_flag:
			if self.selected_option[0]!=('Palette'):
				self.selected_option[1](event,x,y)
				cv.imshow('Photo-Board',self.parent.photo_board)
			
	def get_red(self,x):
		if self.enable_pal_flag:
			self.r=x
	def get_blue(self,x):
		if self.enable_pal_flag:
			self.b=x
	def get_green(self,x):
		if self.enable_pal_flag:
			self.g=x
	def get_switch(self,x):
		if x==1:
			self.enable_pal_flag=True
			self.r=cv.getTrackbarPos('Red','Palette')
			self.g=cv.getTrackbarPos('Green','Palette')
			self.b=cv.getTrackbarPos('Blue','Palette')
			self.rad=cv.getTrackbarPos('Brush Radius','Palette')
		else:
			self.enable_pal_flag=False
	def get_radius(self,x):
		if self.enable_pal_flag:
			if(x==0):
				self.rad=1
			else:
				self.rad=x
	
###################
#Video-editor
###################
class video_editor:
	def __init__(self):
		self.vmenu=0
		self.options={
				('Video-Editor',None):([(30,20),(460,50),(0,100,255),-1],[(35,45),font,1,(0,255,255),4,line]),
				('1.Play A Video(muted)',self.play_video):([(30,100),(460,130),(0,100,255),-1],[(35,125),font,1,(0,255,255),4,line]),
				('2.Record Camera(muted)',self.cam_rec):([(30,140),(460,170),(0,100,255),-1],[(35,165),font,1,(0,255,255),4,line]),
				('3.Record Screen(muted)',self.screen_rec):([(30,180),(460,210),(0,100,255),-1],[(35,205),font,1,(0,255,255),4,line]),
				('4.Back',self.back):([(30,220),(460,250),(0,100,255),-1],[(35,245),font,1,(0,255,255),4,line]),
				('limits',None):([30,460],[100,250])
				}
				#():([],[]),

		self.vmenu=np.ones((512,512,3),np.uint8)
		self.vmenu*=255
		generate_menu(self.vmenu,self.options)
		
	
	def disp_menu(self):
		cv.imshow('Menu',self.vmenu)
		cv.setMouseCallback('Menu',self.veditor_callback)
#functions for options
######################
	def play_video(self):
		filename=input("Enter the filename(with extension):").strip()	
		cap=cv.VideoCapture(filename)
		cv.namedWindow('Video-Board',cv.WINDOW_NORMAL)
		while cap.isOpened():
			ret,frame=cap.read()
			if not ret:
				print("Unable to receive frame(stream end?)Exiting....")
				break
			cv.imshow('Video-Board',frame)
			cv.waitKey(35)
		cap.release()
	def cam_rec(self):
		filename=input("Enter the filename(without extension):").strip()	
		filename+='.avi'
		fourcc=cv.VideoWriter_fourcc(*'XVID')
		cap=cv.VideoCapture(0)
		out=cv.VideoWriter(filename,fourcc,30,(640,480))
		cv.namedWindow('Video-Board',cv.WINDOW_NORMAL)
		while cap.isOpened():
			ret,frame=cap.read()
			if not ret:
				print("Unable to receive frame(stream end?)Exiting....")
				break
			cv.imshow('Video-Board',frame)
			out.write(frame)
			if cv.waitKey(1)==ord('q'):
				break
		cap.release()
		out.release()
	def screen_rec(self):
		print("Press 'q' to exit")
		filename=input("Enter the filename(without extension):").strip()	
		filename+='.avi'
		fourcc=cv.VideoWriter_fourcc(*'XVID')
		out=cv.VideoWriter(filename,fourcc,3,(1920,1080))
		cv.namedWindow('Video-Board',cv.WINDOW_NORMAL)
		cv.resizeWindow('Video-Board',640,480)
		while True:
			img=pyautogui.screenshot()
			frame=np.array(img)
			frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
			cv.imshow('Video-Board',frame)
			out.write(frame)
			if cv.waitKey(1)==ord('q'):
				break
		out.release()
	def back(self):
		cv.destroyAllWindows()
		m.disp_menu()
#callback functions
###################
	def veditor_callback(self,event,x,y,flags,param):
		if(limit_check(self.options[('limits',None)],x,y)):
			pass
		else:
			if event==cv.EVENT_LBUTTONUP:
				check_param(self.options,x,y)
m=main_menu()
m.prog_start()

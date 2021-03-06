import tkinter as tk
from .firebase import firebase
from tkinter import messagebox
import urllib
import requests
import json
from encryption import encrypt



def signin(signup=None):
	auth = firebase.init()

	def checkconn():
		try:
			urllib.request.urlopen('http://216.58.192.142', timeout=1)
			return True
		except: 
			return False

	window = tk.Toplevel()
	window.config(bg="white")
	window.resizable(False,False)
	window.attributes('-topmost', True)
	window.title("Sign In")

	def reset(arg):
		_email_ = str(email.get())
		if _email_ == "":
			messagebox.showerror("Error","Please enter your email to reset password")
		else:
			if _email_.find("@") != -1 and _email_.find(".") != -1:
				try:
					firebase.reset(auth,_email_)
					messagebox.showinfo("Sent!","The reset link has been sent to your email adress")
				except requests.exceptions.HTTPError as e:
					error_json = e.args[1]
					error = json.loads(error_json)['error']['message']
					messagebox.showerror("Error",error)
				
			else:
				messagebox.showerror("Please enter a valid email")
	def _signin_(arg=None):
		_email_ = str(email.get())
		_password_ = str(password.get())
		if _email_ == "" or password == "":
			messagebox.showerror("Error","Please fill all fields")
		else:
			if _email_.find("@") != -1 and _email_.find(".") != -1:
				if checkconn() == False:
					messagebox.showerror("Error","No connection detected please check your internet connection")
				else:
					try:
						firebase.signin(auth=auth,email=str(email.get()),password=str(password.get()))
						window.destroy()
						data = [_email_,_password_]
						return data
						
					except:
						messagebox.showerror("Alert","Couldn't sign in check your email and password and please try again")
						
			else:
				messagebox.showerror("Error","Please enter a valid email id")

	global passw_hide
	passw_hide = True

	def pass_show_hide(arg):
		global passw_hide
		if passw_hide == True:
			password.config(show="")
			eye.config(text="􀋮")
			passw_hide = False
		elif passw_hide == False:
			password.config(show="*")
			eye.config(text="􀋰")
			passw_hide = True

	font = "avenir"


	tk.Label(window,text="Email Id:",font=(font,16),fg="black",bg="white").grid(row=1,column=0,pady=20,padx=20)

	email = tk.Entry(window,font=(font,16),fg="black",bg="white",insertbackground="black")
	email.grid(row=1,column=1,pady=20,padx=20)

	tk.Label(window,text="Password:",font=(font,16),fg="black",bg="white").grid(row=2,column=0,pady=0,padx=20)

	password = tk.Entry(window,font=(font,16),fg="black",bg="white",show="*",insertbackground="black")
	password.grid(row=2,column=1,pady=0,padx=20)

	eye = tk.Label(window,fg="grey",bg="white",text="􀋰",font=(font,16))
	eye.grid(row=2,column=2,sticky=tk.W)
	eye.bind("<Button-1>",pass_show_hide)

	reset_ = tk.Label(window,text="forgot passsword? Reset it",bg="white",fg="blue")
	reset_.grid(row=3,column=1,pady=(0,20),padx=20)
	reset_.bind("<Button-1>",reset)

	def signin_(arg=None):
		 data = _signin_()
		 data = {"email":encrypt(data[0]),"password":encrypt(data[1])}
		 file = open("henrymolar.settings","w")
		 json.dump(data,file)


	signin = tk.Button(window,font=(font,16),text="Sign In",command=signin_)
	signin.grid(row=4,column=0,columnspan=2,pady=(20,0))
	
	def __signin__(arg=None):
		window.destroy()
		signup()

	signup_ = tk.Label(window,text="or sign up",bg="white",fg="blue")
	signup_.grid(row=5,column=0,columnspan=2)
	signup_.bind("<Button-1>",__signin__)

	def setfocus(widget):
		widget.focus_set()

	email.focus_set()
	email.bind("<Return>",lambda event: setfocus(widget=password))
	email.bind("<Down>",lambda event: setfocus(widget=password))

	password.bind("<Up>",lambda event: setfocus(widget=email))
	password.bind("<Return>",lambda event: setfocus(widget=signin))
	password.bind("<Down>",lambda event: setfocus(widget=signin))

	signin.bind("<Up>",lambda event: setfocus(widget=password))
	signin.bind("<Return>",signin_)


if __name__ == "__main__":
	signin()
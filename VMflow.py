import tkinter
import tkinter as tk
from tkinter import filedialog as browser
from tkinter import messagebox
import PIL
import whois
import ipaddress
import json
from PIL import ImageTk, Image
import threading
import nmap
import requests
import xmltodict
import time
from datetime import datetime
from xlwt import Workbook
import xlrd

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def update_placeholder(self, place_holder):
        self.delete(0, tk.END)
        self.insert(0, place_holder)
        self['fg'] = self.placeholder_color

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def get_date():
	date = datetime.now()
	return "{}-{}-{}-{}-{}-{}".format(date.year,date.month,date.day,date.hour,date.minute,date.second)

global keys,datval
def findkey(strt,m,n,w):
    global keys, datval
    for i in m:
        #print(type(i))
        if(type(m[i])==n):
            findkey(strt+i+'_',m[i],n,w)
        else:
            if(strt+i not in keys):
                keys.append(strt+i)


def extract(strt,m,n,w):
    for i in m:
        #print(type(i))
        if(type(m[i])==n):
            extract(strt+i+'_',m[i],n,w)
        else:
            datval[strt+i]=str(m[i]).replace('\u200b',' ').replace("\n",' ').replace(',',';')

def get_qapi():
	global qapiframe, E1, keys, datval
	infile = E1.get()
	print(infile)
	keys = []
	datval = {}
	url = "https://qualysapi.qualys.com/qps/rest/1.0/search/am/tag"

	payload = "<ServiceRequest>\r\n<preferences>\r\n<limitResults>1000</limitResults>\r\n</preferences>\r\n<filters>\r\n<Criteria field=\"name\" operator=\"CONTAINS\">{}</Criteria>\r\n</filters>\r\n</ServiceRequest> ".format(infile)
	headers = {
		'Content-Type': "text/xml",
		'X-Requested-With': "QualysPostman",
		'Authorization': "Basic ZGV0dGVfa3QzOlQzJHRlckAxMjM=",
		'User-Agent': "PostmanRuntime/7.13.0",
		'Accept': "*/*",
		'Cache-Control': "no-cache",
		'Postman-Token': "495cfc62-44d8-4c9c-84a7-190c4ad720e7,908b9898-1a59-4616-8e88-96f85bf29ee7",
		'Host': "qualysapi.qualys.com",
		'accept-encoding': "gzip, deflate",
		'content-length': "196",
		'Connection': "keep-alive",
		'cache-control': "no-cache"
		}
	print(payload)
	response = requests.request("POST", url, verify=False, data=payload, headers=headers)



	#print(response.text)
	print('\n\n\n\n')
	data = xmltodict.parse(response.text)

	with open("qualys-tag.csv","w") as w:
		for i in data['ServiceResponse']['data']['Tag']:
			print(i)
			findkey("",i,type(data),w)
	#        break
		print(keys)
		for i in sorted(keys):
			w.write(i)
			w.write(',')
		w.write('\n')
		for i in data['ServiceResponse']['data']['Tag']:
			#print(i)
			datval = {}
			extract("", i, type(data), w)
			for key in sorted(keys):
				if(key in datval):
					w.write(datval[key])
					w.write(',')
				else:
					w.write(',')
			w.write("\n")
		w.close()
	qapiframe.destroy()
	print("List of tags been successfully printed to excel sheet")


def get_nmap():
	#infile = input("Please enter filename : ")
	global whoisframe, E1
	infile = E1.get()
	print(infile)
	nm = nmap.PortScanner()
	with open("output_nmap.csv", "w") as wr:
		with open(infile, "r") as f:
			d = f.readline()
			while d:
				entry = d.split(',')
				result=nm.scan(entry[0],entry[1])
				print(result)
				wr.write(result.__str__())
				d = f.readline()
	whoisframe.destroy()
	f.close()
	wr.close()
def get_filepath():
	filename = browser.askopenfilename(initialdir="/", title="Select file", filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
	return filename

def get_dirpath():
	filename = browser.askdirectory()
	return filename

def copytoclip(txt, out):
	val = txt.get("1.0", 'end-1c')
	out.clipboard_clear()
	out.clipboard_append(val)

def savedata(path, data):
	wb = Workbook()
	sheetwhois = wb.add_sheet('Whois')
	for entry in data:
		col=0
		for key in entry:
			sheetwhois.write(0, col, key)
			col+=1
		break
	row=1
	for entry in data:
		col=0
		for key in entry:
			sheetwhois.write(row ,col,str(entry[key]))
			col+=1
		row+=1
	wb.save(path)
	messagebox.showinfo("Success", "Successfully saved to "+path)

def get_whois(v):
	#infile = input("Please enter filename : ")
	global whoisframe, E1
	infile = E1.get()
	print(infile)
	outframe = tk.Frame(whoisframe, background="black")
	outframe.place(x=0, y=0, anchor="nw", width=900, height=400)

	txt = tk.Text(outframe, state='disabled', height=20, width=110)
	txt.place(x=10, y=10)
	#time.sleep(20)
	lookupdata=[]
	if(v==2):
		wb = xlrd.open_workbook(infile)
		sheet = wb.sheet_by_index(0)
		for i in range(sheet.nrows):
			lookup = whois.whois(sheet.cell_value(i, 0).strip())
			print(lookup)
			txt.config(state='normal')
			txt.insert('end',lookup)
			txt.config(state='disable')
			lookupdata.append(lookup)
			#wr.write(lookup.__str__())
	else:
		lookup = whois.whois(infile)
		lookupdata.append(lookup)
		txt.config(state='normal')
		txt.insert('end',lookup)
		txt.config(state='disable')
		print(lookup)

	E13 = EntryWithPlaceholder(outframe, "Output file path")
	E13.config(width=40, font='large_font')
	buttonfolder = tk.Button(outframe,
							 text="Browse",
							 command=lambda: E13.update_placeholder(get_dirpath()+'/whois_'+get_date()+'.xls'))

	buttonfolder.config(width=15, height=1)
	E13.place(x=20, y=360)
	buttonfolder.place(x=470, y=360)

	buttonsave = tk.Button(outframe,
							 text="Save",
							 command=lambda: savedata(E13.get(),lookupdata))

	buttonsave.config(width=15, height=1)
	buttonsave.place(x=600, y=360)
	buttoncopy = tk.Button(outframe,
							 text="Copy to Clipboard",
							 command=lambda: copytoclip(txt,outframe))

	buttoncopy.config(width=15, height=1)
	buttoncopy.place(x=730, y=360)
	currentframe=outframe
	buttonback = tk.Button(mainframe,
							 text="Back",
						     fg='red',
							 command=lambda: currentframe.destroy())

	buttonback.config(width=10, height=1)
	buttonback.place(x=710, y=5)
	#whoisframe.destroy()
def twhois(v):
	print(v)
	x = threading.Thread(target=get_whois, args=(v))
	x.start()
	
def tnmap():
	print("starting")
	x = threading.Thread(target=get_nmap)
	x.start()
	
def tqapi():
	print("starting")
	x = threading.Thread(target=get_qapi)
	x.start()
	
def destroy():
	global frameGlobal
	frameGlobal.destroy()

def whois_lambda(EntryObject, BrowseButton, placeholder, fileInput):
	EntryObject.update_placeholder(placeholder)
	if fileInput:
		BrowseButton.place(x=370, y=50)
	else:
		BrowseButton.place_forget()
def disp(event):
	print("enter")
def run_whois():
	global root, mainframe, whoisframe, E1, frameGlobal
	whoisframe = tk.Frame(mainframe, background="black")
	whoisframe.place(x=0, y=200, anchor="nw", width=900, height=400)
	#L1 = tk.Label(text="Enter file name ")
	#L1.pack()
	v = tk.IntVar()
	buttonbrowse = tk.Button(whoisframe,
							 text="Browse",
							 command=lambda: E1.update_placeholder(get_filepath()))

	buttonbrowse.config(width=20, height=1)
	E1 = EntryWithPlaceholder(whoisframe, "IP / Domain")
	E1.config(width=30, font='large_font')
	E1.place(x=20,y=50)
	tk.Radiobutton(whoisframe,
				   text="Input File",
				   padx=20,
				   bg="grey",
				   fg="blue",
				   borderwidth="6",
				   variable=v,
				   command = lambda : whois_lambda(E1,buttonbrowse,'Input file',True),
				   value=2).place(x=150,y=0)
	tk.Radiobutton(whoisframe,
				   text="IP/Domain",
				   padx=20,
				   bg="grey",
				   fg="blue",
				   borderwidth="6",
				   variable=v,
				   command = lambda : whois_lambda(E1,buttonbrowse,'IP / Domain', False),
				   value=1).place(x=10,y=0)

	frameGlobal = whoisframe

	buttonwhois = tk.Button(whoisframe,
					text= "Execute ->",
					command = lambda : get_whois(v.get()))


	#bind("<Return>", (lambda event: name_of_function()))
	buttonwhois.config(width=20, height=1)
	buttonwhois.place(x=50,y=100)
	buttonHome = tk.Button(whoisframe,
					text= "Home",
					command = destroy)
		
	buttonHome.config(width=20, height=1)					
	buttonHome.place(x=40,y=140)

	
	
	
def run_nmap():
	global root, mainframe, whoisframe, E1, frameGlobal
	whoisframe = tk.Frame(mainframe, background="black")
	whoisframe.place(x=0, y=200, anchor="nw", width=600, height=400)
	#L1 = tk.Label(text="Enter file name ")
	#L1.pack()
	E1 = tk.Entry(whoisframe, bd =5)
	E1.pack()
	frameGlobal = whoisframe
	
	buttonwhois = tk.Button(whoisframe,
					text= "Go ->",
					command = tnmap)
					
				
	buttonwhois.config(width=20, height=1)					
	buttonwhois.pack(pady = 5)
	
	buttonHome = tk.Button(whoisframe,
					text= "Home",
					command = destroy)
		
	buttonHome.config(width=20, height=1)					
	buttonHome.pack(pady = 5)


def get_iprc():
	#print("insert ip range counter functionality")
	global iprcframe, E1
	infile = E1.get()
	print(infile)
	#infile = input("Please enter filename : ")
	with open("output.csv", "w") as w:
		with open(infile, "r") as f:
			d = f.readline()
			while d:
				d=d.strip()
				data = d.split("-")
				if len(data)==2:
					ip1 = int(ipaddress.IPv4Address(data[0].strip()))
					ip2 = int(ipaddress.IPv4Address(data[1].strip()))
					cnt = ip2 - ip1 +1
					print(ip2)
				elif len(d.strip())==0:
					cnt=0
				else:
					cnt = 1
				w.write(d.strip()+','+str(cnt)+'\n')
				d = f.readline()
		f.close()
	iprcframe.destroy()
	w.close()
	

def run_iprc():
	#print("insert ip range counter functionality")
	global root, mainframe, iprcframe, E1, frameGlobal
	iprcframe = tk.Frame(mainframe, background="black")
	iprcframe.place(x=0, y=200, anchor="nw", width=600, height=400)
	#L1 = tk.Label(text="Enter file name ")
	#L1.pack()
	E1 = tk.Entry(iprcframe, bd =5)
	E1.pack()
	frameGlobal = iprcframe
	buttonwhois = tk.Button(iprcframe,
					text= "Go ->",
					command = get_iprc)

	buttonwhois.config(width=20, height=1)					
	buttonwhois.pack(pady = 5)
	#When ever Home button is called, destroy function executes using the frame global.
	
	frameGlobal = iprcframe
	buttonHome = tk.Button(iprcframe,
					text= "Home",
					command = destroy)
		
	buttonHome.config(width=20, height=1)					
	buttonHome.pack(pady = 5)
	
	
def run_qcve():
	print("insert qualys CVE Search functionality")

def run_qapi():
	#print("insert qualys api functionality")
	global root, mainframe, qapiframe, E1, frameGlobal
	qapiframe = tk.Frame(mainframe, background="black")
	qapiframe.place(x=0, y=200, anchor="nw", width=600, height=400)
	#L1 = tk.Label(text="Enter file name ")
	#L1.pack()
	E1 = tk.Entry(qapiframe, bd =5)
	E1.pack()
	frameGlobal = qapiframe
	buttonwhois = tk.Button(qapiframe,
					text= "Go ->",
					command = tqapi)

	buttonwhois.config(width=20, height=1)					
	buttonwhois.pack(pady = 5)
	#When ever Home button is called, destroy function executes using the frame global.
	
	frameGlobal = qapiframe
	buttonHome = tk.Button(qapiframe,
					text= "Home",
					command = destroy)
		
	buttonHome.config(width=20, height=1)					
	buttonHome.pack(pady = 5)
	
def run_snow():
	print("insert snow functionality")	


def RequestCred(msg):
    popup = tk.Tk()
    popup.geometry("500x330")
    popup.bg = 'black'
    popup.title("Authentication Credentials")
    popup.wm_title("Authentication Credentials")
    framemain = tk.Frame(popup, background="black")
    inframe = tk.Frame(popup, background="black")
    framemain.place(x=0, y=0, anchor="nw", width=500, height=330)
    inframe.place(x=0, y=100, anchor="nw", width=500, height=200)
    path = "Picture2.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(popup, image = img, border=0)
    panel.pack(side = "left",  expand = "no")
    panel.place(relx=0.0, rely=0.0, anchor="nw")
    label = tk.Label(inframe, text=msg, font=("Helvetica", 10))
    label.pack(side="top", fill="x", pady=10)
    inframe.grid(column=0, row=3, padx=15, pady=180)
    user = EntryWithPlaceholder(inframe, "Username")
    user.pack(pady=2)
    passw = EntryWithPlaceholder(inframe, "Password")
    passw.pack(pady=2)
    B1 = tk.Button(inframe, text="Submit", command = popup.destroy)
    B1.pack(pady=2)
    popup.mainloop()

whoisframe = ""
E1= ""

print(get_date())


#RequestCred("Login Credentials")

root = tk.Tk()
root.geometry("900x600")
root.bg = 'black'
root.title("DTTL Vulnerability Management Service(VMS)")

mainframe = tk.Frame(root, background="black")
labelframe = tk.Frame(mainframe, background="black")
buttonframe = tk.Frame(mainframe, background="black")


mainframe.place(x=0, y=0, anchor="nw", width=900, height=600)
labelframe.place(x=0, y=0, anchor="nw", width=900, height=150)
buttonframe.place(x=0, y=150, anchor="nw", width=900, height=450)

path = "Picture2.jpg"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image = img, border=0)
panel.pack(side = "left",  expand = "no")
panel.place(relx=0.0, rely=0.0, anchor="nw")

# path = "Picture3.jpg"
# img2 = ImageTk.PhotoImage(Image.open(path))
# panel2 = tk.Label(root, image = img2, border=0)
# panel2.pack(side = "left",  expand = "no")
# panel2.place(relx=0.0, rely=0.0, anchor="s")

#self.nw.place(relx=0.0, rely=0.0, anchor="nw")

buttonframe.grid(column=0, row=7, padx=15, pady=200)		 

		 

button1 = tk.Button(buttonframe,
					text= "Whois",
					command = run_whois)
button1.config(width=20, height=1)					
button1.pack(pady = 5)
				
button2 = tk.Button(buttonframe,
					text= "NMAP",
					command = run_nmap)
button2.config(width=20, height=1)					
button2.pack(pady = 5)
				
button4 = tk.Button(buttonframe,
					text= "IP Range Counter",
					command = run_iprc)
button4.config(width=20, height=1)
button4.pack(pady = 5)					
					
button5 = tk.Button(buttonframe,
					text= "Qualys CVE Search",
					command = run_qcve)
button5.config(width=20, height=1)
button5.pack(pady = 5)
					
button6 = tk.Button(buttonframe,
					text= "Qualys API",
					command = run_qapi)				
button6.config(width=20, height=1)
button6.pack(pady = 5)

button7 = tk.Button(buttonframe,
					text= "ServiceNow Ticketing", fg = 'red',
					command = run_snow)				
button7.config(width=20, height=1)
button7.pack(pady = 5)

button = tk.Button(mainframe,
                   text="QUIT", 
                   fg="red",
                   command=quit)
button.place(x=800, y=5)
button.config(width=10, height=1)

w = tk.Label(buttonframe, text="DTTL Vulnerability Management Service(VMS)" , background = "black", fg = "white", width = 40, font = "Helvetica 8")	
w.pack(pady = 70)
root.iconbitmap('Deloitte.ico')
root.mainloop()

import sqlite3
import tkinter as tk
from tkinter import*
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pymongo
import string
import secrets
from customtkinter import*
from PIL import Image

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
def login():
    global mainpass 
    mainpass=password_entry.get()

def generate_key():
    password = b"password"
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key
    # return Fernet.generate_key()

def encrypt_password(key, password):
    plaintext = password.encode()
    f = Fernet(key)
    enctext = f.encrypt(plaintext)
    enctext = enctext.decode()
    return enctext


def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def generator():
    upper = list(string.ascii_uppercase)
    lower = list(string.ascii_lowercase)
    digits = list(string.digits)
    punctuation = list(string.punctuation)

    all=upper+lower+digits+punctuation
    password_len=int(slider.get())
    part1 = round(password_len * (30 / 100))#letters %60
    part2 = round(password_len * (20 / 100))#digits+punc %40
    #print(password_len)
    password=""
    for i in range(part1):
        password += secrets.choice(upper)
        password += secrets.choice(digits)

    for i in range(part2):
        password += secrets.choice(punctuation)
        password += secrets.choice(lower)

    password_entry.insert(0,password)
    messagebox.showinfo("genereted pass",password_entry.get())
        
def Create_account_table ():    
    Connection= sqlite3.connect("Data.db")
    cursor= Connection.cursor()
    cursor.execute('CREATE TABLE books(service text  ,username text ,password text)')
    Connection.commit()
    Connection.close()
  
key = generate_key()    

def add_password():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    mycol = mydb[service+mainpass]

    if service and username and password:
        encrypted_password = encrypt_password(key, password)
        Connection= sqlite3.connect("Data.db")
        cursor= Connection.cursor()
        cursor.execute('INSERT INTO books VALUES(?,?,?)',(service,username,encrypted_password))
        Connection.commit()
        Connection.close()
        dict={"name":service , "key": key,"username":username,"pass1":encrypted_password}
        mycol.insert_one(dict)
        messagebox.showinfo("Success", "Password added successfully!")
    else:
        messagebox.showwarning("Error", "Please fill in all the fields.")

def get_password():
    service = service_entry.get()
    mycol = mydb[service+mainpass]
    Connection= sqlite3.connect("Data.db")
    cursor= Connection.cursor()
    cursor.execute('SELECT * FROM books where service = ?',(service,))
    password=[ row[2] for row in cursor.fetchall()]
    print(password)
    username=[ row[1] for row in cursor.fetchall()]
    print(cursor.fetchall())
    Connection.commit()
    Connection.close()
    x = mycol.find({"name":service},{ "_id": 0, "name": 1, "key": 1 ,"username":1,"pass1":1})
    
    if password :
        for i in range(len(password)):
            key=x[i]["key"]
            username=x[i]["username"]
            decrypted_password = decrypt_password(key,x[i]["pass1"])
            messagebox.showinfo("Password", f"Username: {username}\nPassword: {decrypted_password}")
            
    else:
        messagebox.showwarning("Error", "Password not found.")        
        

instructions = '''First login by entrinh username and master password
To add password fill all the fields and press "Add Password"
To view password, enter Account Name and press "Get Password"
to generate a random stong password select length of password and press"Generate"'''
signature = "project by ayush "

from customtkinter import*
from PIL import Image
win=CTk()
win.title("Password Manager")
win.geometry("1050x500+100+330")
win.resizable(False,False)


bg_img=CTkImage(dark_image=Image.open("wallpaperbetter.jpg"),size=(1050,500))
bg_lab=CTkLabel(win,image=bg_img,text="")
bg_lab.place(x=0,y=0)

frame1=CTkFrame(win,fg_color="violetRed1",bg_color="RoyalBlue4",height=470,width=760,corner_radius=0)
frame1.place(x=300,y=15)

#INSTRUCTIONS

lab1=CTkLabel(frame1,text="First login by entering username and master password",text_color="black",fg_color="light goldenrod",corner_radius=10,font=("Agency",16))
lab1.place(x=170,y=20)

lab2=CTkLabel(frame1,text="To add passowrd fill all the fields and press Add Password ",text_color="black",fg_color="light goldenrod",corner_radius=10,font=("Agency",16))
lab2.place(x=153,y=50)

lab3=CTkLabel(frame1,text="To view password enter Account Name and press Get Password",text_color="black",fg_color="light goldenrod",corner_radius=10,font=("Agency",16))
lab3.place(x=133,y=80.5)

lab4=CTkLabel(frame1,text="To generate a random strong password select length of password and press ""Generate""",text_color="black",fg_color="light goldenrod",corner_radius=10,font=("Agency",16))
lab4.place(x=58,y=111)

#ACC,PASS,USER LABELS

lab5=CTkLabel(frame1,text="ACCOUNT:",text_color="black",corner_radius=10,font=("Agency",16))
lab5.place(x=245,y=180)

lab6=CTkLabel(frame1,text="USERNAME:",text_color="black",corner_radius=10,font=("Agency",16))
lab6.place(x=234,y=210)

lab7=CTkLabel(frame1,text="PASSWORD:",text_color="black",corner_radius=10,font=("Agency",16))
lab7.place(x=230,y=240)

#ENTRY FIELDS

service_entry=CTkEntry(frame1,fg_color="pink1",text_color="black",placeholder_text="account",placeholder_text_color="slate gray",border_width=3,border_color="light goldenrod")
service_entry.place(x=370,y=180)

username_entry=CTkEntry(frame1,fg_color="pink1",text_color="black",placeholder_text="username",placeholder_text_color="slate gray",border_width=3,border_color="light goldenrod")
username_entry.place(x=370,y=210)

password_entry=CTkEntry(frame1,fg_color="pink1",text_color="black",placeholder_text="password",placeholder_text_color="slate gray",border_width=3,border_color="light goldenrod")
password_entry.place(x=370,y=240)

#BUTTONS

img=CTkImage(dark_image=Image.open("getpass.png"),size=(150,30))
btn=CTkButton(frame1,image=img,height=5,width=50,text="",hover_color="light goldenrod",border_color="black",border_width=2,corner_radius=20,cursor="hand2",command=get_password)
btn.place(x=100,y=285)

img1=CTkImage(dark_image=Image.open("generate.png"),size=(150,30))
btn1=CTkButton(frame1,image=img1,height=5,width=50,text="",hover_color="light goldenrod",border_color="black",border_width=2,corner_radius=20,cursor="hand2",command=generator)
btn1.place(x=290,y=285)

img2=CTkImage(dark_image=Image.open("addpass.png"),size=(150,30))
btn2=CTkButton(frame1,image=img2,height=5,width=50,text="",hover_color="light goldenrod",border_color="black",border_width=2,corner_radius=20,cursor="hand2",command=add_password)
btn2.place(x=480,y=285)

img3=CTkImage(dark_image=Image.open("login.png"),size=(150,30))
btn3=CTkButton(frame1,image=img3,height=5,width=50,text="",hover_color="light goldenrod",border_color="black",border_width=2,corner_radius=20,cursor="hand2",command=login)
btn3.place(x=385,y=350)

#SIZE FOR GENERATION

lab8=CTkLabel(frame1,text="CHOOSE SIZE",text_color="black",corner_radius=10,font=("Agency",16))
lab8.place(x=91,y=342)

#SLIDER FOR GENERATION

def sliding(value):
    lab9.configure(text=value)

lab9=CTkLabel(frame1,text="",fg_color="light goldenrod",corner_radius=5,text_color="black",font=("Agency",20))
lab9.place(x=105,y=380)

slider=CTkSlider(master=frame1,from_=8,to=16,number_of_steps=8,button_color="cyan2",progress_color="light goldenrod",orientation="horizontal",command=sliding)
slider.place(x=197,y=375,anchor="center")

#SIGNATURE

lab10=CTkLabel(frame1,text="A Project by Abdul Aman & Aminesh Bajpai",text_color="black",corner_radius=10,font=("Agency",16))
lab10.place(x=420,y=435)

win.mainloop()


from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from timezonefinder import TimezoneFinder
import webbrowser

root = Tk()
root.title("Weather App 1.0")
root.geometry("750x470+300+200")
root.resizable(False,False)
root.config(bg="#202731")

news_win = None

def open_news_window():
    global news_win
    if news_win is not None and news_win.winfo_exists():
        news_win.lift()
        return

    news_win = Toplevel(root)
    news_win.title("Vijesti")
    news_win.geometry("400x300")
    news_win.config(bg="#202731")

    vijesti = [
        ("Gotovo: Kevin de Brujne stigao u Napulj", "https://www.vijesti.me/sport/fudbal/762375/gotovo-kevin-de-brujne-stigao-u-napulj"),
        ("Odbojkašice u Kapošvaru za kraj Zlatne lige", "https://www.vijesti.me/sport/odbojka/762302/odbojkasice-u-kaposvaru-za-kraj-zlatne-lige"),
        ("Franc Vagner potvrdio nastup na Eurobasketu", "https://www.vijesti.me/sport/kosarka/762365/franc-vagner-potvrdio-nastup-na-eurobasketu"),
        ("Oklahoma savladala Indijanu i izjednačila u seriji", "https://www.vijesti.me/sport/kosarka/761862/oklahoma-savladala-indijanu-i-izjednacila-u-seriji"),
        ("Alkaras: Pariz će biti zauvijek u mom srcu", "https://www.vijesti.me/sport/tenis/761850/alkaras-pariz-ce-biti-zauvijek-u-mom-srcu"),
        ("Luča osvojila dvije medalje u Varni", "https://www.vijesti.me/sport/ostali-sportovi/761701/luca-osvojila-dvije-medalje-u-varni"),
        ("Erani i Paolini najbolji ženski dubl Rolan Garosa", "https://www.vijesti.me/sport/tenis/761786/erani-i-paolini-najbolji-zenski-dubl-rolan-garosa"),
        ("Mark Markes slavio u sprint trci u Aragonu", "https://www.vijesti.me/sport/ostali-sportovi/761725/mark-markes-slavio-u-sprint-trci-u-aragonu"),
    ]

    def open_link(url):
        webbrowser.open_new_tab(url)

    for title, url in vijesti:
        link = Label(news_win, text=title, fg="#81ecec", cursor="hand2", bg="#202731", font=("Arial", 12, "underline"))
        link.pack(anchor="w", pady=7, padx=10)
        link.bind("<Button-1>", lambda e, url=url: open_link(url))

    def on_close():
        global news_win
        news_win.destroy()
        news_win = None

    news_win.protocol("WM_DELETE_WINDOW", on_close)
    
btn_vijesti = Button(root, text="Vijesti", bg="#81ecec", fg="#202731", cursor="hand2", font=("Arial", 10, "bold"), command=open_news_window)
btn_vijesti.place_forget()

def open_playlist(url):
    webbrowser.open_new_tab(url)

def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)
    
    long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")
    
    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    
    api_key="cf249ee00c342e84d0d5bafcf59b7c31"
    api =f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    json_data=requests.get(api).json()
    print(json_data)
    
    current= json_data['list'][0]
    temp=current['main']['temp']
    humidity=current['main']['humidity']
    pressure=current['main']['pressure']
    wind_speed=current['wind']['speed']
    description=current['weather'][0]['description']
    
    t.config(text=f"{temp}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure} hPa")
    w.config(text=f"{wind_speed} m/s")
    d.config(text=f"{description}")

    daily_data = []
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)
    
    icons = []
    temps = []
    
    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        img = Image.open(fr"C:\Users\user\Desktop\icon\{icon_code}@2x.png").resize((50,50))
        icons.append(ImageTk.PhotoImage(img))
        temps.append((
    daily_data[i]['main']['temp_max'],
    daily_data[i]['main']['feels_like']
))

    
    day_widget = [
        (firstimage,day1,day1temp),
        (secondimage,day2,day2temp),
        (thirdimage,day3,day3temp),
        (fourthimage,day4,day4temp),
        (fifthimage,day5,day5temp)
    ]
        
    for i,(img_label,day_label,temp_label) in enumerate(day_widget):
        if i >= len(icons):
             break
        img_label.config(image=icons[i])
        img_label.image = icons[i]
        temp_label.config(text=f"Day: {temps[i][0]}\nNight: {temps[i][1]}")
        future_date = datetime.now() + timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))
        
    if temp < 5:
        clothing = "Obucite toplu jaknu, kapu i šal."
    elif temp < 15:
        clothing = "Preporučujemo laganu jaknu ili džemper."
    elif temp < 25:
        clothing = "Majica s dugim ili kratkim rukavima je dovoljna."
    else:
        clothing = "Vrlo toplo - nosite laganu odjeću."
    clothing_label.config(text=f"Preporuka: {clothing}")

    hour = local_time.hour
    if 6 <= hour < 12:
        music = "Predlog muzike: Lagani pop ili jutarnji jazz za dobar početak dana."
    elif 12 <= hour < 18:
        music = "Predlog muzike: Energizujući rock ili dance muzika."
    elif 18 <= hour < 22:
        music = "Predlog muzike: Smireni indie ili akustični zvuci."
    else:
        music = "Predlog muzike: Umirujući ambient ili klasična muzika za opuštanje."
    music_label.config(text=music)

    if temp > 25:
        drink = "Predlog pića: Hladni koktel ili ledeni čaj."
    elif 15 <= temp <= 25:
        drink = "Predlog pića: Sveže ceđeni sok ili limunada."
    elif 5 <= temp < 15:
        drink = "Predlog pića: Topla kafa ili čaj."
    else:
        drink = "Predlog pića: Vruća čokolada ili biljni čaj."
    drink_label.config(text=drink)
    
    desc = description.lower()
    if "clear" in desc:
        playlist_text = "🎵 Sunčana plejlista za dobro raspoloženje"
        playlist_url = "https://www.youtube.com/watch?v=y6Sxv-sUYtM&list=PLWyCiVKEayX_WuoYgy0eopWvDzCnmoAGn"
    elif "cloud" in desc:
        playlist_text = "☁ Plejlista za oblačne dane"
        playlist_url = "https://www.youtube.com/watch?v=ru0K8uYEZWw&list=RDQMNKED_0Rpx4g&start_radio=1"
    elif "rain" in desc or "drizzle" in desc:
        playlist_text = "🌧️ Plejlista za kišne dane"
        playlist_url = "https://www.youtube.com/watch?v=aHPVwb9C-zo&pp=ygUOY2xvdWR5IHBsYWxpc3Q%3D"
    elif "snow" in desc:
        playlist_text = "❄ Zimska chill muzika"
        playlist_url = "https://www.youtube.com/watch?v=RKrErm9D404&pp=ygUOd2ludGVyIHBsYWxpc3Q%3D"
    elif "storm" in desc or "thunder" in desc:
        playlist_text = "⚡ Intenzivna instrumentalna plejlista"
        playlist_url = "https://www.youtube.com/watch?v=pAgnJDJN4VA&list=RDQMHIn4IannryI&start_radio=1"
    else:
        playlist_text = "🎧 Muzika za svaki dan"
        playlist_url = "https://www.youtube.com/watch?v=ktvTqknDobU&list=PLBvlOmA5U9CqIy9lLQrZgyYEYqD6vpMED"

    btn_vijesti.place(x=650, y=225, width=80, height=25)
    playlist_label.config(text=playlist_text)
    playlist_label.bind("<Button-1>", lambda e: open_playlist(playlist_url))

image_icon=PhotoImage(file=r"C:\Users\user\Desktop\Images\logo.png")
root.iconphoto(False,image_icon)

Round_box=PhotoImage(file=r"C:\Users\user\Desktop\Images\Rounded_Rectangle_1.png")
Label(root,image=Round_box,bg="#202731").place(x=30,y=60)
 
label1 = Label(root,text="Temperature",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label1.place(x=50,y=120)

label2 = Label(root,text="Humidity",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label2.place(x=50,y=140)

label3 = Label(root,text="Pressure",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label3.place(x=50,y=160)

label4 = Label(root,text="Wind Speed",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label4.place(x=50,y=180)

label5 = Label(root,text="Description",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label5.place(x=50,y=200)

Search_image=PhotoImage(file=r"C:\Users\user\Desktop\Images\Rounded_Rectangle_3.png")
myimage=Label(root,image=Search_image,bg="#202731")
myimage.place(x=270,y=122)

weat_image=PhotoImage(file=r"C:\Users\user\Desktop\Images\Layer_7.png")
weatherimage=Label(root,image=weat_image,bg="#333c4c")
weatherimage.place(x=290,y=127)

textfield=tk.Entry(root,justify="center",width=15,font=("poppins",25,"bold"),bg="#333c4c",border=0,fg="white")
textfield.place(x=370,y=130)

Search_icon=PhotoImage(file=r"C:\Users\user\Desktop\Images\Layer_6.png")
myimage_icon=Button(root,image=Search_icon,borderwidth=0,cursor="hand2",bg="#333c4c",command=getWeather)
myimage_icon.place(x=640,y=135)

frame=Frame(root,width=900,height=180,bg="#7094d4")
frame.pack(side=BOTTOM)

firstbox=PhotoImage(file=r"C:\Users\user\Desktop\Images\Rounded_Rectangle_2.png")
secondbox=PhotoImage(file=r"C:\Users\user\Desktop\Images\Rounded_Rectangle_2_copy.png")

Label(frame,image=firstbox,bg="#7094d4").place(x=30,y=20)
Label(frame,image=secondbox,bg="#7094d4").place(x=300,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=400,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=500,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=600,y=30)

clock=Label(root,font=("Helvetica",20),bg="#202731",fg="white")
clock.place(x=30,y=20)

timezone=Label(root,font=("Helvetica",18),bg="#202731",fg="white")
timezone.place(x=490,y=20)

long_lat=Label(root,font=("Helvetica",18),bg="#202731",fg="white")
long_lat.place(x=480,y=50)

t=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
t.place(x=150,y=120)

h=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
h.place(x=150,y=140)

p=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
p.place(x=150,y=160)

w=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
w.place(x=150,y=180)

d=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
d.place(x=150,y=200)

clothing_label = Label(root, font=("Helvetica", 10, "italic"), bg="#202731", fg="lightblue", wraplength=350, justify="left")
clothing_label.place(x=30, y=230)

music_label = Label(root, font=("Helvetica", 10, "italic"), bg="#202731", fg="#8be9fd", wraplength=350, justify="left")
music_label.place(x=380, y=190)

drink_label = Label(root, font=("Helvetica", 10, "italic"), bg="#202731", fg="#f0a500", wraplength=350, justify="left")
drink_label.place(x=380, y=225)

playlist_label = Label(root, font=("Helvetica", 10, "underline"), bg="#202731", fg="#81ecec", cursor="hand2", wraplength=350, justify="left")
playlist_label.place(x=380, y=250)

firstframe=Frame(frame,width=230,height=132,bg="#323661")
firstframe.place(x=35,y=25)

firstimage=Label(firstframe,bg="#323661")
firstimage.place(x=1,y=15)

day1=Label(firstframe,font=("Arial 20"),bg="#323661",fg="white")
day1.place(x=100,y=5)

day1temp=Label(firstframe,font=("Arial 15 bold"),bg="#323661",fg="white")
day1temp.place(x=100,y=50)

secondframe=Frame(root,width=70,height=115,bg="#eeefea")
secondframe.place(x=305,y=325)

secondimage=Label(secondframe,bg="#eeefea")
secondimage.place(x=7,y=20)

day2=Label(secondframe,bg="#eeefea",fg="#000")
day2.place(x=10,y=5)

day2temp=Label(secondframe,bg="#eeefea",fg="#000")
day2temp.place(x=2,y=70)

thirdframe=Frame(root,width=70,height=115,bg="#eeefea")
thirdframe.place(x=405,y=325)

thirdimage=Label(thirdframe,bg="#eeefea")
thirdimage.place(x=7,y=20)

day3=Label(thirdframe,bg="#eeefea",fg="#000")
day3.place(x=10,y=5)

day3temp=Label(thirdframe,bg="#eeefea",fg="#000")
day3temp.place(x=2,y=70)

fourthframe=Frame(root,width=70,height=115,bg="#eeefea")
fourthframe.place(x=505,y=325)

fourthimage=Label(fourthframe,bg="#eeefea")
fourthimage.place(x=7,y=20)

day4=Label(fourthframe,bg="#eeefea",fg="#000")
day4.place(x=10,y=5)

day4temp=Label(fourthframe,bg="#eeefea",fg="#000")
day4temp.place(x=2,y=70)

fifthframe=Frame(root,width=70,height=115,bg="#eeefea")
fifthframe.place(x=605,y=325)

fifthimage=Label(fifthframe,bg="#eeefea")
fifthimage.place(x=7,y=20)

day5=Label(fifthframe,bg="#eeefea",fg="#000")
day5.place(x=10,y=5)

day5temp=Label(fifthframe,bg="#eeefea",fg="#000")
day5temp.place(x=2,y=70)

btn_vijesti = Button(root, text="Vijesti", bg="#accbff", fg="#202731", cursor="hand2", font=("Arial", 10, "bold"), command=open_news_window)
btn_vijesti.place_forget()

root.mainloop()
import tkinter as tk 
from tkinter import simpledialog, messagebox 
import mysql.connector as c 
con = c.connect(host='localhost', user='root', passwd='********', database='project') 
cur = con.cursor() 
u = None 
 
def work(): 
    while True: 
        a = simpledialog.askinteger("Menu", "1: View available cars\n2: Book a car\n3: View Bookings\n4: Contact us\n5: Exit\nEnter Choice:") 
        if a == 1: 
            view_cars() 
        elif a == 2: 
            book_car() 
        elif a == 3: 
            view_bookings() 
        elif a == 4: 
            messagebox.showinfo("Contact Us", "Customer care no.: 1532874267\nMail id: carbookz@gmail.com\nReach out to us for any help.") 
        elif a == 5: 
            break 
        else: 
            messagebox.showwarning("Invalid Input", "Invalid Number Request Made.") 
 
def view_cars(): 
    b = simpledialog.askinteger("View Cars", "1: View sedan cars\n2: View SUV cars\nEnter choice:") 
    cars_list = [] 
    if b == 1: 
        cars_list = query_and_fetch("sedan") 
    elif b == 2: 
        cars_list = query_and_fetch("SUV") 
    else: 
        messagebox.showwarning("Invalid Input", "Invalid Number Request Made.") 
    display_cars(cars_list) 
 
def query_and_fetch(car_type=None): 
    if car_type: 
        cur.execute(f"select * from cars where type='{car_type}'") 
    else: 
        cur.execute("select * from cars") 
    return cur.fetchall() 
 
def display_cars(cars_list): 
    cars_details = "" 
    for car in cars_list: 
        car_details = f"Car: {car[0]}\nCost per day: INR {car[6]}\nmileage: {car[1]} {car[2]} {car[3]} {car[4]} {car[5]} seater\n\n" 
        cars_details += car_details 
    cars_window = tk.Toplevel(root) 
    cars_window.title("Available Cars")
    label_cars = tk.Label(cars_window, text=cars_details, font=("Helvetica", 12)) 
    label_cars.pack(pady=10) 
    cars_window.attributes('-topmost', True) 
    cars_window.transient(root) 
    cars_window.grab_set() 
    cars_window.wait_window() 
def book_car(): 
    cur.execute("select * from cars") 
    cars_list = cur.fetchall() 
    req_car = simpledialog.askstring("Book a Car", "Enter the desired car name:") 
    check = 0 
    for car in cars_list: 
        if req_car.title() in car[0]: 
            name = simpledialog.askstring("Book a Car", "Enter name under booking:") 
            pickup = simpledialog.askstring("Book a Car", "Enter pickup date (dd-mm-yyyy):") 
            no = simpledialog.askinteger("Book a Car", "Enter number of days:") 
            cost = car[6] * no 
            global u 
            q = f"insert into bookings values({u}, '{name}', '{car[0]}', '{pickup}', {no}, {cost})" 
            cur.execute(q) 
            con.commit() 
            messagebox.showinfo("Booking Successful", "Booking registered successfully") 
            check = 1 
            break 
    if check == 0: 
        messagebox.showwarning("Car Not Found", "Car not found. Try again.") 
 
def view_bookings(): 
    global u 
    check = 0 
    cur.execute("select * from bookings") 
    bookings_list = cur.fetchall() 
    bookings_details = "" 
    for booking in bookings_list: 
        if booking[0] == u: 
            check = 1 
            booking_details = f"Name: {booking[1]}\nCar: {booking[2]}\nPickup date: {booking[3]}\nNumber of days: {booking[4]}\nTotal cost: {booking[5]}\n\n" 
            bookings_details += booking_details 
    if check == 0: 
        messagebox.showinfo("No Booking", "No booking found.") 
    else: 
        messagebox.showinfo("Booking Details", bookings_details) 
 
def login(): 
    global u 
    t = simpledialog.askinteger("Login", "1: Login using id and password\n2: Login using phone number and password\n3: Sign up a new account\nEnter choice:") 
    cur.execute("select * from login") 
    login_list = cur.fetchall() 
    if t == 1 or t == 2: 
        identifier = "ID" if t == 1 else "Phone Number" 
        identifier_value = simpledialog.askstring("Login", f"Enter your {identifier}:") 
        if identifier_value is not None: 
            password = simpledialog.askstring("Login", "Enter your password:") 
            if password is not None: 
                check = 0 
                for login_info in login_list: 
                    if (t == 1 and login_info[0] == int(identifier_value)) or (t == 2 and login_info[2] == identifier_value): 
                        check = 1 
                        if login_info[1] == password: 
                            messagebox.showinfo("Login Successful", "Password Successfully Matched.") 
                            u = login_info[0] 
                            work() 
                        else: 
                            messagebox.showwarning("Incorrect Password", "Incorrect password.") 
                        break 
                if check == 0: 
                    messagebox.showwarning(f"{identifier} Not Found", f"{identifier} does not exist.") 
    elif t == 3: 
        signup() 
    else: 
        messagebox.showwarning("Invalid Input", "Invalid Number Request Made") 
 
def signup(): 
    cur.execute("select * from login") 
    login_list = cur.fetchall() 
    id_no = login_list[-1][0] + 1 
    mobile_no = simpledialog.askstring("Sign Up", "Enter your mobile number:") 
    password = simpledialog.askstring("Sign Up", "Create a new password:") 
    messagebox.showinfo("Sign Up", f"Your generated id number is: {id_no}") 
    query = f"insert into login values ({id_no}, '{password}', '{mobile_no}')" 
    cur.execute(query) 
    con.commit() 
    messagebox.showinfo("Registration Successful", "Registered Successfully. Please login now.") 
    login() 
 
# Tkinter GUI setup 
root = tk.Tk() 
root.title("Online Car Rental System") 
 
label = tk.Label(root, text="ONLINE CAR RENTAL SYSTEM", font=("Helvetica", 16)) 
label.pack(pady=10) 
 
button_login = tk.Button(root, text="Login to an existing account", command=login) 
button_login.pack(pady=5) 
 
button_signup = tk.Button(root, text="Signup a new account", command=signup) 
button_signup.pack(pady=5) 
 
label_thank_you = tk.Label(root, text="Thank You for visiting us.") 
label_thank_you.pack(pady=10) 
 
root.mainloop()
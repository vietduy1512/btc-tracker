import requests
import tkinter as tk

def get_btc_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    data = response.json()
    price_usd = float(data['bpi']['USD']['rate'].replace(",", ""))
    return price_usd

def update_price():
    current_price = round(get_btc_price())
    if current_price > update_price.previous_price:
        price_label.config(text=f"{current_price} ↑", fg='green')
    elif current_price < update_price.previous_price:
        price_label.config(text=f"{current_price} ↓", fg='red')
    else:
        price_label.config(text=f"{current_price}", fg='white')
    update_price.previous_price = current_price
    price_label.after(35000, update_price)  # Update every 35 seconds (35000 milliseconds)

update_price.previous_price = get_btc_price()

def toggle_visibility():
    if bottom_frame.winfo_ismapped():
        bottom_frame.pack_forget()
        visibility_button.config(text="+")
    else:
        visibility_button.pack_forget()
        bottom_frame.pack(side='bottom', fill='x')
        visibility_button.pack(side='bottom')
        visibility_button.config(text="-")

def toggle_always_on_top():
    app.attributes('-topmost', always_on_top_var.get())

def close_app():
    app.destroy()

def start_move(event):
    app.drag_x = event.x
    app.drag_y = event.y

def stop_move(event):
    app.drag_x = None
    app.drag_y = None

def on_motion(event):
    deltax = event.x - app.drag_x
    deltay = event.y - app.drag_y
    x = app.winfo_x() + deltax
    y = app.winfo_y() + deltay
    app.geometry(f"+{x}+{y}")

app = tk.Tk()
app.title("Bitcoin Price Tracker")
app.configure(bg='black')  # Set background color to black
app.overrideredirect(True)  # Remove title bar

top_frame = tk.Frame(app, bg='black')
top_frame.pack(fill='x')

price_label = tk.Label(top_frame, text=f"{update_price.previous_price}", font=('Arial', 14), fg='white', bg='black')  # Set text color to white and background color to black
price_label.pack(pady=5)

bottom_frame = tk.Frame(app, bg='black')

top_bar = tk.Frame(bottom_frame, bg='gray', height=20, cursor="fleur")
top_bar.pack(fill='x')
top_bar.bind("<ButtonPress-1>", start_move)
top_bar.bind("<ButtonRelease-1>", stop_move)
top_bar.bind("<B1-Motion>", on_motion)

always_on_top_var = tk.BooleanVar(value=False)
always_on_top_checkbox = tk.Checkbutton(bottom_frame, text="Always on Top", variable=always_on_top_var, command=toggle_always_on_top, fg='white', bg='black', selectcolor='black')
always_on_top_checkbox.pack(side='left', padx=5)

close_button = tk.Button(bottom_frame, text="Close", command=close_app, fg='white', bg='black', relief='flat')
close_button.pack(side='left', padx=5)

bottom_frame.pack(side='bottom', fill='x')

visibility_button = tk.Button(app, text="-", command=toggle_visibility, fg='white', bg='black', relief='flat')
visibility_button.pack(side='bottom')

update_price()  # Start updating the price

app.mainloop()

from datetime import datetime, timedelta
import tkinter as tk

PRICE_PER_PACK = 9.00
PACKS_PER_DAY = 0.8
# based on 24-hour clock
WAKE_HOUR = 6
SLEEP_HOUR = 22
# datetime(year, month, day, hour, minute)
LAST_CIG = datetime(2024, 2, 11, 9, 0)

ACTIVE_HOURS = 24 - (24 - SLEEP_HOUR) - WAKE_HOUR
PRICE_PER_HOUR = PRICE_PER_PACK * PACKS_PER_DAY / ACTIVE_HOURS

def calculate_accumulated_balance(current_datetime):
    balance = 0.00
    
    total_seconds = (current_datetime - LAST_CIG).total_seconds()
    total_hours = total_seconds / 3600
    
    for hour in range(int(total_hours)):
        hour_datetime = LAST_CIG + timedelta(hours=hour)
        
        if WAKE_HOUR < hour_datetime.hour < SLEEP_HOUR:
            balance += PRICE_PER_HOUR
    
    if WAKE_HOUR < current_datetime.hour < SLEEP_HOUR:
        partial_hour_seconds = total_seconds % 3600
        balance += (partial_hour_seconds / 3600) * PRICE_PER_HOUR
    
    return balance

def update_balance():
    current_datetime = datetime.now()
    
    balance = calculate_accumulated_balance(current_datetime)
    
    balance_var.set(f" Money Saved: ${balance:.2f} ")
    
    root.after(60000, update_balance)

root = tk.Tk()
root.title(f"Cigarette Cessation Savings Counter - Price Per Hour Awake: ${PRICE_PER_HOUR}")
root.configure(background='black')

balance_var = tk.StringVar()
balance_label = tk.Label(root, textvariable=balance_var, font=('Arial', 48), fg='green', bg='black')
balance_label.pack(pady=20)

update_balance()

root.mainloop()

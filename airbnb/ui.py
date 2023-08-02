from tkinter import ttk
from tkinter import *
from data import Reservations
import subprocess


class Airbnb():
    def __init__(self, reservation_data: Reservations):
        self.reservations = reservation_data

        self.window = Tk()
        self.window.title('Airbnb')
        self.window.config(pady=20, padx=20)

        self.allowance = Label(text=f"Remaining Allowance: £{self.reservations.remaining_allowance}")
        self.allowance.grid(row=0, column=1)

        self.period_reservations = Label(text='', justify=LEFT)
        self.period_reservations.grid(row=3, column=0, columnspan=2)

        self.period_amount = Label(text='', justify=LEFT)
        self.period_amount.grid(row=4, column=0, columnspan=2)

        self.canvas = Canvas(width=500, height=300, bg = 'white')
        self.res_box = self.canvas.create_text(250,150, text='')
        self.canvas.grid(row=1, column=0, columnspan=2)

        self.combo = ttk.Combobox(
            values=['MTD', 'Month', 'YTD', 'Year', 'Month+1', 'Month+2', 'Month+3'],

        )
        self.combo.set(value='Month')
        self.combo.grid(row=2, column=0)

        button = Button(text='Retrieve results', command=self.get_reservations)
        button.grid(row=2, column=1)

        open_directory = Button(text='Open Directory', command=self.open_directory)
        open_directory.grid(row=5, column=1)

        self.window.mainloop()

    def get_reservations(self):
        selection = self.combo.get()
        results = self.reservations.get_reservations(selection)
        self.period_reservations.config(text=f"Period Reservations: ["
                                             f"{results[results.Listing == 'Private room'].count()['Listing']} room / "
                                             f"{results.count()['Listing'] - results[results.Listing == 'Private room'].count()['Listing']} flat]")
        self.period_amount.config(text=f"Period Amount: £{results['Amount'].sum()}")
        self.canvas.itemconfig(tagOrId = self.res_box, text = results)
        print(results)

    def open_directory(self):
        subprocess.Popen(r'explorer /select,"C:\Users\Zacharias.Detorakis\Desktop\Personal\PyCharmProjects\100-days-of-code\airbnb\output_data\"')
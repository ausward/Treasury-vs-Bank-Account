from tkinter import *
import advise
import webbrowser
global t_bill_data

t_bill_data = []


def close (child:Tk, next, dict = None):
    child.destroy()
    if next == 'questions()':
        questions()
    elif next == 'guiTwo':
        gUITwo(dict)


def openSite():
    webbrowser.open('https://invest.ameritrade.com/grid/p/site#r=jPage/https://valubond.ameritrade.com/Dotnet/PrivateOffers/T-Auction.aspx?c_name=invest_VENDOR'
                    ,2, True)


def disclaim() -> None:
    x = 200
    frame1 = Tk()
    frame1.title('Disclaimer')
    frame1.geometry('1200x500')
    Label(master=frame1, text=advise.disclaimer(), font="times 15", justify='left', background='black', foreground='red',padx=100 ,pady=100).pack()
    Button(frame1, text='Understood', command=lambda: close(frame1, 'questions()'),background='black' , width=300,font='times 25',foreground="blue").pack()
    frame1.mainloop()


def questions():
    x=200
    root = Tk()
    root.geometry('700x600')
    amount = StringVar()
    apy = StringVar()

    root.title("advise question")

    Label(root, text=advise.disclaimer(), justify="left", takefocus=3).place(x=0, y=0)
    Label(root, text="Invest Amount  **Must be a multiple of 1,000").place(x=x, y=225)
    Entry(root, textvariable=amount, highlightthickness=2, width=50).place(x=x, y=245)
    Label(root, text="Account APY").place(x=x, y=275)
    Entry(root, textvariable=apy, width=50).place(x=x+2, y=295)
    try:
        Button(text="Submit", width=10, font="times 15", command=lambda : close(root, 'guiTwo', {'apy': float(apy.get()), 'amount': float(amount.get())}
                                             )).place(x=x + 75, y=325)
    except Exception:
        if apy.get() == "" and amount.get() == "":
            apy.set('.05')
            amount.set('1_000')
    root.mainloop()
    return {'apy': float(apy.get()), 'amount': float(amount.get())}


def gUITwo(dict: dict):
    amount = dict['amount']
    apy = dict['apy']
    t_bill_data = advise.t_bill(amount / 100)
    t_bill_print = advise.t_bill_print(t_bill_data)
    root = Tk()
    root.title("data")
    root.geometry("1700x500")
    Label(root, text="Based on Historical Data from the past 5 days Treasury auctions.", font='times',
          justify='center').place(x=10, y=50)

    Message(root, text=t_bill_print, justify='center', width=9000 *2, font="times", relief="raised").place(x=5, y=100)
    Message(root, text=str(advise.fullRecurAndPrint(apy, amount, t_bill_data)), font='times', justify='center',
            width=9000*2, relief="sunken").place(x=5, y=150)

    Button(root, text="Open TD Ameritrade", font="Times 15", command=lambda: openSite(), width=50, foreground="blue", background='purple').place(x=70, y=300)
    root.mainloop()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


def main():
    disclaim()


if __name__ == '__main__':
    main()
    print(t_bill_data)

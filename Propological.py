import tkinter as tk
from io import StringIO
import sys
from pathlib import Path
from pynput.keyboard import Key, Controller
from tkinter import filedialog, Canvas, Button, PhotoImage
from tkinter.filedialog import askopenfilename
keyboard= Controller()
# Main Program
def isWellFormed(P): #Function for checking if the proposition itself is of the correct format
    bracketLevel = 0
    for c in P:
        if c == "(":
            bracketLevel += 1
        if c == ")":
            if bracketLevel == 0:
                return False
            bracketLevel -= 1
    return bracketLevel == 0

def parseNegation(P, truthValues):
    return not parseProposition(P, truthValues)

def parseConjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) and parseProposition(Q, truthValues)

def parseDisjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) or parseProposition(Q, truthValues)

def parseConditional(P, Q, truthValues):
    return (not parseProposition(P, truthValues)) or parseProposition(Q, truthValues) # Used tautology to implement the conditional operator

def parseBiconditional(P, Q, truthValues):
    return parseProposition(P, truthValues) == parseProposition(Q, truthValues)

def parseProposition(P , truthValues):
    P = P.replace(" ", "")

    if not isWellFormed(P):
        return "Error"

    while P[0] == "(" and P[-1] == ")" and isWellFormed(P[1:len(P) - 1]):
        P = P[1:len(P) - 1]

    if len(P) == 1:
        return truthValues[P]

    bracketLevel = 0 # Bracketlevel used for checking if it should be the first proposition to be parsed
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "→" and bracketLevel == 0:
            return parseConditional(P[0:i], P[i + 1:], truthValues)
        if P[i] == "↔" and bracketLevel == 0:
            return parseBiconditional(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∨" and bracketLevel == 0:
            return parseDisjunction(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∧" and bracketLevel == 0:
            return parseConjunction(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "¬" and bracketLevel == 0:
            return parseNegation(P[i + 1:], truthValues)

def writeTruthTable(P):
    truthValues = {} # Dictionary for the truth values
    for i in range(len(P)):
        if P[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": # Extracts the propositions from the Input
            truthValues[P[i]] = True

    output = StringIO()
    sys.stdout = output

    for statement in list(truthValues.keys()):
        print(statement, end=" | ") # Prints the header of the table
    print(P)
    for truthValue in list(truthValues.values()):
        print("T" if truthValue else "F", end=" | ") # Prints the truth value of each proposition
    print("T" if parseProposition(P, truthValues) else "F")

    j = len(truthValues.values()) - 1
    while True in truthValues.values():
        variable = list(truthValues.keys())[j]
        truthValues[variable] = not truthValues[variable]

        if not truthValues[variable]:
            for truthValue in list(truthValues.values()):
                print("T" if truthValue else "F", end=" | ") # Prints the truth value of the compound proposition
            print("T" if parseProposition(P, truthValues) else "F")
            j = len(truthValues.values()) - 1
        else:
            j -= 1

    sys.stdout = sys.__stdout__
    return output.getvalue() #returned the printed table into a single variable for the GUI usage
#PATH for the assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
#Button Binds
def Conjunction(): 
    keyboard.press('∨') #used controller function to emulate button press
    keyboard.release('∨')
def Conjuction():
    keyboard.press('∨')
    keyboard.release('∨')
def Disjunction():
    keyboard.press('∧')
    keyboard.release('∧')
def Conditional():
    keyboard.press('→')
    keyboard.release('→')
def Biconditional():
    keyboard.press('↔')
    keyboard.release('↔')
def Negation():
    keyboard.press('¬')
    keyboard.release('¬')
def OpenP():
    keyboard.press('(')
    keyboard.release('(')
def CloseP():
    keyboard.press(')')
    keyboard.release(')')
def LetterP():
    keyboard.press('P')
    keyboard.release('P')
def LetterQ():
    keyboard.press('Q')
    keyboard.release('Q')
def LetterR():
    keyboard.press('R')
    keyboard.release('R')
def LetterS():
    keyboard.press('S')
    keyboard.release('S')
def LetterT():
    keyboard.press('T')
    keyboard.release('T')
def LetterU():
    keyboard.press('U')
    keyboard.release('U')
def LetterV():
    keyboard.press('V')
    keyboard.release('V')
def Backspace():
    keyboard.press(Key.backspace)
    keyboard.release(Key.backspace)
#Console Output
class ConsoleGUI:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(side='top')
        #icon for the app
        photo=PhotoImage(  
            file=relative_to_assets("image_1.png")
        )
        master.iconphoto(False,photo)

        canvas = Canvas(
            self.master,
            bg = "#FFFFFF",
            height = 450,
            width = 325,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        #Object for the input of the user
        self.command_entry = PhotoImage(
            file=relative_to_assets("entry_2.png")
        )
        self.command_entry_bg = canvas.create_image(
            162.0,
            197.5,
            image=self.command_entry
        )
        self.command_entry = tk.Entry(
            bd=0,
            bg="#F2F2F2",
            fg="#000716",
            highlightthickness=0
        )
        self.command_entry.place(
            x=14.0,
            y=174.0,
            width=298.0,
            height=45.0
        )
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.focus_set()
        #Object for the output of the program
        self.console_output = tk.Text(
            bd=0,
            bg="#F2F2F2",
            fg="#000716",
            highlightthickness=0
        )
        self.console_output.place(
            x=14,
            y=33,
            width=298.0,
            height=134.0
        )
 #Function for printing the table
    def execute_command(self):
        command = self.command_entry.get()
        output = writeTruthTable(command)
        self.console_output.config(state='normal')
        self.console_output.insert('end', output)
        self.console_output.config(state='disabled')
        self.console_output.see('end')
#Function for saving the displayed table
    def save_console_text(self):
        command = self.command_entry.get()
        self.command_entry.delete(0, 'end')
        output = writeTruthTable(command)
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w",encoding='utf-8') as file:
                file.write(output)
#Command for clearing the whole output of the app
    def clear_console(self):
        self.console_output.config(state='normal')
        self.console_output.delete('1.0', 'end')
        self.console_output.config(state='disabled')
        self.command_entry.delete(0, 'end')
#Function for loading a save file
    def load_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
#Function for displaying the loaded file
    def load_file_handler(self):
        filename = askopenfilename()
        if filename:
            text = self.load_file(filename)
            self.console_output.config(state='normal')
            self.console_output.delete('1.0', 'end')
            self.console_output.insert('end', text)
            self.console_output.config(state='disabled')

    def run(self):
        self.master.mainloop()
#Class for the main frame
class PropologicalGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Propological")
        self.master.geometry("325x450")
        self.master.configure(bg = "#FFFFFF")
        self.master.resizable(False, False)

        canvas = Canvas(
            self.master,
        bg = "#FFFFFF",
        height = 450,
        width = 325,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        self.console = ConsoleGUI(self.master)
        #Button '∨'
        global disj_button_image
        disj_button_image = PhotoImage(
            file=relative_to_assets("button_19.png"))
        disj_button = Button(
            image=disj_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=Disjunction,
            relief="flat"
        )
        disj_button.place(
            x=14.420135498046875,
            y=227.5557861328125,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button '∧'
        global con_button_image
        con_button_image = PhotoImage(
            file=relative_to_assets("button_18.png"))
        con_button = Button(
            image=con_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=Conjunction,
            relief="flat"
        )
        con_button.place(
            x=93.25199127197266,
            y=227.24703979492188,
            width=60.01887130737305,
            height=45.471832275390625
        )

        #Button '→'
        global cd_button_image
        cd_button_image = PhotoImage(
            file=relative_to_assets("button_17.png"))
        cd_button = Button(
            image=cd_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=Conditional,
            relief="flat"
        )
        cd_button.place(
            x=172.0378875732422,
            y=227.5557861328125,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button 'P'
        global p_button_image
        p_button_image = PhotoImage(
            file=relative_to_assets("button_14.png"))
        p_button = Button(
            image=p_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterP,
            relief="flat"
        )
        p_button.place(
            x=14.420135498046875,
            y=282.8798828125,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button '('
        global op_button_image
        op_button_image = PhotoImage(
            file=relative_to_assets("button_13.png"))
        op_button = Button(
            image=op_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=OpenP,
            relief="flat"
        )
        op_button.place(
            x=93.0,
            y=283.0,
            width=60.01887130737305,
            height=45.47186279296875
        )

        #Button ')'
        global cp_button_image
        cp_button_image = PhotoImage(
            file=relative_to_assets("button_12.png"))
        cp_button = Button(
            image=cp_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=CloseP,
            relief="flat"
        )
        cp_button.place(
            x=172.0,
            y=283.0,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button '↔'
        global bicon_button_image
        bicon_button_image = PhotoImage(
            file=relative_to_assets("button_15.png"))
        bicon_button = Button(
            image=bicon_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=Biconditional,
            relief="flat"
        )
        bicon_button.place(
            x=251.0,
            y=283.0,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button 'Q'
        global q_button_image
        q_button_image = PhotoImage(
            file=relative_to_assets("button_11.png"))
        q_button = Button(
            image=q_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterQ,
            relief="flat"
        )
        q_button.place(
            x=14.420135498046875,
            y=338.2039794921875,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button 'R'
        global r_button_image
        r_button_image = PhotoImage(
            file=relative_to_assets("button_10.png"))
        r_button = Button(
            image=r_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterR,
            relief="flat"
        )
        r_button.place(
            x=93.22911071777344,
            y=338.2039794921875,
            width=60.01887130737305,
            height=45.47186279296875
        )

        #Button 'S'
        global s_button_image
        s_button_image = PhotoImage(
            file=relative_to_assets("button_6.png"))
        s_button = Button(
            image=s_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterS,
            relief="flat"
        )
        s_button.place(
            x=172.0378875732422,
            y=338.2039794921875,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button '¬'
        global neg_button_image
        neg_button_image = PhotoImage(
            file=relative_to_assets("button_5.png"))
        neg_button = Button(
            image=neg_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=Negation,
            relief="flat"
        )
        neg_button.place(
            x=250.84646606445312,
            y=338.2039794921875,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button 'T'
        global t_button_image
        t_button_image = PhotoImage(
            file=relative_to_assets("button_4.png"))
        t_button = Button(
            image=t_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterT,
            relief="flat"
        )
        t_button.place(
            x=14.420135498046875,
            y=393.52813720703125,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button 'Backspace'
        global bs_button_image 
        bs_button_image = PhotoImage(
            file=relative_to_assets("button_16.png"))
        bs_button = Button(
            image=bs_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=Backspace,
            relief="flat"
        )
        bs_button.place(
            x=251.0,
            y=228.0,
            width=60.0,
            height=45.47186279296875
        )

        #Button 'U'
        global u_button_image
        u_button_image = PhotoImage(
            file=relative_to_assets("button_3.png"))
        u_button = Button(
            image=u_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterU,
            relief="flat"
        )
        u_button.place(
            x=93.22911071777344,
            y=393.52813720703125,
            width=60.01887130737305,
            height=45.47186279296875
        )

        #Button 'V'
        global v_button_image
        v_button_image = PhotoImage(
            file=relative_to_assets("button_2.png"))
        v_button = Button(
            image=v_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=LetterV,
            relief="flat"
        )
        v_button.place(
            x=172.0378875732422,
            y=393.52813720703125,
            width=60.01887512207031,
            height=45.47186279296875
        ) 

        #Button '='
        global equal_image 
        equal_image = PhotoImage(
            file=relative_to_assets("button_1.png"))
        equal_button = Button(
            image=equal_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.console.execute_command,
            relief="flat"
        )
        equal_button.place(
            x=250.84646606445312,
            y=393.52813720703125,
            width=60.01887512207031,
            height=45.47186279296875
        )

        #Button 'Clear'
        global clr_button_image
        clr_button_image = PhotoImage(
            file=relative_to_assets("button_9.png"))
        clr_button = Button(
            image=clr_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.console.clear_console,
            relief="flat"
        )
        clr_button.place(
            x=258.0,
            y=7.0,
            width=54.0,
            height=21.0
        )

        #Button 'Save'
        global save_button_image
        save_button_image = PhotoImage(
            file=relative_to_assets("button_8.png"))
        save_button = Button(
            image=save_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.console.save_console_text,
            relief="flat"
        )
        save_button.place(
            x=144.0,
            y=7.0,
            width=54.0,
            height=21.0
        )

        #Button 'Load'
        global load_button_image
        load_button_image = PhotoImage(
            file=relative_to_assets("button_7.png"))
        load_button = Button(
            image=load_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.console.load_file_handler,
            relief="flat"
        )
        load_button.place(
            x=201.0,
            y=7.0,
            width=54.0,
            height=21.0
        )
        global image_image_1
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            19.0,
            19.0,
            image=image_image_1
        )
    
if __name__ == '__main__':
    
    root = tk.Tk()
    app = PropologicalGUI(root)
    app.console.run()
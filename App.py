import customtkinter
import AESencryption
import OwnAlgo, AESencryption
from pathlib import Path


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project CMPG215")
        self.geometry(f"{365}x{350}")

        self.grid_rowconfigure(3, pad=20, weight=3)
        self.grid_rowconfigure((0,1,2,4,5), weight=2)

        # add widgets to app
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter file location")
        self.entry.grid(row=0, column=0, columnspan=2, padx=10, ipady=10, sticky="ew")

        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Enter password")
        self.entry2.grid(row=1, column=0, columnspan=2, padx=10, ipady=10, sticky="ew")

        self.rButtonVar = customtkinter.IntVar(value=0)

        self.radiobutton_1 = customtkinter.CTkRadioButton(self, radiobutton_width=30, radiobutton_height=30, text="AES", variable=self.rButtonVar, value=1)
        self.radiobutton_1.grid(row=2, column=0, padx=20, pady=20)

        self.radiobutton_2 = customtkinter.CTkRadioButton(self, radiobutton_width=30, radiobutton_height=30, text="OwnAlgo", variable=self.rButtonVar, value=2)
        self.radiobutton_2.grid(row=2, column=1, padx=20, pady=20)

        self.button1 = customtkinter.CTkButton(self, text='Encrypt', command=self.button_encrypt)
        self.button1.grid(row=3, column=0, padx=20)

        self.button2 = customtkinter.CTkButton(self, text='Decrypt', command=self.button_decrypt)
        self.button2.grid(row=3, column=1, padx=20)

        self.label_1 = customtkinter.CTkLabel(self, text="")
        self.label_1.grid(row=5, column=0, columnspan=2)


    # add methods to app
    def labelChange(self, value: str):
        self.label_1.destroy()
        self.label_1 = customtkinter.CTkLabel(self, text=value)
        self.label_1.grid(row=5, column=0, columnspan=2, sticky="ew")

    def button_encrypt(self):
        path = self.entry.get()
        pw = self.entry2.get()
        if path == "":
            self.labelChange("Please enter file location")
        elif not Path(path).is_file():
            self.labelChange("File does not exist")
        elif pw == "":
            self.labelChange("Please enter password")
        elif self.rButtonVar.get() == 0:
            self.labelChange("Please choose method")
        elif self.rButtonVar.get() == 1:
            AESencryption.Encryption.encrypt(self, path, pw)
            self.labelChange("Encryption with AES successful")
        else:
            OwnAlgo.Encryption.encrypt(self,path, pw)
            self.labelChange("Encryption successful. File removed")
    
    def button_decrypt(self):
        path = self.entry.get()
        pw = self.entry2.get() 
        if path == "":
            self.labelChange("Please enter file location")
        elif not Path(path).is_file():
            self.labelChange("File does not exist")
        elif pw == "":
            self.labelChange("Please enter password")
        elif self.rButtonVar.get() == 0:
            self.labelChange("Please choose method")
        elif self.rButtonVar.get() == 1:
            AESencryption.Encryption.decrypt(self, path, pw)
        else:
            OwnAlgo.Encryption.decrypt(self, path, pw)

    
if __name__ == "__main__":
    app = App()
    app.mainloop()

import json
from tkinter.ttk import Treeview

from lxml import html
import os
import urllib.request
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as tm

import struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


global opener
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor
)

def load_file():
    filename = askopenfilename()
    print(filename)


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class OpenPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.encrypt_btn = Button(self, text="Encrypt File", command=self._encrypt_btn_clicked)

        self.download_btn = Button(self, text="Download Report Files", command=self._download_btn_clicked)
        self.encrypt_btn.grid(columnspan=2)
        self.download_btn.grid(columnspan=2)
        self.pack()

    def _encrypt_btn_clicked(self):
        encrypt_frame.lift()

    def _download_btn_clicked(self):
        login_frame.lift()


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        global remote_url, local_url, base_url
        remote_url = 'http://calm-tundra-99675.herokuapp.com/'
        local_url = 'http://localhost:8000'
        base_url = remote_url

        Page.__init__(self, *args, **kwargs)
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)
        self.pack()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        login_form = opener.open(base_url + '/myapplication/login/').read()
        csrf_token = html.fromstring(login_form).xpath(
            '//input[@name="csrfmiddlewaretoken"]/@value'
        )[0]

        values = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token,
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        login_page = opener.open(base_url + '/myapplication/fdalogin/', data)
        list = json.loads(opener.open(base_url + '/myapplication/fdalistreports/').read().decode("utf-8"))
        if not list['success']:
            tm.showerror("Login Unsuccessful", "Something went wrong logging in, please try again")
        else:
            reports_frame.lift()
            reports_frame.load_data()


class EncryptPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.file_str = StringVar()
        self.file_str.set("No File Selected")
        self.choose_file_btn = Button(self, text='Choose File To Encrypt', command=self.load_file)
        self.choose_file_btn.grid(row=0, sticky=E)
        self.label_file = Label(self, textvariable=self.file_str)
        self.label_file.grid(row=0, column=1)

        self.label_pass = Label(self, text="Enter password for encryption")
        self.entry_pass = Entry(self, show="*")
        self.label_pass.grid(row=1, sticky=E)
        self.entry_pass.grid(row=1, column=1)
        self.encrypt_btn = Button(self, text="Encrypt File", command=self._encrypt_btn_clicked)
        self.encrypt_btn.grid(columnspan=2)
        self.pack()

    def _encrypt_btn_clicked(self):
        chunksize = 16 * 1024
        path = self.file_str.get()
        password = self.entry_pass.get()
        f = open(path, 'rb')
        key = SHA256.new(password.encode('utf-8')).hexdigest()[:16]
        iv = os.urandom(16)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(path)
        with open(path, 'rb') as infile:
            with open(path + '.enc', 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += (' ' * (16 - len(chunk) % 16)).encode('ascii')
                    outfile.write(encryptor.encrypt(chunk))
                tm.showinfo("Success", "Encrypted file saved as: \n" + path + '.enc')
                open_frame.lift()

    def load_file(self):
        filename = askopenfilename()
        self.file_str.set(filename)


class ReportsPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.tree = Treeview(self)
        self.tree["columns"] = ("desc", "author", "date", "encrypted")
        self.tree.column("desc", width=100 )
        self.tree.column("author", width=100)
        self.tree.column("date", width=100 )
        self.tree.column("encrypted", width=100)
        self.tree.heading("desc", text="Description")
        self.tree.heading("author", text="Author")
        self.tree.heading("date", text="Date")
        self.tree.heading("encrypted", text="Encrypted")
        self.tree.pack()
        self.pack()

    def load_data(self):
        list = json.loads(opener.open(base_url + '/myapplication/fdalistreports/').read().decode("utf-8"))
        global data
        data = list['reports']
        for num in data['num']:
            desc = data['Description'][num - 1]
            author = data['Author'][num - 1]
            date = data['Date'][num - 1]
            encrypted = data['Encrypted'][num - 1]
            self.tree.insert("", num - 1, text=str(num), values=(desc, author, date, encrypted))
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, event):
        item = self.tree.selection()[0]
        view_frame.lift()
        view_frame.load_data(data, self.tree.item(item,"text"))


class ViewPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.label_desc = Label(self, text="Description:", font="bold")
        self.label_author = Label(self, text="Author:", font="bold")
        self.label_date = Label(self, text="Date:", font="bold")
        self.label_content = Label(self, text="Content:", font="bold")

        self.label_desc.grid(row=0, sticky=E)
        self.label_author.grid(row=1, sticky=E)
        self.label_date.grid(row=2, sticky=E)
        self.label_content.grid(row=3, sticky=E)

        self.report_desc = StringVar()
        self.report_author = StringVar()
        self.report_date = StringVar()
        self.report_content = StringVar()

        self.val_desc = Label(self, textvariable=self.report_desc)
        self.val_author = Label(self, textvariable=self.report_author)
        self.val_date = Label(self, textvariable=self.report_date)
        self.val_content = Label(self, textvariable=self.report_content)

        self.val_desc.grid(row=0, column=2)
        self.val_author.grid(row=1, column=2)
        self.val_date.grid(row=2, column=2)
        self.val_content.grid(row=3, column=2)

        self.pack()

    def load_data(self, data, report_num):
        report_response = json.loads(opener.open(base_url + '/myapplication/fdagetreport?reportID=' + str(data['ID'][int(report_num)-1])).read().decode("utf-8"))
        report = report_response['report']
        print("\n============== REPORT ==============\n")
        self.report_desc.set(report['Description'])
        self.report_author.set(report['Author'])
        self.report_date.set(report['Date'])
        self.report_content.set(report['Content'])
        files_present = False
        if 'files' in report_response:
            files_present = True
            print("FILES:")
            i = 0
            for file in report_response['files']:
                i+=1
                print("\t" + str(i) + ": " + file['name'][2:])
        else:
            print("FILES: NONE")


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        global open_frame
        global login_frame
        global encrypt_frame
        global reports_frame
        global view_frame
        open_frame = OpenPage(self)
        login_frame = LoginPage(self)
        encrypt_frame = EncryptPage(self)
        reports_frame = ReportsPage(self)
        view_frame = ViewPage(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        open_frame.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        login_frame.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        encrypt_frame.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        reports_frame.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        view_frame.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        open_frame.show()

if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x400")
    root.title('SafeCollab File Download Application')
    root.mainloop()

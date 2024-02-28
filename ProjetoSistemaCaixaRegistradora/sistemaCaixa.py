import customtkinter as ctk
import tktabl as tkt
from PIL import Image,ImageTk
import mysql.connector as mysql
from tkinter import *
from tkinter import ttk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()

width= root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry("%dx%d" % (width, height))

def tela_login():

    def login():
        usuario = entry1.get()
        senha = entry2.get()

        if usuario == "" and senha == "":
            trocar_tela_primaria(tela_opcoes)

        else:
            label = ctk.CTkLabel(master=frame_login, text="Senha Incorreta")
            label.grid(column=0, row=4, pady=12, padx=10)

    frame_login = ctk.CTkFrame(master=main_frame)
    frame_login.place(relx = 0.5, rely = 0.5, anchor =ctk.CENTER)

    label= ctk.CTkLabel(master=frame_login, text="Login System")
    label.grid(column=0, row=0, pady=12, padx=10)

    entry1 = ctk.CTkEntry(master=frame_login, placeholder_text="Username")
    entry1.grid(column=0, row=1, pady=12, padx=10)

    entry2 = ctk.CTkEntry(master=frame_login, placeholder_text="Password", show="*")
    entry2.grid(column=0, row=2, pady=12, padx=10)

    button = ctk.CTkButton(master=frame_login, text="Login", command=login)
    button.grid(column=0, row=3, pady=12, padx=10)

def tela_opcoes():
    frame_botoes = ctk.CTkFrame(main_frame, bg_color='#c3c3c3', border_width=2,
                                border_color='gray', corner_radius=0)
    frame_botoes.pack(side=LEFT, fill=Y)
    frame_botoes.configure(width=100)

    frame_primario = ctk.CTkFrame(main_frame, border_width=2, border_color='blue', corner_radius=0)
    frame_primario.pack(fill='both', expand=True)

    botao_tela_vendas = ctk.CTkButton(master=frame_botoes, text="Tela de Vendas")
    botao_tela_vendas.grid(pady=15, padx=10, column=0, row=2)

    botao_estoque = ctk.CTkButton(master=frame_botoes, text="Tela de Estoque", command=lambda: trocar_tela_secundaria(tela_estoque))
    botao_estoque.grid(pady=15, padx=10, column=0, row=3)

    def delete_pages():
        for frame in frame_primario.winfo_children():
            frame.destroy()

    def trocar_tela_secundaria(page):
        delete_pages()
        page(frame_primario)

def tela_estoque(frame1):
    conn = mysql.connect(database="dbEstoque",
                        host="localhost",
                        user="root",
                        password="RR2210",
                        port="3306")

    sql = 'SELECT * FROM estoque'

    cursor = conn.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()

    style = ttk.Style()

    style.theme_use("default")

    style.configure("Treeview",
                    background="#2a2d2e",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#343638",
                    bordercolor="#343638",
                    borderwidth=0)
    style.map('Treeview', background=[('selected', '#22559b')])

    style.configure("Treeview.Heading",
                    background="#565b5e",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading",
            background=[('active', '#3484F0')])

    frame = ctk.CTkFrame(master=frame1)
    frame.place(relx = 0.5, rely = 0.5,anchor =ctk.CENTER, relwidth= 0.9, relheight= 0.9)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    tv=ttk.Treeview(frame,columns=('id','nome','preço'), show='headings',yscrollcommand=scrollbar.set)
    scrollbar.config(command=tv.yview)
    tv.pack(fill="both", expand=True, anchor =ctk.CENTER)

    tv.column('id', minwidth=0, width=50)
    tv.column('nome', minwidth=0, width=200)
    tv.column('preço', minwidth=0, width=50)

    tv.heading('id', text="ID")
    tv.heading('nome', text="Nome")
    tv.heading('preço', text="Preço")

    for (i,n,q,pc,pv) in rs:
        tv.insert("","end", values=(i, n, ("R$"+str(f"{pv:.2f}"))))

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()   

def trocar_tela_primaria(page):
    delete_pages()
    page()

main_frame = ctk.CTkFrame(root)
main_frame.pack(padx=(5,5), pady=(5,5), fill="both", expand=True, anchor =ctk.CENTER)

tela_login()
root.mainloop()
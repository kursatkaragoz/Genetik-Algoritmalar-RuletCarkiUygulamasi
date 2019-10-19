#-------------------------------------------------------------------------------
# Name:        GenetikAlgoritma
# Purpose:
#
# Author:      Kürşad
#
# Created:     25.03.2019
# Copyright:   (c) Kürşad 2019
# Licence:     <10400336210>
#-------------------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
import numpy as np
import random
import math
import fpdf
import unicodedata
from tkinter import filedialog
import datetime
import time
class Algoritma():

    global firstclick
    firstclick=True

    def aralik2_event(self,sv,event=None):
        self.firstclick=False
        self.event = event

        if(len(self.sv.get()) >0 ):
            self.k.configure(state="normal")
        else:
            self.k.configure(state="readonly")

    def __init__(self):



        pencere = Tk()
        self.pencere = pencere
        pencere.title("Genetik Algoritmalar Rulet Çarkı Problemleri Uygulaması")
        pencere.geometry("900x360+250+50")
        canvas = Canvas(pencere,width=900,height=360)
        myimage = PhotoImage(file = "arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)
        pencere.resizable(0,0)
        self.scrollbar2 = Scrollbar(self.pencere)
        self.listbox2 = Listbox(canvas,width="80",height="19",bg="white",fg="black",font=('consolas',10),yscrollcommand = self.scrollbar2.set)
        self.scrollbar2.pack(side=LEFT, fill=Y)
        self.scrollbar2.config(command=self.listbox2.yview)
        self.listbox2.place(x=20, y=30)

        self.jenerasyonLabel = Label(canvas,text="Jenerasyon Sayısı : ",width="18",anchor="w")
        self.jenerasyonLabel.place(x=600,y=30)
        self.jenerasyonsayisi = Entry(canvas,width="12")
        self.jenerasyonsayisi.place(x=760,y=30)

        self.aralikLabel1 = Label(canvas,text="Aralık [0,maximum] : ",width="17",anchor="w")
        self.aralikLabel1.place(x=600,y=60)
        self.aralik1 =Entry(canvas,width="6")
        self.aralik1.place(x=760,y=60)

        self.sv = StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv:self.aralik2_event(self.sv))
        self.aralik2 =Entry(canvas,width="6",textvariable=self.sv)
        self.aralik2.place(x=795,y=60)
        self.aralik2.bind('<Button-1>',self.aralik2_event)

        self.pop_sizeLabel=Label(canvas,text="Birey Sayisi(pop_size) :",width="18",anchor="w")
        self.pop_sizeLabel.place(x=600,y=90)
        self.pop_size=Entry(canvas,width="12")
        self.pop_size.place(x=760,y=90)

        self.mLabel = Label(canvas,text="Gen Sayisi(m) :",width="18",anchor="w")
        self.mLabel.place(x=600,y=120)
        self.m1=Entry(canvas,width="6",state="readonly")
        self.m1.place(x=760,y=120)
        self.m1.insert(END,10)
        self.m2=Entry(canvas,width="6",state="readonly")
        self.m2.place(x=795,y=120)


        self.klabel=Label(canvas,text="Basamak Hassasiyeti(k):",width="18",anchor="w")
        self.klabel.place(x=600,y=150)
        self.k=Entry(canvas,width="12")
        self.k.place(x=760,y=150)
        self.k.insert("end","0")   #2 Yİ 0 YAP
        self.k.configure(state="readonly")

        self.pcLabel=Label(canvas,text="Çaprazlama ihtimali(Pc) :",width="18",anchor="w")
        self.pcLabel.place(x=600,y=180)
        self.pc=Entry(canvas,width="12")
        self.pc.place(x=760,y=180)
        self.pc.insert(END,0.9)

        self.pmLabel=Label(canvas,text="Mutasyon İhtimali(Pm) :",width="18",anchor="w")
        self.pmLabel.place(x=600,y=210)
        self.pm=Entry(canvas,width="12")
        self.pm.place(x=760,y=210)
        self.pm.insert(END,0.02)

        self.parametre=Button(canvas,text="Parametre ve Problem Belirle",width="32",command=self.parametre_belirle)
        self.parametre.place(x=600,y=240)

        self.basla=Button(canvas,text="Çözüme Başla",width="32",command=self.basla)
        self.basla.place(x=600,y=270)

        self.pdf=Button(canvas,text="Sonuçları Pdf'e Kaydet",width="32",command=self.topdf)
        self.pdf.place(x=600,y=300)

        canvas.pack()
        pencere.mainloop()

    def topdf(self):
    #try:
        b=0
        index=0
        if(self.pdf_yazilacak is not None):
            f = filedialog.asksaveasfilename(initialdir="/", title="Select file", defaultextension=".pdf",filetypes=[('pdf file', '*.pdf')])
            tim = datetime.datetime.now()
            pdf = fpdf.FPDF(format='letter')
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(350, 5, txt=str(tim), ln=1, align="C")
            pdf.cell(200, 10, txt="Genetik Algoritma Fmax - Xmax (Ymax) Sonuç Raporu", ln=1, align="C")


            pdf.ln()
            i=1
            for b in range(0,len(self.pdf_yazilacak)):
                if("fmax" in self.pdf_yazilacak[b]):
                    pdf.cell(200, 10, txt="---------------------{} SON--------------------".format(i), ln=1, align="L")
                    i +=1
                sonuc = "{}".format(self.pdf_yazilacak[b])
                sonuclar = str(unicodedata.normalize('NFKD',sonuc).encode('ascii', 'ignore'))
                sonuclar = sonuclar[2:len(sonuclar)-1]
                pdf.write(5,sonuclar)
                pdf.ln()
            pdf.cell(200, 10, txt="---------------------{}--------------------".format(i), ln=1, align="L")
            pdf.output(f)
        else:
            return 0
    #except:
        #b=0


    def binaryToDecimal(self,binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return decimal

    def uygunlukFonksiyonu_kare(self,dizi=[]):
        self.listbox2.insert(END,"")
        self.listbox2.insert("end","Her Bir Kromozom için uygunluk fonksiyonu y=x^2")
        self.listbox2.itemconfig(END,bg="red",fg="white")
        self.dizi = []
        self.dizi = dizi
        for x in range (0,self.popsize):
            fonksiyon=""
            self.dizi[x] = int(self.dizi[x])
            self.dizi[x] = self.dizi[x] * self.dizi[x]

            fonksiyon = "v{} = {} ==> {}".format(x+1,self.populasyon1binary[x],self.dizi[x])
            self.listbox2.insert(END,fonksiyon)

    def uygunlukFonksiyonu_toplam(self,dizix=[],diziy=[]):
        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"Her Bir Kromozom için Uygunluk Fonksiyonu : F(x,y) = x+y")
        self.listbox2.itemconfig(END,bg="green",fg="white")
        self.dizix=[]
        self.diziy=[]
        self.dizix = dizix
        self.diziy=diziy
        self.dizix = [float(x) for x in self.dizix]    # "dizi" adlı dizide bulunan tüm elemanlar integera çevrilerek aynı diziye aktarıldı
        self.diziy = [float(x) for x in self.diziy]
        uygunluk_sonuc = []    # x değerleri ve y değerlerinin toplamında oluşan sonuçları tutan dizi

        i=0
        for i in range(0,self.popsize):
            uygunluk_sonuc.append("{:.2f}".format(self.dizix[i] + self.diziy[i]))
            # uygunluk fonksiyonu yazdırılıyor
            fonksiyon = "V{} = ({},{})  ==>  {}".format(i+1,self.dizix[i],self.diziy[i],uygunluk_sonuc[i])
            self.listbox2.insert(END,fonksiyon)   # uygunluk fonksiyonu sonuçları yazdırıldı

        #fmax xmax hesaplanıyor
        uygunluk_sonuc = [float(i) for i in uygunluk_sonuc]

        return uygunluk_sonuc,self.dizix,self.diziy


    def parametre_belirle(self):

        if(self.aralik1.get()!="" and self.aralik2.get() == ""):
            self.gen_sayisi=0
            y=1
            self.aralikx=int(self.aralik1.get())
            for y in range(1,20):
                if (self.aralikx <= ((2**y)-1)):
                    self.gen_sayisi=y
                    break

            self.popsize = int(self.pop_size.get())
            self.m1.configure(state="normal")
            self.m1.delete(0,END)
            self.m1.insert(END,self.gen_sayisi)
            self.m1.configure(state="readonly")
            self.listbox2.insert(END,"Parametreler Belirlendi: Amaç [0-{}] aralığında y=x2 fonksiyonu ile maksimumu bulmak".format(self.aralik1.get()))
            self.listbox2.insert(END,"Pop_Size {} olarak belirlendi".format(self.pop_size.get()))
            self.listbox2.insert(END,"Her Kromozomdaki Gen Sayısı {} olarak belirlendi".format(self.m1.get()))
            self.listbox2.insert(END,"Çaprazlama Olasılığı(PC)  {} olarak belirlendi".format(self.pc.get()))
            self.listbox2.insert(END,"Mutasyon Olasılığı (PM) {} olarak belirlendi".format(self.pm.get()))

        if(self.aralik1.get()!="" and self.aralik2.get()!=""):
            aralikx=int(self.aralik1.get())
            araliky=int(self.aralik2.get())
            if(self.pop_size.get()=="" or self.k.get()==""):
                print("popsize belirle")
            else:
                self.gen_sayisi=0
                self.gen2_sayisi=0
                hassasiyet = int(self.k.get())
                y=1
                for y in range(1,20):
                    if((aralikx-0)*(10**hassasiyet) <= (2**y)-1):
                        self.gen_sayisi=y
                        break
                y=1
                for y in range(1,20):
                    if((araliky-0)*(10**hassasiyet) <= (2**y)-1):
                        self.gen2_sayisi=y
                        break

                self.m1.configure(state="normal")
                self.m1.delete(0,END)
                self.m1.insert(END,self.gen_sayisi)
                self.m1.configure(state="readonly")
                self.m2.configure(state="normal")
                self.m2.delete(0,END)
                self.m2.insert(END,self.gen2_sayisi)
                self.m2.configure(state="readonly")
                self.listbox2.insert(END,"Parametreler Belirlendi:")
                self.listbox2.insert(END,"Amaç F(x,y) = x+y, fonksiyonun x ∈ {}, y ∈ {} maksimumunu bulmak ".format(aralikx,araliky))
                self.listbox2.itemconfig(END,bg="red",fg="white")
                self.listbox2.insert(END,"Pop_Size {} olarak belirlendi".format(self.pop_size.get()))
                self.listbox2.insert(END,"X Kromozomlarındaki gen Sayisi {} olarak belirlendi".format(self.m1.get()))
                self.listbox2.insert(END,"Y Kromozomlarındaki gen sayisi {} olarak belirlendi.".format(self.m2.get()))
                self.listbox2.insert(END,"Virgülden Sonra Gereken Hassasiyet(k) {} olarak belirlendi".format(self.k.get()))
                self.listbox2.insert(END,"Çaprazlama Olasılığı(PC)  {} olarak belirlendi".format(self.pc.get()))
                self.listbox2.insert(END,"Mutasyon Olasılığı (PM) {} olarak belirlendi".format(self.pm.get()))

    def ilkel_populasyon_olustur(self):
        self.listbox2.insert(END,"---------------JENERASYON 1-----------------")
        self.listbox2.insert(END,"")
        self.toplam_kromozom_gen = int(self.m1.get())
        self.listbox2.insert("end","--1A-- Rastgele ilkel Popülasyon Oluşturuldu--1A--")
        self.listbox2.itemconfig(END,bg="red",fg="white")
        self.populasyon1=[]
        self.populasyon1binary=[]
        self.populasyon1decimal=[]
        self.popsize = int(self.pop_size.get())

        #
        for i in range(0,self.popsize):
            sayi=np.random.choice([0, 1], size=(int(self.m1.get()),), p=[1./3, 2./3])
            self.populasyon1.append(sayi)

        for i in range(0,self.popsize):
            cikti = "V{} = {}".format(i+1,self.populasyon1[i])
            self.listbox2.insert(END,cikti)

    def ilkel_populasyon_olustur2(self):

        self.listbox2.insert(END,"---------------JENERASYON 1-----------------")
        self.listbox2.insert(END,"")
        self.toplam_kromozom_gen = int(self.m1.get()) + int(self.m2.get())
        self.listbox2.insert(END,"1.) Rastgele İlkel Popülasyon Oluşturuldu")
        self.listbox2.itemconfig(END,bg="red",fg="white")

        self.popsize = int(self.pop_size.get())
        self.gensayisix = int(self.m1.get())
        self.gensayisiy = int(self.m2.get())
        self.ilkel_populasyonx = []
        self.ilkel_populasyony = []
        self.populasyon_binaryx=[]
        self.populasyon_binaryy=[]
        self.populasyon_decimalx=[]
        self.populasyon_decimaly=[]

        # İlkel Populasyon random olarak oluşturuldu ve dizelere akarıldı
        i =0
        for i in range(0,self.popsize):
            sayix=np.random.choice([0, 1], size=(self.gensayisix), p=[1./3, 2./3])
            sayiy=np.random.choice([0, 1], size=(self.gensayisiy), p=[1./3, 2./3])
            self.ilkel_populasyonx.append(sayix)
            self.ilkel_populasyony.append(sayiy)
            cikti = "V{} = {},{}".format(i+1,self.ilkel_populasyonx[i],self.ilkel_populasyony[i])
            self.listbox2.insert(END,cikti)

        # Bitler arasındaki boşluklar kaldırılıyor
        uzunluk = len(self.ilkel_populasyonx[0])
        sayi2=""
        for y in range(0,self.popsize):
            for z in range(0,uzunluk):
                sayi2="{}{}".format(sayi2,self.ilkel_populasyonx[y][z])
                sayi2=str(sayi2)
            self.populasyon_binaryx.append(sayi2)
            sayi2=""
        uzunluk = len(self.ilkel_populasyony[0])
        sayi2=""
        y=0; z=0;
        for y in range(0,self.popsize):
            for z in range(0,uzunluk):
                sayi2="{}{}".format(sayi2,self.ilkel_populasyony[y][z])
                sayi2=str(sayi2)
            self.populasyon_binaryy.append(sayi2)
            sayi2=""



    global jenerasyon_count


    def basla(self):
        self.pdf_yazilacak=[]

        jenerasyon_count = 1
        self.jenerason_sayisi = int(self.jenerasyonsayisi.get())
        while (jenerasyon_count <= self.jenerason_sayisi):

            if(self.m2.get()==""):

                if(jenerasyon_count == 1):
                    print("ilkel tmm")
                    self.ilkel_populasyon_olustur()

                    uzunluk = len(self.populasyon1[0])
                    sayi2=""
                    y=0
                    for y in range(0,self.popsize):
                        for z in range(0,uzunluk):
                            sayi2="{}{}".format(sayi2,self.populasyon1[y][z])
                            sayi2=str(sayi2)
                        self.populasyon1binary.append(sayi2)
                        sayi2=""


                    self.listbox2.insert("end","")
                    self.listbox2.insert(END,"---- Popülasyon Değerlendirildi----")
                    self.listbox2.itemconfig(END,bg="red",fg="white")
                    sayac = 0
                    for sayac in range(0,self.popsize):
                        decimal = self.binaryToDecimal(int(self.populasyon1binary[sayac]))
                        sonuc = "v{} = {}  =>  {}".format(sayac+1,self.populasyon1binary[sayac],decimal)
                        self.populasyon1decimal.append(decimal)
                        self.listbox2.insert(END,sonuc)
                    self.uygunlukFonksiyonu_kare(self.populasyon1decimal)
                    self.listbox2.insert(END,"")
                    self.fmax1 =max(self.populasyon1decimal)
                    self.xmax1_index=[]
                    index2=0
                    for index2 in range(0,self.popsize):
                        if(self.fmax1==self.populasyon1decimal[index2]):
                            self.xmax1_index.append(index2)
                    self.listbox2.insert(END,"fMax{}= {}".format(jenerasyon_count,self.fmax1))
                    self.pdf_yazilacak.append("fMax{}= {}".format(jenerasyon_count,self.fmax1))  ### daha sonra pdf e yazmak üzere diziye eklendi
                    self.pdf_yazilacak.append("")
                    len1 = len(self.xmax1_index)
                    for index in range(0,len1):
                        self.listbox2.insert(END,"xmax{}{} = {}".format(jenerasyon_count,self.xmax1_index[index]+1,self.populasyon1binary[int(self.xmax1_index[index])]))
                        #daha sonra xmax ı pdf yazacağız o yüzden diziye ekledik
                        self.pdf_yazilacak.append("xmax{}{} = {}".format(jenerasyon_count,self.xmax1_index[index]+1,self.populasyon1binary[int(self.xmax1_index[index])]))
                    self.pdf_yazilacak.append("")
                    self.pdf_yazilacak.append("")
                    jenerasyon_count += 1
###################### YUKARIDAKİ KOD BLOĞU SADECE JENERASYON 1 DE ÇALIŞIR ÇÜNKÜ DEĞER HESAPLAMALARI MUTASYONDAN SONRA ÇALIŞMAKTADIR.#######


                if(jenerasyon_count <= self.jenerason_sayisi):
                    print(jenerasyon_count)
                else:
                    break

                # SEÇİM İŞLEMİ BAŞLADI
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"Seçim işlemleri yapıldı")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                F=0
                sonuc=""
                sayac=0
                for sayac in range(0,self.popsize):
                    F=F+int(self.dizi[sayac])
                    sonuc = "{} + {}".format(sonuc,str(self.dizi[sayac]))
                self.listbox2.insert(END,"F = {}  => {}".format(sonuc,F))           #f bulundu
                self.secilme_ihtimali=[]
                sayac2=0
                for sayac2 in range(0,self.popsize):
                    ihtimal = int(self.dizi[sayac2]) / int(F)
                    self.secilme_ihtimali.append(ihtimal)

                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"Her bir Kromozomun secilme ihtimali :")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                y=0
                for y in range(0,self.popsize):
                    cikti = "P{} = {:.4f}".format(y+1,self.secilme_ihtimali[y])    # secilme ihtimali yazdırıldı
                    self.listbox2.insert(END,cikti)

                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"Her bir Kromozomun Ardışık ihtimali :")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                self.ardisik_ihtimali=[]
                sayac2=0
                for sayac2 in range(0,self.popsize):
                    if sayac2==0:
                        self.ardisik_ihtimali.append(self.secilme_ihtimali[0])
                    else:
                        index = sayac2 - 1
                        ardisikihtimal = self.ardisik_ihtimali[index] + self.secilme_ihtimali[sayac2]
                        self.ardisik_ihtimali.append(ardisikihtimal)

                y=0
                cikti=""
                for y in range(0,self.popsize):
                    cikti = "Q{} = {:.4f}".format(y+1,self.ardisik_ihtimali[y])    # Ardışık ihtimali yazdırıldı
                    self.listbox2.insert(END,cikti)

                self.listbox2.insert("end","")
                self.listbox2.insert(END,"Rastgele [0-1] aralığında {} adet sayi üretildi".format(self.popsize))    #random sayı üretiliyor
                self.listbox2.itemconfig(END,bg="red",fg="white")
                self.random1sayilar = []
                i=0
                for i in range(0,self.popsize):
                    rand = random.uniform(0,1)
                    self.random1sayilar.append("{:.4f}".format(rand))
                self.listbox2.insert("end","Random Sayilar:")
                i=0
                for i in range(0,len(self.random1sayilar)):
                    self.listbox2.insert("end","r{} = {}".format(i+1,self.random1sayilar[i]))

                ####### her üretilen r sayısı için i'nci kromozomun yerine eski jenerasyondan kromozomların değişikliği analiz ediliyor.
                i=0
                y=0
                self.jenerasyon2_index=[]

                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"Her bir üretilen r sayısı için yer değişikliği hesaplandı")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                for i in range(0,len(self.random1sayilar)):
                    for y in range(0,self.popsize):
                        if ((float(self.random1sayilar[i])) > 0 and (float(self.random1sayilar[i]) <= self.ardisik_ihtimali[y])):
                            self.jenerasyon2_index.append(y)
                            self.listbox2.insert(END,"r{} < Q1".format(i+1))
                            break
                        if (float(self.random1sayilar[i])>self.ardisik_ihtimali[y] and float(self.random1sayilar[i])<=self.ardisik_ihtimali[y+1]):
                            self.jenerasyon2_index.append(y+1)
                            self.listbox2.insert(END,"Q{} < r{} < Q{}".format(y+1,i+1,y+2))
                            break
                i=0
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"{}. Jenerasyon 1. Populasyon Aşağıdaki Gibidir".format(jenerasyon_count))
                self.listbox2.itemconfig(END,bg="red",fg="white")

                for i in range (0,len(self.jenerasyon2_index)):
                    cikti =""
                    yeniindex=self.jenerasyon2_index[i] + 1
                    cikti="V{} = V{}eski = {}".format(i+1,self.jenerasyon2_index[i]+1,self.populasyon1binary[self.jenerasyon2_index[i]])
                    self.listbox2.insert(END,cikti)
                self.duz_caprazlama()

                self.listbox2.insert(END,"Çaprazlama Sonucu Populasyonun Son Hali Aşağıdadır")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                i=0
                for i in range(0,self.popsize):
                    self.listbox2.insert(END,"V{} = {}".format(i+1,self.caprazlama_populasyon[i]))
                self.mutasyon_populasyon = self.caprazlama_populasyon

                self.mutasyon_duz()
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"Mutasyon Sonucu Oluşan Son Populasyon:")
                self.mutasyon_decimal=[]
                self.listbox2.itemconfig(END,bg="red",fg="white")
                i=0
                for i in range(0,len(self.mutasyon_populasyon)):
                    self.listbox2.insert(END,"V{} = {}".format(i+1,self.mutasyon_populasyon[i]))
                    decimal =self.binaryToDecimal(int(self.mutasyon_populasyon[i]))
                    self.mutasyon_decimal.append(decimal)
                self.listbox2.insert(END,"Populasyon Değerlendirildi")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                i=0
                for i in range(0,len(self.mutasyon_decimal)):
                    self.listbox2.insert(END,"V{} = {}  ==>  {}".format(i+1,self.mutasyon_populasyon[i],self.mutasyon_decimal[i]))

                self.listbox2.insert("end","Her Bir Kromozom için uygunluk fonksiyonu y=x^2")
                self.listbox2.itemconfig(END,bg="red",fg="white")
                self.dizi = []
                self.dizi = self.mutasyon_decimal
                x=0
                for x in range (0,self.popsize):
                    fonksiyon=""
                    self.dizi[x] = int(self.mutasyon_decimal[x])
                    self.dizi[x] = self.mutasyon_decimal[x] * self.mutasyon_decimal[x]
                    fonksiyon = "v{} = {} ==> {}".format(x+1,self.mutasyon_populasyon[x],self.mutasyon_decimal[x])
                    self.listbox2.insert(END,fonksiyon)

                self.fmax2 =max(self.mutasyon_decimal)
                self.xmax2_index=[]
                index2=0
                for index2 in range(0,self.popsize):
                    if(self.fmax2==self.mutasyon_decimal[index2]):
                        self.xmax2_index.append(index2)
                self.listbox2.insert(END,"fmax{}= {}".format(jenerasyon_count,self.fmax2))
                self.pdf_yazilacak.append("fmax{}= {}".format(jenerasyon_count,self.fmax2))
                self.pdf_yazilacak.append("")
                lenmax2 = len(self.xmax2_index)
                for index in range(0,lenmax2):
                    self.listbox2.insert(END,"xmax{}{} = {}".format(jenerasyon_count,self.xmax2_index[index]+1,self.mutasyon_populasyon[int(self.xmax2_index[index])]))
                    self.pdf_yazilacak.append("xmax{}{} = {}".format(jenerasyon_count,self.xmax2_index[index]+1,self.mutasyon_populasyon[int(self.xmax2_index[index])]))
                self.pdf_yazilacak.append("")
                self.pdf_yazilacak.append("")
                ### başa sardığında dizilerin çakışmaması için aynı dizi isimlerine değişkenler aktarılıyor
                self.populasyon1binary = []
                self.populasyon1binary = self.mutasyon_populasyon
                self.populasyon1decimal=[]
                #self.populasyon1decimal = self.mutasyon_decimal
                jenerasyon_count +=1






    ## vir güllü çözüm
            else:  # Virgüllü çözüm yapılacaksa buradan başlar###########################******************************###################################

                if (jenerasyon_count == 1):
                    self.ilkel_populasyon_olustur2()

                    # İlkel populasyon Değerlendiriliyor
                    self.listbox2.insert("end","")
                    self.listbox2.insert(END,"------İlkel Popülasyon Değerlendirildi------")
                    self.listbox2.itemconfig(END,bg="red",fg="white")

                    for sayac in range(0,self.popsize):
                        decimalx = self.binaryToDecimal(int(self.populasyon_binaryx[sayac]))
                        decimaly = self.binaryToDecimal(int(self.populasyon_binaryy[sayac]))
                        self.populasyon_decimalx.append(decimalx)
                        self.populasyon_decimaly.append(decimaly)
                        sonuc = "v{} = {},{}  =>  ({},{})".format(sayac+1,self.populasyon_binaryx[sayac],self.populasyon_binaryy[sayac],decimalx,decimaly)
                        self.listbox2.insert(END,sonuc)

                    #  x ve y 'nin decimal değerlerinin kopyası alındı
                    self.yeni_decimalx=[]
                    self.yeni_decimaly=[]


                    self.listbox2.insert("end","")
                    self.listbox2.insert(END,"------İlkel Popülasyon Değerleri [0,{}] ve [0,{}] arasına indirgeniyor------".format(self.aralik1.get(),self.aralik2.get()))
                    self.listbox2.itemconfig(END,bg="red",fg="white")



                    i=0
                    m1 = int(self.m1.get())   #fonksiyonun x gen sayisi
                    m2 = int(self.m2.get())   #fonksiyonun y gen sayisi
                    b1 = int(self.aralik1.get())    # fonksiyon 1. genin maksimumu sınırı
                    b2 = int(self.aralik2.get())    # fonksiyon 2. genin maksimumu sınırı
                    for i in range(0,self.popsize):
                        decimalx = self.populasyon_decimalx[i]
                        decimaly = self.populasyon_decimaly[i]
                        # indirgeme
                        decimalx = ((decimalx * b1) / ((2 ** m1)-1))  # a = 0 olarak alındı indirgeme formülü
                        decimaly = ((decimaly * b2) / ((2 ** m2)-1))  # a = 0 olarak alındı indirgeme formülü

                        #dönüştürülen değerler tekrar aynı diziye yükleniyor  virgülden sonra sadece 2 hane yazılıyor
                        self.yeni_decimalx.append("{:.2f}".format(decimalx))
                        self.yeni_decimaly.append("{:.2f}".format(decimaly))


                        #dönüştürülen değerler listboxda görüntüleniyor
                        sonuc="V{0} = ({1},{2})  =>  ({3},{4})".format(i+1,self.populasyon_decimalx[i],self.populasyon_decimaly[i],self.yeni_decimalx[i],self.yeni_decimaly[i])
                        self.listbox2.insert(END,sonuc)

                    self.listbox2.insert(END,"")
                    self.listbox2.insert(END,"2.) Her Bir Kromozom İçin Uygunluk Fonksiyonu Hesaplandı.")
                    self.listbox2.itemconfig(END,bg="red",fg="white")

                    # uygunluktoplam fonksiyonu calıstırıldı ve return değerleri yeni bir diziye aktarıldı
                    self.uygunluk_sonuc,self.dizix,self.diziy = self.uygunlukFonksiyonu_toplam(self.yeni_decimalx,self.yeni_decimaly)

                    #uygunluk fonksiyonu sonucu oluşan populasyon değişkene aktarılıyor ve fmax xmax yazdırılıyor

                    self.fmax1=max(self.uygunluk_sonuc)
                    self.xmax1_index=[]
                    i=0
                    for i in range(0,self.popsize):    #fmax1 kaçtane mevcut bilmiyoruz 1 den fazla ihtimali var bu nedenle indexlerini aldık her bir fmaxın
                        if(self.fmax1 == self.uygunluk_sonuc[i]):
                            self.xmax1_index.append(i)

                    #fmax1 ve xmax1 , ymax1 ler yazdırılıyor
                    self.listbox2.insert(END,"")
                    self.listbox2.insert(END,"Fmax{} = {}".format(jenerasyon_count,self.fmax1))
                    self.pdf_yazilacak.append("Fmax{} = {}".format(jenerasyon_count,self.fmax1)) # daha sonra pdf'e yazılmak üzere diziye eklendi
                    self.pdf_yazilacak.append("")
                    i=0
                    for i in range (0,len(self.xmax1_index)):
                        self.listbox2.insert(END,"xmax{}{} = {}".format(jenerasyon_count,self.xmax1_index[i]+1,self.dizix[self.xmax1_index[i]]))    #x değeri
                        self.listbox2.insert(END,"ymax{}{} = {}".format(jenerasyon_count,self.xmax1_index[i]+1,self.diziy[self.xmax1_index[i]]))    #y değeri
                        # x max ve y max lar pdf'e yazılacak onun için önce diziye ekledik
                        self.pdf_yazilacak.append("xmax{}{} = {}".format(jenerasyon_count,self.xmax1_index[i]+1,self.dizix[self.xmax1_index[i]]))
                        self.pdf_yazilacak.append("ymax{}{} = {}".format(jenerasyon_count,self.xmax1_index[i]+1,self.diziy[self.xmax1_index[i]]))

                    self.pdf_yazilacak.append("")
                    self.pdf_yazilacak.append("")
                    jenerasyon_count +=1
    ##################################### SEÇİM İŞLEMLERİ BAŞLIYOR######################### #yukarıdakiler sadece 1 kere çalışır
                if(jenerasyon_count>self.jenerason_sayisi):
                    break

                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"3.) {}.Jenerasyon için Seçim İşlemleri Yapıldı:".format(jenerasyon_count))
                self.listbox2.itemconfig(END,bg="red",fg="white")
                F=0.0
                self.uygunluk_sonuc = [float(i) for i in self.uygunluk_sonuc]   #DEGERLER FLOAT'a ÇEVRİLDİ
                i=0
                for i in range(0,len(self.uygunluk_sonuc)):      #F HESAPLANDI
                    F=F+self.uygunluk_sonuc[i]
                self.listbox2.insert(END,"a.) F = {:.2f}".format(F))
                self.listbox2.itemconfig(END,bg="green",fg="white")

                self.secilme_ihtimali = []  # Her bir kromozomun seçilme ihtimali hesaplanacak

                self.secilme_ihtimali = [i/F for i in self.uygunluk_sonuc]
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"b.) Her Bir Kromozomun Seçilme İhtimali Hesaplandı:")
                self.listbox2.itemconfig(END,bg="green",fg="white")
                i=0
                for i in range (0,len(self.secilme_ihtimali)):
                    ihtimal = self.uygunluk_sonuc[i] / F
                    cikti = "P{} = {} / {:.2f} = {:.3f}".format(i+1,self.uygunluk_sonuc[i],F,self.secilme_ihtimali[i])
                    self.listbox2.insert(END,cikti)

                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"c.) Her bir Kromozomun Ardışık ihtimali Hesaplandı:")
                self.listbox2.itemconfig(END,bg="green",fg="white")

                self.ardisik_ihtimali=[]
                i=0
                for i in range(0,self.popsize):
                    if i==0:     # q1 için direk p1 alınır
                        self.ardisik_ihtimali.append(self.secilme_ihtimali[0])
                        cikti = "Q{} = P{}  = {:.2f}".format(i+1,i+1,self.secilme_ihtimali[i])
                        self.listbox2.insert(END,cikti)
                    else:
                        index=i -1
                        ardisikihtimal = self.ardisik_ihtimali[index] + self.secilme_ihtimali[i]
                        self.ardisik_ihtimali.append(ardisikihtimal)
                        cikti ="Q{} = Q{} + P{} => {:.2f} + {:.2f} = {:.3f}".format(i+1,i,i+1,self.ardisik_ihtimali[index],self.secilme_ihtimali[i],self.ardisik_ihtimali[i])
                        self.listbox2.insert(END,cikti)

                # d şıkı için popsize kadar random sayı üretiliyor.
                self.listbox2.insert("end","")
                self.listbox2.insert(END,"d.) Rastgele [0-1] aralığında {} adet sayi üretildi".format(self.popsize))    #random sayı üretiliyor
                self.listbox2.itemconfig(END,bg="green",fg="white")
                self.random1sayilar = []
                i=0
                for i in range(0,self.popsize):
                    rand = random.uniform(0,1)
                    self.random1sayilar.append("{:.3f}".format(rand))
                    cikti = "r{} = {:.3f}".format(i+1,rand)
                    self.listbox2.insert(END,cikti)

                ####### her üretilen r sayısı için i'nci kromozomun yerine eski jenerasyondan kromozomların değişikliği analiz ediliyor.

                self.jenerasyon2_index=[]
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"e.) Her bir üretilen r sayısı için yer değişikliği hesaplandı")
                self.listbox2.itemconfig(END,bg="green",fg="white")
                i=0; y=0;
                for i in range(0,len(self.random1sayilar)):
                    for y in range(0,self.popsize):
                        if ((float(self.random1sayilar[i])) > 0 and (float(self.random1sayilar[i]) <= self.ardisik_ihtimali[y])):
                            self.jenerasyon2_index.append(y)
                            self.listbox2.insert(END,"r{} < Q1".format(i+1))
                            break
                        if (float(self.random1sayilar[i])>self.ardisik_ihtimali[y] and float(self.random1sayilar[i])<=self.ardisik_ihtimali[y+1]):
                            self.jenerasyon2_index.append(y+1)
                            self.listbox2.insert(END,"Q{} < r{} < Q{}".format(y+1,i+1,y+2))
                            break
                i=0
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"{}. Jenerasyon 1. Populasyon Aşağıdaki Gibidir".format(jenerasyon_count))
                self.listbox2.itemconfig(END,bg="blue",fg="white")

                for i in range (0,len(self.jenerasyon2_index)):
                    cikti =""
                    yeniindex=self.jenerasyon2_index[i] + 1
                    cikti="V{} = V{}eski = {},{}".format(i+1,self.jenerasyon2_index[i]+1,self.populasyon_binaryx[self.jenerasyon2_index[i]],self.populasyon_binaryy[self.jenerasyon2_index[i]])
                    self.listbox2.insert(END,cikti)

                ## populasyon degiskeni güncelleniyor
                self.caprazlanacak_binaryx=[]
                self.caprazlanacak_binaryy=[]
                i=0
                for i in range(0,len(self.jenerasyon2_index)):
                    self.caprazlanacak_binaryx.append(self.populasyon_binaryx[self.jenerasyon2_index[i]])
                    self.caprazlanacak_binaryy.append(self.populasyon_binaryy[self.jenerasyon2_index[i]])

                # Çaprazlama sonucunda oluşan populasyon degerleri caprazlama fonksiyonundan return ediliyor ve yeni değişkenlere atarıldı
                #Mutasyona sokmak için bu dizileri kullanacağız
                self.mutasyon_degerlerix=[]
                self.mutasyon_degerleriy=[]
                self.mutasyon_degerlerixy=[]
                self.mutasyon_degerlerix,self.mutasyon_degerleriy,self.mutasyon_degerlerixy = self.ikiliCaprazlama(self.caprazlanacak_binaryx,self.caprazlanacak_binaryy)
                #Mutasyon sonucun oluşan x değerleri , y değerleri ve x ve y nin birleşimini oluşturan değerler alındı
                self.sonuc_populasyonx=[]
                self.sonuc_populasyony=[]
                self.sonuc_populasyonxy=[]
                self.sonuc_populasyonx,self.sonuc_populasyony,self.sonuc_populasyonxy=self.mutasyon_ikili(self.mutasyon_degerlerix,self.mutasyon_degerleriy,self.mutasyon_degerlerixy)
                #Bu değerlerin decimal karşılığı bulunacak (DEĞERLENDİRİLİYOR)

                self.listbox2.insert("end","")
                self.listbox2.insert(END,"6.) {} Jenerasyon Mutasyon Sonucu oluşan popülasyon Değerlendiriliyor".format(jenerasyon_count))
                self.listbox2.itemconfig(END,bg="red",fg="white")

                self.sonuc_decimalx=[]
                self.sonuc_decimaly=[]

                for sayac in range(0,self.popsize):
                    decimalx = self.binaryToDecimal(int(self.sonuc_populasyonx[sayac]))
                    decimaly = self.binaryToDecimal(int(self.sonuc_populasyony[sayac]))
                    self.sonuc_decimalx.append(decimalx)
                    self.sonuc_decimaly.append(decimaly)
                    sonuc = "v{} = {},{}  =>  ({},{})".format(sayac+1,self.sonuc_populasyonx[sayac],self.sonuc_populasyony[sayac],decimalx,decimaly)
                    self.listbox2.insert(END,sonuc)


                #  x ve y 'nin decimal değerlerinin kopyası alındı
                self.yeni2_decimalx=[]
                self.yeni2_decimaly=[]

                self.listbox2.insert("end","")
                self.listbox2.insert(END,"{} jenerasyon mutasyon sonucu oluşan değerleri [0,{}] ve [0,{}] arasına indirgeniyor".format(jenerasyon_count,self.aralik1.get(),self.aralik2.get()))
                self.listbox2.itemconfig(END,bg="green",fg="white")
                i=0
                m1 = int(self.m1.get())   #fonksiyonun x gen sayisi
                m2 = int(self.m2.get())   #fonksiyonun y gen sayisi
                b1 = int(self.aralik1.get())    # fonksiyon 1. genin maksimumu sınırı
                b2 = int(self.aralik2.get())    # fonksiyon 2. genin maksimumu sınırı
                for i in range(0,self.popsize):
                    decimalx = self.sonuc_decimalx[i]
                    decimaly = self.sonuc_decimaly[i]
                    # indirgeme
                    decimalx = ((decimalx * b1) / ((2 ** m1)-1))  # a = 0 olarak alındı indirgeme formülü
                    decimaly = ((decimaly * b2) / ((2 ** m2)-1))  # a = 0 olarak alındı indirgeme formülü

                    #dönüştürülen değerler tekrar aynı diziye yükleniyor  virgülden sonra sadece 2 hane yazılıyor
                    self.yeni2_decimalx.append("{:.2f}".format(decimalx))
                    self.yeni2_decimaly.append("{:.2f}".format(decimaly))


                    #dönüştürülen değerler listboxda görüntüleniyor
                    sonuc="V{0} = ({1},{2})  =>  ({3},{4})".format(i+1,self.sonuc_decimalx[i],self.sonuc_decimaly[i],self.yeni2_decimalx[i],self.yeni2_decimaly[i])
                    self.listbox2.insert(END,sonuc)
                #Dönüştürülen değerlerin uygunluk fonksiyonu hesaplanıyor.
                self.uygunluk_sonuc2=[]
                self.uygunluk_sonuc2,self.degerlerx,self.degerlery = self.uygunlukFonksiyonu_toplam(self.yeni2_decimalx,self.yeni2_decimaly)
                #fmax2 xmax2 bulunuyor
                self.uygunluk_sonuc2 = [float(i) for i in self.uygunluk_sonuc2]
                self.fmax2 = max(self.uygunluk_sonuc2)
                self.xmax_sonuc_index=[]
                i=0
                for i in range(0,self.popsize):    #fmax2 kaçtane mevcut bilmiyoruz 1 den fazla ihtimali var bu nedenle indexlerini aldık her bir fmaxın
                    if(self.fmax2 == self.uygunluk_sonuc2[i]):
                        self.xmax_sonuc_index.append(i)
                #fmax2 ve xmax2 , ymax2 ler yazdırılıyor
                self.listbox2.insert(END,"")
                self.listbox2.insert(END,"Fmax{} = {}".format(jenerasyon_count,self.fmax2))
                self.pdf_yazilacak.append("Fmax{} = {}".format(jenerasyon_count,self.fmax2))
                self.pdf_yazilacak.append("")
                i=0
                for i in range (0,len(self.xmax_sonuc_index)):
                    self.listbox2.insert(END,"xmax{}{} = {}".format(jenerasyon_count,self.xmax_sonuc_index[i]+1,self.degerlerx[self.xmax_sonuc_index[i]]))    #x değeri
                    self.listbox2.insert(END,"ymax{}{} = {}".format(jenerasyon_count,self.xmax_sonuc_index[i]+1,self.degerlery[self.xmax_sonuc_index[i]]))    #y değeri

                    self.pdf_yazilacak.append("xmax{}{} = {}".format(jenerasyon_count,self.xmax_sonuc_index[i]+1,self.degerlerx[self.xmax_sonuc_index[i]]))
                    self.pdf_yazilacak.append("ymax{}{} = {}".format(jenerasyon_count,self.xmax_sonuc_index[i]+1,self.degerlery[self.xmax_sonuc_index[i]]))
                self.pdf_yazilacak.append("")
                self.pdf_yazilacak.append("")
                # 2 üzeri jenerasyonlarda başa döndüğünde dizi çakışmaması için diziler eşitleniyor

                self.uygunluk_sonuc =[]
                self.uygunluk_sonuc = self.uygunluk_sonuc2
                self.decimalx = self.degerlerx
                self.decimaly = self.degerlery
                """self.populasyon_binaryx = []
                self.populasyon_binaryx = self.sonuc_populasyonx
                self.populasyon_binaryy=[]
                self.sonuc_populasyony
                self.populasyon1binary = self.sonuc_populasyonxy
                #self.populasyon1decimal=[]"""
                jenerasyon_count +=1


    def ikiliCaprazlama(self,binaryx,binaryy):

        self.c_binaryx=binaryx
        self.c_binaryy=binaryy
        self.xy_populasyon=[]    # caprzlanacak kromozomların x ve y kısımları birleştiriliyor

        # çaprazlama işlemi için x ve y kısımları birleştiriliyor
        for i in range(0,len(self.caprazlanacak_binaryx)):
            kromozom ="{}{}".format(self.c_binaryx[i],self.c_binaryy[i])
            self.xy_populasyon.append(kromozom)


        caprazlama_ihtimali = float(self.pc.get())
        c_k_s = self.popsize*caprazlama_ihtimali      #caprazlanacak kromozom sayisi
        if (c_k_s % 2 !=0):                       #eğer kromozom sayisi çift değilse
            c_k_s = round(c_k_s)                  #önce sayı en yakın reel sayıya yuvarlanır
            if(c_k_s % 2 !=0):                     # eğer sayı haala çift değilse
                c_k_s  = c_k_s + 1                  #sayı bir artırılarak çift yapılır
                if(c_k_s > self.popsize):           #eğer çift olan sayı popsize'dan yani max kromozom sayısından büyükse
                    c_k_s = c_k_s -2                #en yakın çift sayıya düşürülür

        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"4.) Caprazlama için parametreler:")
        self.listbox2.itemconfig(END,bg="red",fg="white")
        self.listbox2.insert(END,"pc(Çaprazlama İhtimali) = {}".format(caprazlama_ihtimali))
        self.listbox2.insert(END,"Pop_size x Pc (Çaprazlanacak Kromozom Sayisi) = {}".format(c_k_s))
        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"[1,{}] aralığında rastgele {} tane tamsayı üretildi".format(self.popsize,c_k_s))
        self.listbox2.itemconfig(END,bg="green",fg="white")
        i=0
        self.caprazlama_random=[]
        self.caprazlama_random = random.sample(range(1,self.popsize+1),c_k_s)   ##Birbirinden farklı rastgele sayılar üretiliyor
        for y in range(0,len(self.caprazlama_random)):
                self.listbox2.insert(END,"r{} = {}".format(y+1,self.caprazlama_random[y]))
        while (i<len(self.caprazlama_random)):

            self.listbox2.insert(END,"v{} ile v{} çaprazlanacak".format(self.caprazlama_random[i],self.caprazlama_random[i+1]))
            self.listbox2.itemconfig(END,bg="green",fg="white")

            pos =random.randint(1,self.toplam_kromozom_gen-1)
            self.listbox2.insert(END,"Rastgele [1-{}] arasında pos belirlendi : {}".format(self.toplam_kromozom_gen-1,pos))

            self.listbox2.insert(END,"V{} = {}".format(self.caprazlama_random[i],self.xy_populasyon[self.caprazlama_random[i]-1]))
            self.listbox2.insert(END,"V{} = {}".format(self.caprazlama_random[i+1],self.xy_populasyon[self.caprazlama_random[i+1]-1]))
            gecici1_indeks =int( self.caprazlama_random[i]-1)
            gecici2_indeks =int(self.caprazlama_random[i+1]-1)
            gecici1 = self.xy_populasyon[gecici1_indeks][pos:len(self.xy_populasyon[gecici1_indeks])]
            gecici2 = self.xy_populasyon[gecici2_indeks][pos:len(self.xy_populasyon[gecici2_indeks])]
            change_binary=self.xy_populasyon[self.caprazlama_random[i]-1]
            change_binary2 = self.xy_populasyon[self.caprazlama_random[i+1]-1]
            change_binary_sonuc = change_binary[0:pos] + gecici2
            change_binary2_sonuc = change_binary2[0:pos] + gecici1
            self.listbox2.insert(END,"")
            self.listbox2.insert(END,"Çaprazlama İşlemi Tamamlandı")
            self.listbox2.insert(END,"v{0}={1}   =>   v{2}'={3}".format(self.caprazlama_random[i],change_binary,self.caprazlama_random[i],change_binary_sonuc))
            self.listbox2.insert(END,"v{0}={1}   =>   v{2}'={3}".format(self.caprazlama_random[i+1],change_binary2,self.caprazlama_random[i+1],change_binary2_sonuc))
            self.listbox2.insert(END,"")

            # Çaprazlama işlemi sonucunda populasyondaki değişen değerler güncellendi
            self.xy_populasyon[self.caprazlama_random[i]-1] = change_binary_sonuc
            self.xy_populasyon[self.caprazlama_random[i+1]-1] = change_binary2_sonuc
            i=i+2
        #çaprazlama işlemi sonucu kromozomlar tekrar virgüllü haale getiriliyor, virgülü nereye koyacağız onun için xgensayisi öğreniliyor
        # gen sayisi parametre belirleme kısmında gensayisix değişkenine aktarılmıştı
        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"Çaprazlama Sonucu Oluşan Populasyon:")
        self.listbox2.itemconfig(END,bg="blue",fg="white")
        i=0
        for i in range(0,len(self.xy_populasyon)):
            kromozomx=self.xy_populasyon[i][0:self.gensayisix]
            kromozomy=self.xy_populasyon[i][self.gensayisix:len(self.xy_populasyon[0])] #bütün genler aynı boyutta herhangi birinin gen uzunluğu yeterli
            self.listbox2.insert(END,"V{} = {},{}".format(i+1,kromozomx,kromozomy))
            #değişkenler virgülsüz eski haline döndürüldü
            self.c_binaryx[i] = kromozomx
            self.c_binaryy[i] = kromozomy

        return self.c_binaryx,self.c_binaryy,self.xy_populasyon





    def mutasyon_ikili(self,mutasyon_kromozomx=[],mutasyon_kromozomy=[],mutasyon_degerlerixy=[]):
        self.mutasyon_kromozomx=mutasyon_kromozomx
        self.mutasyon_kromozomy=mutasyon_kromozomy
        self.mutasyon_degerlerixy =mutasyon_degerlerixy
        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"5.) Çaprazlama Sonucu Oluşan Populasyona Mutasyon uygulandı")
        self.listbox2.itemconfig(END,bg="red",fg="white")
        self.toplam_gen_sayisi = int(self.toplam_kromozom_gen) * self.popsize
        self.listbox2.insert(END,"Mutasyon ihtimali {} olarak belirlendi.".format(self.pm.get()))
        mutasyon_gen_sayisi = math.ceil(self.popsize * int(self.toplam_kromozom_gen) * float(self.pm.get()))
        self.listbox2.insert(END,"Mutasyona maruz kalması beklenen gen sayisi = {}".format(mutasyon_gen_sayisi))
        self.listbox2.itemconfig(END,bg="green",fg="white")

        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"[1-{}] aralığında rastgele {} adet tam sayi oluşturuldu".format(self.toplam_gen_sayisi,mutasyon_gen_sayisi))
        self.listbox2.itemconfig(END,bg="green",fg="white")
        self.mutasyon_random=[]
        self.mutasyon_random = sayi = random.sample(range(1,self.toplam_gen_sayisi),mutasyon_gen_sayisi)
        self.kromozom_number=[]
        self.gen_number=[]
        i=0
        for i in range(0,mutasyon_gen_sayisi):
            sayi =int(self.mutasyon_random[i])
            self.listbox2.insert(END,"R{} = {}".format(i+1,sayi))
            self.listbox2.itemconfig(END,bg="green",fg="white")
            gen = sayi%int(self.toplam_kromozom_gen)
            if(gen==0):
                gen=int(self.toplam_kromozom_gen)
                self.gen_number.append(gen)
            else:
                self.gen_number.append(sayi%int(self.toplam_kromozom_gen))
            self.kromozom_number.append(math.ceil(sayi/int(self.toplam_kromozom_gen)))
            self.listbox2.insert(END,"Gen ile ilgili kromozom => V{}= {}".format(self.kromozom_number[i],self.mutasyon_degerlerixy[self.kromozom_number[i]-1]))
            ilgili_kromozom =self.mutasyon_degerlerixy[self.kromozom_number[i]-1]
            ilgili_gen = ilgili_kromozom[self.gen_number[i]-1]
            yeni_gen=""
            if(ilgili_gen=="0"):
                yeni_gen="1"
            else:
                yeni_gen="0"

            yeni_kromozom =ilgili_kromozom[0:self.gen_number[i]-1] +yeni_gen+ ilgili_kromozom[self.gen_number[i]:len(ilgili_kromozom)]
            self.listbox2.insert(END,"Mutasyon Sonucu V{}' = {}".format(self.kromozom_number[i],yeni_kromozom))
            self.mutasyon_degerlerixy[self.kromozom_number[i]-1] = yeni_kromozom
            yeni_kromozom=""

        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"Mutasyon Sonucu Oluşan Son Populasyon:")
        self.listbox2.itemconfig(END,bg="blue",fg="white")
        # populasyon tekrar virgüllü hale çevriliyor
        self.m_binaryx=[]
        self.m_binaryy=[]
        i=0
        for i in range(0,len(self.mutasyon_degerlerixy)):
            kromozomx=self.mutasyon_degerlerixy[i][0:self.gensayisix]
            kromozomy=self.mutasyon_degerlerixy[i][self.gensayisix:len(self.mutasyon_degerlerixy[0])] #bütün genler aynı boyutta herhangi birinin gen uzunluğu yeterli
            self.listbox2.insert(END,"V{} = {},{}".format(i+1,kromozomx,kromozomy))
            #değişkenler virgülsüz eski haline döndürüldü
            self.m_binaryx.append(kromozomx)
            self.m_binaryy.append(kromozomy)

        return self.m_binaryx,self.m_binaryy,self.mutasyon_degerlerixy







    def mutasyon_duz(self):
        self.listbox2.insert(END,"Mutasyon ihtimali {} olarak belirlendi.".format(self.pm.get()))
        self.listbox2.itemconfig(END,bg="red",fg="white")
        gen_sayisi = self.popsize * int(self.m1.get())
        mutasyon_gen_sayisi = math.ceil(self.popsize * int(self.m1.get()) * float(self.pm.get()))
        self.listbox2.insert(END,"Mutasyona maruz kalması beklenen gen sayisi = {}".format(mutasyon_gen_sayisi))
        self.listbox2.itemconfig(END,bg="red",fg="white")

        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"[1-{}] aralığında rastgele {} adet tam sayi oluşturuldu".format(gen_sayisi,mutasyon_gen_sayisi))
        self.mutasyon_random=[]
        self.mutasyon_random = sayi = random.sample(range(1,gen_sayisi),mutasyon_gen_sayisi)
        self.kromozom_number=[]
        self.gen_number=[]
        i=0
        for i in range(0,mutasyon_gen_sayisi):
            sayi =int(self.mutasyon_random[i])
            self.listbox2.insert(END,"R{} = {}".format(i+1,sayi))
            gen = sayi%int(self.m1.get())
            if(gen==0):
                gen=int(self.m1.get())
                self.gen_number.append(gen)
            else:
                self.gen_number.append(sayi%int(self.m1.get()))

            self.kromozom_number.append(math.ceil(sayi/int(self.m1.get())))
            self.listbox2.insert(END,"Gen ile ilgili kromozom => V{}= {}".format(self.kromozom_number[i],self.mutasyon_populasyon[self.kromozom_number[i]-1]))
            ilgili_kromozom =self.mutasyon_populasyon[self.kromozom_number[i]-1]
            ilgili_gen = ilgili_kromozom[self.gen_number[i]-1]
            yeni_gen=""
            if(ilgili_gen=="0"):
                yeni_gen="1"
            else:
                yeni_gen="0"

            yeni_kromozom =ilgili_kromozom[0:self.gen_number[i]-1] +yeni_gen+ ilgili_kromozom[self.gen_number[i]:len(ilgili_kromozom)]
            self.listbox2.insert(END,"Mutasyon Sonucu V{}' = {}".format(self.kromozom_number[i],yeni_kromozom))
            self.mutasyon_populasyon[self.kromozom_number[i]-1] = yeni_kromozom

            yeni_kromozom=""

    def duz_caprazlama(self,):
        caprazlama_ihtimali = float(self.pc.get())
        c_k_s = self.popsize*caprazlama_ihtimali      #caprazlanacak kromozom sayisi
        if (c_k_s % 2 !=0):
            c_k_s = int(c_k_s)
            if(c_k_s % 2 !=0):
                c_k_s  = c_k_s + 1
        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"Caprazlama için parametreler:")
        self.listbox2.itemconfig(END,bg="red",fg="white")


        self.listbox2.insert(END,"pc(Çaprazlama İhtimali) = {}".format(caprazlama_ihtimali))
        self.listbox2.insert(END,"Pop_size x Pc (Çaprazlanacak Kromozom Sayisi = {}".format(c_k_s))
        self.caprazlama_populasyon = []
        for i in range (0,len(self.populasyon1binary)):
            self.caprazlama_populasyon.append(self.populasyon1binary[self.jenerasyon2_index[i]])

        self.listbox2.insert(END,"")
        self.listbox2.insert(END,"[1,{}] aralığında rastgele {} tane tamsayı üretildi".format(self.popsize,c_k_s))
        self.listbox2.itemconfig(END,bg="red",fg="white")
        i=0
        self.caprazlama_random=[]
        self.caprazlama_random = random.sample(range(1,self.popsize+1),c_k_s)   ##Birbirinden farklı rastgele sayılar üretiliyor
        y=0
        for y in range(0,len(self.caprazlama_random)):
            self.listbox2.insert(END,"r{} = {}".format(y+1,self.caprazlama_random[y]))
        self.listbox2.insert(END,"")



        while (i<len(self.caprazlama_random)):

            self.listbox2.insert(END,"v{} ile v{} çaprazlanacak".format(self.caprazlama_random[i],self.caprazlama_random[i+1]))
            self.listbox2.itemconfig(END,bg="red",fg="white")

            pos =random.randint(1,self.toplam_kromozom_gen-1)
            self.listbox2.insert(END,"Rastgele [1-{}] arasında pos belirlendi : {}".format(self.toplam_kromozom_gen-1,pos))

            self.listbox2.insert(END,"V{} = {}".format(self.caprazlama_random[i],self.caprazlama_populasyon[self.caprazlama_random[i]-1]))
            self.listbox2.insert(END,"V{} = {}".format(self.caprazlama_random[i+1],self.caprazlama_populasyon[self.caprazlama_random[i+1]-1]))
            gecici1_indeks =int( self.caprazlama_random[i]-1)
            gecici2_indeks =int(self.caprazlama_random[i+1]-1)
            gecici1 = self.caprazlama_populasyon[gecici1_indeks][pos:len(self.caprazlama_populasyon[gecici1_indeks])]
            gecici2 = self.caprazlama_populasyon[gecici2_indeks][pos:len(self.caprazlama_populasyon[gecici2_indeks])]
            change_binary=self.caprazlama_populasyon[self.caprazlama_random[i]-1]
            change_binary2 = self.caprazlama_populasyon[self.caprazlama_random[i+1]-1]
            change_binary_sonuc = change_binary[0:pos] + gecici2
            change_binary2_sonuc = change_binary2[0:pos] + gecici1
            self.listbox2.insert(END,"")
            self.listbox2.insert(END,"Çaprazlama İşlemi Tamamlandı")
            self.listbox2.insert(END,"v{0}={1}   =>   v{2}={3}".format(self.caprazlama_random[i],change_binary,self.caprazlama_random[i],change_binary_sonuc))
            self.listbox2.insert(END,"v{0}={1}   =>   v{2}={3}".format(self.caprazlama_random[i+1],change_binary2,self.caprazlama_random[i+1],change_binary2_sonuc))
            self.listbox2.insert(END,"")

            # Çaprazlama işlemi sonucunda populasyondaki değişen değerler güncellendi
            self.caprazlama_populasyon[self.caprazlama_random[i]-1] = change_binary_sonuc
            self.caprazlama_populasyon[self.caprazlama_random[i+1]-1] = change_binary2_sonuc

            i=i+2




if __name__ == '__main__':
    Algoritma()

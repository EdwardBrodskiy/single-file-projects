from tkinter import *


class romans:
    def __init__(self,root):
        self.m=0
        self.entry= Entry(root)
        self.entry.pack()
        button=Button(root, text='Decode')
        button.pack(fill=X)
        button.bind("<Button-1>", self.decode)
        
        #scrollbar = Scrollbar(root)
        #scrollbar.pack(side=RIGHT, fill=Y)
        self.listb= Listbox(root)
        self.listb.pack(fill=BOTH)
    def decode(self,event):
        self.listb.delete(0,END)
        
            
        alphabet_english=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                          "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                          "W", "X", "Y", "Z"]
        Try=1
        
        text=self.entry.get()
        self.entry.delete(0,END)
        numerical=text.upper()
        no=len(text)
        cnumerical=[]
        c=0
        while c<no:
            try:
                no_letter=alphabet_english.index(numerical[c])
                
                cnumerical.append(no_letter)
            except:
                cnumerical.append(numerical[c])
                
            c=c+1
        
        

        while Try<=26:
            c=0
            numerical=[]
            decoded=[]
            answer=[]
            while c<no:
                try:
                    changed = cnumerical[c]
                    changed = changed + Try  
                    decoded.append(changed)
                except:
                    decoded.append(cnumerical[c])
                    
                c=c+1
            c=0
            while c<no:
                try:
                    try:
                        final=alphabet_english[decoded[c]]
                        
                    except:
                        final=alphabet_english[decoded[c]-26]
                except:
                    final=decoded[c]
                    
                    
                answer.append(final)
                c=c+1
            c=0
            self.listb.insert(END,''.join(answer))
            
            Try=Try+1



            
        
        
        
        
        








root=Tk()
root.title("Decoding Romans")
qwerty= romans(root)
root.mainloop()

    

import Tkinter, tkFileDialog
def query_file(prompt='Choose an input file',
                types=[('All files','*'),('csv','*.csv'),('pkl','*.pkl')],
                defaultextension='*') :
    root = Tkinter.Tk()
    root.withdraw() # don't want a full GUI
    root.update()
    ffn_in = tkFileDialog.askopenfilename(parent=root,title=prompt,filetypes=types)
    return ffn_in

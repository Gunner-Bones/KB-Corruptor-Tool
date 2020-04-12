import pages
import tools.clientinput as ci
import tools.gdleveltools as glt
import winsound
import tkinter as tk


class TkView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(pages.PageTitle)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


def sound(name):
    if ci.is_win():
        winsound.PlaySound(glt.corePYIPath(name), winsound.SND_ALIAS | winsound.SND_ASYNC)


def rgb(tup):
    return "#%02x%02x%02x" % tup


# Unused
def loading(label, bl, prev):
    m_list = ['/', '-', '\\', '|']
    use = ''
    if prev == m_list[len(m_list) - 1]:
        use = m_list[0]
    else:
        use = m_list[m_list.index(prev) + 1]
    if bl:
        label.set('Loading... ' + use)
    else:
        label.grid_forget()
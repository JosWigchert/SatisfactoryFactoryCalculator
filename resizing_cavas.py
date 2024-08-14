from tkinter import *


class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)


def main():
    root = Tk()
    myframe = Frame(root)
    myframe.pack(fill=BOTH, expand=YES)
    mycanvas = ResizingCanvas(
        myframe, width=850, height=400, bg="red", highlightthickness=0
    )
    mycanvas.pack(fill=BOTH, expand=YES)

    # add some widgets to the canvas
    mycanvas.create_line(0, 0, 200, 100)
    mycanvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    mycanvas.create_rectangle(50, 25, 150, 75, fill="blue")

    # tag all of the drawn widgets
    mycanvas.addtag_all("all")
    root.mainloop()


if __name__ == "__main__":
    main()

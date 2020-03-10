import tkinter as tk

class GUI:
    def __init__(self, root):
        self.root = root
        root.title('Paintbot Scene Generator')

        main_frame = tk.Frame(root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        paint_frame = tk.LabelFrame(main_frame, text='Paints')
        paint_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=(0, 10))

        self.paints = tk.Variable()
        self.paint_listbox = tk.Listbox(paint_frame, listvariable=self.paints)
        self.paint_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_paint_frame = tk.Frame(paint_frame)
        add_paint_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=5, pady=(0, 5))

        self.paint_entry = tk.Entry(add_paint_frame)
        self.paint_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        add_paint_button = tk.Button(add_paint_frame, text='Add', command=self._add_paint)
        add_paint_button.pack(side=tk.RIGHT)

        ws_frame = tk.LabelFrame(main_frame, text='Wall Sections')
        ws_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

        self.wall_sections = tk.Variable()
        self.ws_listbox = tk.Listbox(ws_frame, listvariable=self.wall_sections)
        self.ws_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        gen_frame = tk.Frame(root)
        gen_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=(0, 10))

        gen_button = tk.Button(gen_frame, text='Generate', command=self._generate)
        gen_button.pack(side=tk.RIGHT)

    def _add_paint(self):
        paint = self.paint_entry.get().strip()
        if paint and paint not in self.paints.get():
            self.paint_listbox.insert(tk.END, paint)
        self.paint_entry.delete(0, tk.END)

    def _generate(self):
        pass

root = tk.Tk()
gui = GUI(root)
root.mainloop()

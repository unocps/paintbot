import tkinter as tk

class GUI:
    def __init__(self, root):
        self.ws = []

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

        self.ws_var = tk.Variable()
        self.ws_listbox = tk.Listbox(ws_frame, listvariable=self.ws_var)
        self.ws_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_ws_frame = tk.Frame(ws_frame)
        add_ws_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=5, pady=(0, 5))

        val_float = (ws_frame.register(self._val_float), '%P')

        label = tk.Label(add_ws_frame, text='Start (x, y):')
        label.grid(row=0, column=0, sticky='e')

        self.ws_start_x_entry = tk.Entry(add_ws_frame, width=5, validate='key', validatecommand=val_float)
        self.ws_start_x_entry.grid(row=0, column=1)

        self.ws_start_y_entry = tk.Entry(add_ws_frame, width=5, validate='key', validatecommand=val_float)
        self.ws_start_y_entry.grid(row=0, column=2)

        label = tk.Label(add_ws_frame, text='End (x, y):')
        label.grid(row=1, column=0, stick='e')

        self.ws_end_x_entry = tk.Entry(add_ws_frame, width=5, validate='key', validatecommand=val_float)
        self.ws_end_x_entry.grid(row=1, column=1)

        self.ws_end_y_entry = tk.Entry(add_ws_frame, width=5, validate='key', validatecommand=val_float)
        self.ws_end_y_entry.grid(row=1, column=2)

        label = tk.Label(add_ws_frame, text='Paint:', width=6)
        label.grid(row=2, column=0, sticky='e')

        self.ws_paint_var = tk.StringVar()
        self.ws_paint_option = tk.OptionMenu(add_ws_frame, self.ws_paint_var, [])
        self.ws_paint_option.grid(row=2, column=1, columnspan=2, sticky='ew')

        add_ws_button = tk.Button(add_ws_frame, text='Add', command=self._add_ws)
        add_ws_button.grid(row=1, column=3)

        gen_frame = tk.Frame(root)
        gen_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=(0, 10))

        gen_button = tk.Button(gen_frame, text='Generate', command=self._generate)
        gen_button.pack(side=tk.RIGHT)

    def _add_paint(self):
        paint = self.paint_entry.get().strip()
        if not paint or paint in self.paints.get():
            return

        self.paint_listbox.insert(tk.END, paint)
        paint_menu = self.ws_paint_option['menu']
        paint_menu.delete(0, tk.END)
        for p in self.paints.get():
            paint_menu.add_command(label=p, command=lambda v=p: self.ws_paint_var.set(v))
        self.paint_entry.delete(0, tk.END)

    def _add_ws(self):
        start_x = self.ws_start_x_entry.get().strip()
        start_y = self.ws_start_y_entry.get().strip()
        end_x = self.ws_end_x_entry.get().strip()
        end_y = self.ws_end_y_entry.get().strip()
        paint = self.ws_paint_var.get()
        if not start_x or not start_y or not end_x or not end_y or not paint:
            return

        self.ws_listbox.insert(tk.END, '{} - ({}, {}) to ({}, {})'.format(paint, start_x, start_y, end_x, end_y))
        self.ws.append(((start_x, start_y), (end_x, end_y), paint))

    def _generate(self):
        pass

    def _val_float(self, s):
        if not s:
            return True
        try:
            float(s)
            return True
        except:
            return False

root = tk.Tk()
gui = GUI(root)
root.mainloop()

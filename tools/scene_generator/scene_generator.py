import tkinter as tk

class GUI:
    def __init__(self, root):
        self.ws = []
        self.paints = []

        self.root = root
        root.title('Paintbot Scene Generator')

        main_frame = tk.Frame(root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        val_float = (main_frame.register(self._val_float), '%P')

        paint_frame = tk.LabelFrame(main_frame, text='Paints')
        paint_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=(0, 10))

        self.paint_listbox = tk.Listbox(paint_frame)
        self.paint_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_paint_frame = tk.Frame(paint_frame)
        add_paint_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=5, pady=(0, 5))

        label = tk.Label(add_paint_frame, text='Name:')
        label.grid(row=0, column=0, sticky='e')

        self.paint_name_entry = tk.Entry(add_paint_frame)
        self.paint_name_entry.grid(row=0, column=1, columnspan=2, sticky='ew')

        label = tk.Label(add_paint_frame, text='Tray (x, y):')
        label.grid(row=1, column=0, sticky='e')

        self.paint_x_entry = tk.Entry(add_paint_frame, width=5, validate='key', validatecommand=val_float)
        self.paint_x_entry.grid(row=1, column=1)

        self.paint_y_entry = tk.Entry(add_paint_frame, width=5, validate='key', validatecommand=val_float)
        self.paint_y_entry.grid(row=1, column=2)

        add_paint_button = tk.Button(add_paint_frame, text='Add', command=self._add_paint)
        add_paint_button.grid(row=1, column=3)

        ws_frame = tk.LabelFrame(main_frame, text='Wall Sections')
        ws_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

        self.ws_listbox = tk.Listbox(ws_frame)
        self.ws_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_ws_frame = tk.Frame(ws_frame)
        add_ws_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=5, pady=(0, 5))

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
        name = self.paint_name_entry.get().strip()
        x = self.paint_x_entry.get().strip()
        y = self.paint_y_entry.get().strip()
        if not name or not x or not y:
            return

        self.paints.append(((x, y), name))
        self.paint_listbox.insert(tk.END, '{} - Tray at ({}, {})'.format(name, x, y))

        # Update paint menu
        paint_menu = self.ws_paint_option['menu']
        paint_menu.delete(0, tk.END)
        for p in self.paints:
            paint_menu.add_command(label=p[1], command=lambda v=p: self.ws_paint_var.set(v[1]))

        # Clear fields
        self.paint_name_entry.delete(0, tk.END)
        self.paint_x_entry.delete(0, tk.END)
        self.paint_y_entry.delete(0, tk.END)

    def _add_ws(self):
        start_x = self.ws_start_x_entry.get().strip()
        start_y = self.ws_start_y_entry.get().strip()
        end_x = self.ws_end_x_entry.get().strip()
        end_y = self.ws_end_y_entry.get().strip()
        paint = self.ws_paint_var.get()
        if not start_x or not start_y or not end_x or not end_y or not paint:
            return

        self.ws.append(((start_x, start_y), (end_x, end_y), paint))
        self.ws_listbox.insert(tk.END, '{} - ({}, {}) to ({}, {})'.format(paint, start_x, start_y, end_x, end_y))

        # Clear fields
        self.ws_start_x_entry.delete(0, tk.END)
        self.ws_start_y_entry.delete(0, tk.END)
        self.ws_end_x_entry.delete(0, tk.END)
        self.ws_end_y_entry.delete(0, tk.END)
        self.ws_paint_var.set('')

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

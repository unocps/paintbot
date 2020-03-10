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

        self.wall_sections_var = tk.Variable()
        self.ws_listbox = tk.Listbox(ws_frame, listvariable=self.wall_sections_var)
        self.ws_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_ws_frame = tk.Frame(ws_frame)
        add_ws_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=5, pady=(0, 5))

        add_ws_start_frame = tk.Frame(add_ws_frame)
        add_ws_start_frame.pack(fill=tk.X)

        label = tk.Label(add_ws_start_frame, text='Start X:', width=6)
        label.pack(side=tk.LEFT)

        self.ws_start_x_entry = tk.Entry(add_ws_start_frame)
        self.ws_start_x_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        label = tk.Label(add_ws_start_frame, text='Start Y:', width=6)
        label.pack(side=tk.LEFT)

        self.ws_start_y_entry = tk.Entry(add_ws_start_frame)
        self.ws_start_y_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        add_ws_end_frame = tk.Frame(add_ws_frame)
        add_ws_end_frame.pack(fill=tk.X)

        label = tk.Label(add_ws_end_frame, text='End X:', width=6)
        label.pack(side=tk.LEFT)

        self.ws_end_x_entry = tk.Entry(add_ws_end_frame)
        self.ws_end_x_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        label = tk.Label(add_ws_end_frame, text='End Y:', width=6)
        label.pack(side=tk.LEFT)

        self.ws_end_y_entry = tk.Entry(add_ws_end_frame)
        self.ws_end_y_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        add_ws_paint_frame = tk.Frame(add_ws_frame)
        add_ws_paint_frame.pack(fill=tk.X)

        label = tk.Label(add_ws_paint_frame, text='Paint:', width=6)
        label.pack(side=tk.LEFT)

        self.ws_paint_var = tk.StringVar()
        self.ws_paint_option = tk.OptionMenu(add_ws_paint_frame, self.ws_paint_var, [])
        self.ws_paint_option.pack(fill=tk.X)

        gen_frame = tk.Frame(root)
        gen_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=(0, 10))

        gen_button = tk.Button(gen_frame, text='Generate', command=self._generate)
        gen_button.pack(side=tk.RIGHT)

    def _add_paint(self):
        paint = self.paint_entry.get().strip()
        if paint and paint not in self.paints.get():
            self.paint_listbox.insert(tk.END, paint)

            paint_menu = self.ws_paint_option['menu']
            paint_menu.delete(0, tk.END)
            for p in self.paints.get():
                paint_menu.add_command(label=p, command=lambda v=p: self.ws_paint_var.set(v))
        self.paint_entry.delete(0, tk.END)

    def _generate(self):
        pass

root = tk.Tk()
gui = GUI(root)
root.mainloop()

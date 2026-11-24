
from PIL import Image
from PIL import ImageTk
from tkinter import ttk

import os

from analysis_engine import (
    run_analysis
)

import tkinter as tk

from tkinter import (
    filedialog,
    messagebox
)


class GIWAXSGUI:

    def __init__(
        self,
        root
    ):

        self.root = root

        self.root.title(
            "GIWAXS Analyzer v1.0"
        )

        self.root.state(
            "zoomed"
        )

        self.root.geometry(
            "1500x800"
        )

        self.filename = ""

        self.left_frame = tk.Frame(
            self.root
        )

        self.left_frame.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=10,
            pady=10
        )

        self.right_frame = tk.Frame(
            self.root
        )

        self.right_frame.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        self.create_widgets()

        self.result_text = tk.Text(
            self.left_frame,
            height=8,
            width=60
        )

        self.result_text.pack(
            pady=10
        )

        self.notebook = ttk.Notebook(
            self.right_frame
        )

        self.notebook.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.fit_tab = tk.Frame(
            self.notebook
        )

        self.component_tab = tk.Frame(
            self.notebook
        )

        self.residual_tab = tk.Frame(
            self.notebook
        )   

        self.area_tab = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.fit_tab,
            text="Peak Fit"
        )

        self.notebook.add(
            self.component_tab,
            text="Components"
        )

        self.notebook.add(
            self.residual_tab,
            text="Residual"
        )

        self.notebook.add(
            self.area_tab,
            text="Area Distribution"
        )

        self.fit_label = tk.Label(
            self.fit_tab
        )

        self.fit_label.pack()

        self.component_label = tk.Label(
            self.component_tab
        )

        self.component_label.pack()

        self.residual_label = tk.Label(
            self.residual_tab
        )

        self.residual_label.pack()

        self.area_label = tk.Label(
            self.area_tab
        )

        self.area_label.pack()              

        self.table = ttk.Treeview(

            self.left_frame,

            columns=(
                "Peak",
                "Q",
                "d",
                "Area%"
            ),

            show="headings",

            height=8

        )

        self.table.heading(
            "Peak",
            text="Peak"
        )

        self.table.heading(
            "Q",
            text="Q"
        )

        self.table.heading(
            "d",
            text="d"
        )

        self.table.heading(
            "Area%",
            text="Area %"
        )

        self.table.pack(
            pady=10
        )

        self.table.column(
            "Peak",
            width=60,
            anchor="center"
        )

        self.table.column(
            "Q",
            width=100,
            anchor="center"
        )

        self.table.column(
            "d",
            width=100,
            anchor="center"
        )

        self.table.column(
            "Area%",
            width=100,
            anchor="center"
        )                   

    def display_plots(self):

        plot_map = {

            "Peak_Fit.png":
                self.fit_label,

            "Peak_Components.png":
                self.component_label,

            "Residual.png":
                self.residual_label,

            "Area_Distribution.png":
                self.area_label

        }

        for filename, label in plot_map.items():

            try:

                image = Image.open(

                    os.path.join(
                        "..",
                        "output",
                        filename
                    )

                )

                image.thumbnail(
                    (800, 500)
                )

                photo = ImageTk.PhotoImage(
                    image
                )

                label.image = photo

                label.config(
                    image=photo
                )

            except Exception as e:

                print(e)


    def create_widgets(self):

        tk.Label(
            self.left_frame,
            text="Q min"
        ).pack()

        self.q_min_var = tk.StringVar(
            value="0.18"
        )

        tk.Entry(
            self.left_frame,
            textvariable=self.q_min_var,
            width=10
        ).pack(
            pady=5
        )

        tk.Label(
            self.left_frame,
            text="Smooth Scale"
        ).pack()

        self.smooth_var = tk.StringVar()

        self.smooth_box = ttk.Combobox(

            self.left_frame,

            textvariable=self.smooth_var,

            width=12

        )

        self.smooth_box["values"] = (

            "1e4",
            "3e4",
            "5e4",
            "1e5",
            "3e5"

        )

        self.smooth_box.set(
            "5e4"
        )

        self.smooth_box.pack(
            pady=5
        )

        tk.Label(
            self.left_frame,
            text="SNIP Window"
        ).pack()

        self.window_var = tk.StringVar()

        self.window_box = ttk.Combobox(

            self.left_frame,

            textvariable=self.window_var,

            width=10,

            state="readonly"

        )

        self.window_box["values"] = (

            "20",
            "40",
            "60",
            "80",
            "100"

        )

        self.window_box.set(
            "40"
        )

        self.window_box.pack(
            pady=5
        )


        self.select_button =tk.Button(

            self.left_frame,

            text="Select Data File",

            width=30,

            command=self.select_file

        )

        self.select_button.pack(
            pady=15
        )

        self.file_label = tk.Label(

            self.left_frame,

            text="No file selected"

        )

        self.file_label.pack()

        self.run_button = tk.Button(

            self.left_frame,

            text="Run Analysis",

            width=30,

            command=self.run_analysis

        )

        self.run_button.pack(
            pady=15
        )

        self.open_button = tk.Button(

            self.left_frame,

            text="Open Output Folder",

            width=30,

            command=self.open_output

        )

        self.open_button.pack(
            pady=15
        )

    def select_file(self):

        self.filename = filedialog.askopenfilename()

        self.file_label.config(
            text=os.path.basename(
                self.filename
            )
        )

    def update_log(
        self,
        message
    ):

        self.result_text.insert(
            tk.END,
            message + "\n"
        )

        self.result_text.see(
            tk.END
        )

        self.root.update()   

    def run_analysis(self):

        if self.filename == "":

            messagebox.showerror(
                "Error",
                "Select a file first"
            )

            return

        self.run_button.config(
            state="disabled"
        )

        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.result_text.insert(
            tk.END,
            "Running analysis...\n"
        )

        self.root.update()

        try:

            q_min = float(
                self.q_min_var.get()
            )

            smooth_scale = float(
                self.smooth_var.get()
            )

            window = int(
                self.window_var.get()
            )

            result = run_analysis(

                self.filename,

                q_min=q_min,

                window=window,

                smooth_scale=smooth_scale,

                log_callback=self.update_log

            )

            self.result_text.insert(

                tk.END,

                "\n\n"
                "====================\n"
                "Analysis Summary\n"
                "====================\n\n"

                f"Detected Peaks : {result['num_peaks']}\n\n"

                f"R² : {result['r2']:.6f}\n"

                f"Chi² : {result['chi2']:.2f}\n"

                f"Reduced Chi² : {result['reduced_chi2']:.2f}\n"

                f"Q min : {q_min}\n"

                f"SNIP Window : {window}\n"

                f"Smooth Scale : {smooth_scale:.0f}\n"

            )

            self.root.update()

            self.display_plots()

            for row in self.table.get_children():

                self.table.delete(row)

            for _, row in result[
                "peak_table"
            ].iterrows():

                self.table.insert(

                    "",

                    tk.END,

                    values=(

                        int(row["Peak"]),

                        f"{row['Q']:.4f}",

                        f"{row['d']:.3f}",

                        f"{row['Area_Percent']:.2f}"

                    )

                )

        except Exception as e:

            messagebox.showerror(
                "Analysis Error",
                str(e)
            )

        finally:

            self.run_button.config(
                state="normal"
            )                        

    def open_output(self):

        import os

        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        output_path = os.path.join(
            current_dir,
            "..",
            "output"
        )

        output_path = os.path.abspath(
            output_path
        )

        try:

            if not os.path.exists(output_path):

                messagebox.showerror(
                    "Error",
                    f"Output folder not found:\n{output_path}"
                )

                return

            os.startfile(
                output_path
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

root = tk.Tk()

GIWAXSGUI(root)

root.mainloop()
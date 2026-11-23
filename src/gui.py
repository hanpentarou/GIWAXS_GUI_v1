
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

        tk.Button(

            self.left_frame,

            text="Select Data File",

            width=30,

            command=self.select_file

        ).pack(pady=15)

        self.file_label = tk.Label(

            self.left_frame,

            text="No file selected"

        )

        self.file_label.pack()

        tk.Button(

            self.left_frame,

            text="Run Analysis",

            width=30,

            command=self.run_analysis

        ).pack(pady=15)

        tk.Button(

            self.left_frame,

            text="Open Output Folder",

            width=30,

            command=self.open_output

        ).pack(
            pady=15
        )

    def select_file(self):

        self.filename = filedialog.askopenfilename()

        self.file_label.config(
            text=os.path.basename(
                self.filename
            )
        )

    def run_analysis(self):

        if self.filename == "":

            messagebox.showerror(
                "Error",
                "Select a file first"
            )

            return

        try:

            result = run_analysis(
                self.filename
            )

            self.result_text.delete(
                "1.0",
                tk.END
            )

            self.result_text.insert(

                tk.END,

                "Analysis Summary\n"
                "====================\n\n"

                f"Detected Peaks : {result['num_peaks']}\n\n"

                f"R² : {result['r2']:.6f}\n"

                f"Chi² : {result['chi2']:.2f}\n"

                f"Reduced Chi² : {result['reduced_chi2']:.2f}\n"

            )

            self.display_plots()

        except Exception as e:

            messagebox.showerror(
                "Analysis Error",
                str(e)
            )

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
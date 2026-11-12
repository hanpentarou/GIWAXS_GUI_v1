
from PIL import Image
from PIL import ImageTk

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
            "GIWAXS Analyzer"
        )

        self.root.geometry(
            "1200x800"
        )

        self.filename = ""

        self.create_widgets()

        self.result_text = tk.Text(
            self.root,
            height=8,
            width=60
        )

        self.result_text.pack(
            pady=10
        )

        self.image_label = tk.Label(
            self.root
        )

        self.image_label.pack(
            pady=10
        )

    def create_widgets(self):

        tk.Button(

            self.root,

            text="Select Data File",

            width=30,

            command=self.select_file

        ).pack(pady=15)

        self.file_label = tk.Label(

            self.root,

            text="No file selected"

        )

        self.file_label.pack()

        tk.Button(

            self.root,

            text="Run Analysis",

            width=30,

            command=self.run_analysis

        ).pack(pady=15)

        tk.Button(

            self.root,

            text="Open Output Folder",

            width=30,

            command=self.open_output

        ).pack(
            pady=15
        )

    def select_file(self):

        self.filename = filedialog.askopenfilename()

        self.file_label.config(
            text=self.filename
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

            self.display_fit_plot()

        except Exception as e:

            messagebox.showerror(
                "Analysis Error",
                str(e)
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

    def display_fit_plot(self):

        try:

            image = Image.open(
                "../output/Peak_Fit.png"
            )

            image.thumbnail(
                (900, 500)
            )

            self.photo = ImageTk.PhotoImage(
                image
            )

            self.image_label.config(
                image=self.photo
            )

        except Exception as e:

            print(e)


root = tk.Tk()

GIWAXSGUI(root)

root.mainloop()
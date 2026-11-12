
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
            "600x300"
        )

        self.filename = ""

        self.create_widgets()

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

            messagebox.showinfo(

                "Analysis Complete",

                f"R² = {result['r2']:.6f}\n"
                f"Chi² = {result['chi2']:.2f}\n"
                f"Reduced Chi² = {result['reduced_chi2']:.2f}"

            )

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
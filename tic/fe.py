import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import subprocess
from tkinterdnd2 import DND_FILES, TkinterDnD

class TumorControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tumor Motion Control")
        #self.root.geometry("600x400")
        self.root.minsize(800, 800)
        self.root.minsize(800, 800)
        self.style = tb.Style("darkly")
        
        self.stage = 1
        self.num_tumors = tk.IntVar(value=1)
        self.tumor_data = None
        self.button = None
        self.warning = None
        self.stage_2_frame = None
        self.create_stage_1()
    
    def create_stage_1(self):
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Select Number of Tumors:", font=("Segoe UI", 16)).pack(pady=20)
        
        ttk.Radiobutton(frame, text="One Tumor", variable=self.num_tumors, value=1, style="info.Toolbutton").pack(pady=10)
        ttk.Radiobutton(frame, text="Two Tumors", variable=self.num_tumors, value=2, style="info.Toolbutton").pack(pady=10)
        
        ttk.Button(frame, text="Next", command=self.create_stage_2, style="success.Tbutton").pack(pady=50)

    def create_stage_2(self):
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Enter Tumor Details:", font=("Segoe UI", 12)).pack(pady=10)

        if self.tumor_data == None:
            self.tumor_data = [{} for _ in range(self.num_tumors.get())]
        if len(self.tumor_data) < self.num_tumors.get():
            self.tumor_data.append({})

        file_entry = [None, None]
        for i in range(self.num_tumors.get()):
            tumor_frame = ttk.LabelFrame(frame, text=f"Tumor {i+1}", padding=10)
            tumor_frame.pack(fill="x", pady=5)

            # Starting Position
            ttk.Label(tumor_frame, text="Starting Position (X, Y, Z):").pack(anchor="w")
            entry_x = ttk.Entry(tumor_frame, width=10)
            entry_y = ttk.Entry(tumor_frame, width=10)
            entry_z = ttk.Entry(tumor_frame, width=10)

            entry_x.pack(side="left", padx=5)
            entry_y.pack(side="left", padx=5)
            entry_z.pack(side="left", padx=5)

            # File Selection Label
            ttk.Label(tumor_frame, text="Select Input File or Drag & Drop:").pack(anchor="w", pady=5)
            self.tumor_data[i]["file"] = None
            # Drag and Drop Area
            file_entry[i] = tk.Entry(tumor_frame, width=40,)
            file_entry[i].pack(pady=5)

            def on_drop(event, index=i):
                file_path = event.data.strip().replace("{", "").replace("}", "")  # Remove curly braces
                file_entry[index].delete(0, tk.END)
                file_entry[index].insert(0, file_path)
                self.tumor_data[index]["file"] = file_path

            # Register drag-and-drop
            file_entry[i].drop_target_register(DND_FILES)
            file_entry[i].dnd_bind("<<Drop>>", lambda e, idx=i: on_drop(e, idx))

            # Browse Button
            def browse_file(index=i):
                file_path = filedialog.askopenfilename()
                if file_path:
                    file_entry[index].delete(0, tk.END)
                    file_entry[index].insert(0, file_path)
                    self.tumor_data[index]["file"] = file_path

            browse_button = ttk.Button(tumor_frame, text="Browse", command=lambda i=i: browse_file(i))
            browse_button.pack(pady=5)

            self.tumor_data[i]["entries"] = (entry_x, entry_y, entry_z)

        ttk.Button(frame, style= "danger.Tbutton", text="Back", command=self.create_stage_1).pack(side="left", padx=10, pady=20)
        ttk.Button(frame, style= "success.Tbutton", text="Next", command=self.transistion_2_to_3).pack(side="right", padx=10, pady=20)
        self.stage_2_frame = frame 

    def transistion_2_to_3(self):
        all_entries_done = True
        
        for j in range(self.num_tumors.get()):
            if self.tumor_data[j]["file"] == None:
                all_entries_done = False
                if self.warning != None:
                    self.warning.destroy()
                self.warning = ttk.Label(self.stage_2_frame, text="Please provide a file path", style='warning.Inverse.TLabel')
                self.warning.pack(side="bottom", padx=10, pady=20)
                break
            for entry in self.tumor_data[j]["entries"]:
                if (entry.get() == ""):
                    all_entries_done = False
                    if self.warning != None:
                        self.warning.destroy()
                    self.warning = ttk.Label(self.stage_2_frame, text="Please provide all entries", style='warning.Inverse.TLabel')
                    self.warning.pack(side="bottom", padx=10, pady=20)
                    break
            if not all_entries_done: break
        
        if all_entries_done: self.create_stage_3()

    def create_stage_3(self):
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Start Tumor Motion Control", font=("Segoe UI", 12)).pack(pady=10)
        
        self.status_labels = []
        for i in range(self.num_tumors.get()):
            status_label = ttk.Label(frame, text=f"Tumor {i+1}: Waiting...", bootstyle="info")
            status_label.pack()
            self.status_labels.append(status_label)
        
        self.button = ttk.Button(frame, text="Back", command=self.create_stage_2, style="danger.TButton")
        self.button.pack(side="left", padx=10, pady=20)
        ttk.Button(frame, text="Start", command=self.start_control, style="success.TButton").pack(side="right", padx=10, pady=20)
    
    def load_file(self, index):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.tumor_data[index]["file"] = file_path
    
    def start_control(self):
        self.button.config(state=tk.DISABLED)
        for i, tumor in enumerate(self.tumor_data):
            x, y, z = [entry.get() for entry in tumor["entries"]]
            input_file = tumor["file"]
            if input_file:
                subprocess.Popen(["./tumor_control", x, y, z, input_file])
                self.status_labels[i]["text"] = f"Tumor {i+1}: Running..."
                self.status_labels[i]["bootstyle"] = "warning"
        self.create_stage_3()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = TumorControlApp(root)
    root.mainloop()

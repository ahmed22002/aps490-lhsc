import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import subprocess
from tkinterdnd2 import DND_FILES, TkinterDnD
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import subprocess
import sys

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
        self.tumor_file = None
        self.tumor_one_grid_pos = None
        self.back_button = None
        self.warning = None
        self.stage_2_frame = None
        self.stop_button = None
        self.actuator_process = None
        self.instructions()
    
    def instructions(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Tumor Motion Control", font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Simulating Realistic Tumor Motion for Radiotherapy Research", font=("Segoe UI", 12, "italic")).pack(pady=20)
        
        #ttk.Label(frame, text=" ", font=("Segoe UI", 16, "bold")).pack(pady=20)

        intro = "Welcome to Tumor Motion Control, an application designed to accurately simulate the motion of lung tumors for research and treatment planning. \nThis tool allows users to input tumor positions, select breathing waveforms, and visualize motion paths before execution."
        ttk.Label(frame, text=intro, font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        ttk.Label(frame, text="Use this app to:", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        ttk.Label(frame, text="\t - Define tumor positions based on CT scan data", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        ttk.Label(frame, text="\t - Upload and apply custom breathing waveforms", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        ttk.Label(frame, text="\t - Calculate tumor orientation (angles at which they should be setup) for precise motion replication", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        ttk.Label(frame, text="\t - Simulate motion in a 3D environment to verify accuracy before actuation", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        
        ttk.Label(frame, text=" ", font=("Segoe UI", 5)).pack(pady=20)
        ttk.Label(frame, text="Click \"Get Started\" to begin setting up your simulation.", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        ttk.Button(frame, text="Get Started", command=self.create_stage_1, style="primary.Tbutton").pack(pady=50)

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
        ttk.Label(frame, text="- Enter the starting and ending position for both tumors based on the CT scan.\n- Upload the breathing waveform you want to simulate.\n- Chose a postion for tumor one on the grid and input it.\n  (This will be used to calculate the position tumor two should be placed on the grid)", font=("Segoe UI", 10)).pack(pady=10)
        if self.tumor_data is None:
            self.tumor_data = [{} for _ in range(self.num_tumors.get())]
        if len(self.tumor_data) < self.num_tumors.get():
            self.tumor_data.append({})

        file_entry = None

        for i in range(self.num_tumors.get()):
            tumor_frame = ttk.LabelFrame(frame, text=f"Tumor {i+1}", padding=10)
            tumor_frame.pack(fill="x", pady=5)

            tumor_grid = ttk.Frame(tumor_frame)
            tumor_grid.pack()

            # Starting Position Label
            ttk.Label(tumor_grid, text="Starting Position (X, Y, Z) from CT scan:").grid(row=0, column=0, columnspan=3, sticky="w", pady=2)

            # Starting Position Entries
            entry_x = ttk.Entry(tumor_grid, width=10)
            entry_y = ttk.Entry(tumor_grid, width=10)
            entry_z = ttk.Entry(tumor_grid, width=10)
            entry_x.grid(row=1, column=0, padx=5)
            entry_y.grid(row=1, column=1, padx=5)
            entry_z.grid(row=1, column=2, padx=5)

            # Ending Position Label (Now Directly Below)
            ttk.Label(tumor_grid, text="Ending Position (X, Y, Z) from CT scan:").grid(row=2, column=0, columnspan=3, sticky="w", pady=5)

            # Ending Position Entries (Placed Directly Below Start Position)
            end_x = ttk.Entry(tumor_grid, width=10)
            end_y = ttk.Entry(tumor_grid, width=10)
            end_z = ttk.Entry(tumor_grid, width=10)
            end_x.grid(row=3, column=0, padx=5)
            end_y.grid(row=3, column=1, padx=5)
            end_z.grid(row=3, column=2, padx=5)

            # Store entries
            self.tumor_data[i]["entries"] = (entry_x, entry_y, entry_z)
            self.tumor_data[i]["end_entries"] = (end_x, end_y, end_z)

            if (i == 0):
                ttk.Label(tumor_grid, text="Tumor one's position on the grid:").grid(row=4, column=0, columnspan=3, sticky="w", pady=5)
                self.tumor_one_grid_pos = ttk.Entry(tumor_grid, width=10)
                self.tumor_one_grid_pos.grid(row=5)


        # File Selection
        tumor_frame = ttk.LabelFrame(frame, text="Breathing Waveform", padding=10)
        tumor_frame.pack(fill="x", pady=5)
        ttk.Label(tumor_frame, text="Select Breathing Waveform File or Drag & Drop:").pack(anchor="w", pady=5)
        file_entry = tk.Entry(tumor_frame, width=40)
        file_entry.pack(pady=5)

        def on_drop(event, index=i):
            file_path = event.data.strip().replace("{", "").replace("}", "")  # Remove curly braces
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)
            self.tumor_file = file_path

        file_entry.drop_target_register(DND_FILES)
        file_entry.dnd_bind("<<Drop>>", lambda e, idx=i: on_drop(e, idx))

        def browse_file(index=i):
            file_path = filedialog.askopenfilename()
            if file_path:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, file_path)
                self.tumor_file = file_path

        browse_button = ttk.Button(tumor_frame, text="Browse", command=lambda i=i: browse_file(i))
        browse_button.pack(pady=5)
        
        ttk.Button(frame, style="danger.Tbutton", text="Back", command=self.create_stage_1).pack(side="left", padx=10, pady=20)
        ttk.Button(frame, style="success.Tbutton", text="Next", command=self.transistion_2_to_3).pack(side="right", padx=10, pady=20)
        self.stage_2_frame = frame



    def transistion_2_to_3(self):
        all_entries_done = True
        
        for j in range(self.num_tumors.get()):
            if self.tumor_file == None:
                all_entries_done = False
                if self.warning != None:
                    self.warning.destroy()
                self.warning = ttk.Label(self.stage_2_frame, text="Please provide a file path", style='warning.Inverse.TLabel')
                self.warning.pack(side="bottom", padx=10, pady=20)
                break
            
            if self.tumor_one_grid_pos == None:
                all_entries_done = False
                if self.warning != None:
                    self.warning.destroy()
                self.warning = ttk.Label(self.stage_2_frame, text="Please provide the grid position for tumor one", style='warning.Inverse.TLabel')
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

            for entry in self.tumor_data[j]["end_entries"]:
                if (entry.get() == ""):
                    all_entries_done = False
                    if self.warning != None:
                        self.warning.destroy()
                    self.warning = ttk.Label(self.stage_2_frame, text="Please provide all entries", style='warning.Inverse.TLabel')
                    self.warning.pack(side="bottom", padx=10, pady=20)
                    break
            if not all_entries_done: break
            x, y, z = [entry.get() for entry in self.tumor_data[j]["entries"]]
            self.tumor_data[j]["entries"] = (int(x), int(y), int(z))
            x, y, z = [entry.get() for entry in self.tumor_data[j]["end_entries"]]
            self.tumor_data[j]["end_entries"] = (int(x), int(y), int(z))
        #print(self.tumor_data)
        self.tumor_one_grid_pos = self.tumor_one_grid_pos.get()
        #print(self.tumor_one_grid_pos)
        if all_entries_done: self.create_stage_3()

    def create_stage_3(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Setup for Tumor One", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        # if self.num_tumors.get() == 1:
        #     steps = [
        #         "Step 1: Set the height of tumor one to " + self.tumor_data[0]["entries"][2],
        #         "Step 2: [Add details here]",
        #         "Step 3: [Add details here]",
        #         "Step 4: [Add details here]"
        #     ]
        # else:
        #     steps = [
        #         "Step 1: Set the height of tumor one to " + self.tumor_data[0]["entries"][2] + \
        #             " and tumor two to " + self.tumor_data[1]["entries"][2],
        #         "Step 2: [Add details here]",
        #         "Step 3: [Add details here]",
        #         "Step 4: [Add details here]"
        #     ]
        steps = [
                "Set the rotation around the z-axis to 45° using the angle system labeled on the base of the holding mechanism",
                "Set the vertical rotation to 45° where 90° is the syringe upright and 0° is the syringe laying flat.",
                "Place tumor one in grid location A3 where the zero degree rotation mark should face the top of the grid.",
        ]

        for i, step in enumerate(steps, start=1):
            ttk.Label(frame, text=f"{i}. {step}", font=("Segoe UI", 12)).pack(anchor="w", pady=5)

        ttk.Label(frame, text=" ", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        tk.Label(frame, text=" ", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Setup for Tumor Two", font=("Segoe UI", 16, "bold")).pack(pady=10)

        steps = [
                "Set the rotation around the z-axis to 0° using the angle system labeled on the base of the holding mechanism",
                "Set the vertical rotation to 60° where 90° is the syringe upright and 0° is the syringe laying flat.",
                "Place tumor two in grid location D4 where the zero degree rotation mark should face the top of the grid.",
        ]

        for i, step in enumerate(steps, start=1):
            ttk.Label(frame, text=f"{i}. {step}", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        tk.Label(frame, text=" ", font=("Segoe UI", 16, "bold")).pack(pady=10)
        # Navigation Buttons
        ttk.Button(frame, style="danger.Tbutton", text="Back", command=self.create_stage_2).pack(side="left", padx=10, pady=20)
        ttk.Button(frame, style="success.Tbutton", text="Next", command=self.create_stage_4).pack(side="right", padx=10, pady=20)
    
    def create_stage_4(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Simulation for the two tumors on a 3D plot", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        instructions = "Click on the SHOW SIMULATION button to see the two tumors interacting in 3D.\nIf you are satisfied with your inputs click Next.\nOtherwise click Back to go to the previous stage and change your inputs."

        ttk.Label(frame, text=instructions, font=("Segoe UI", 12)).pack(anchor="w", pady=5)

        ttk.Button(frame, style="info.Tbutton", text="SHOW SIMULATION", command=self.show_plot).pack(anchor="w", pady=5)

        # Navigation Buttons
        ttk.Button(frame, style="danger.Tbutton", text="Back", command=self.create_stage_3).pack(side="left", padx=10, pady=20)
        ttk.Button(frame, style="success.Tbutton", text="Next", command=self.create_stage_5).pack(side="right", padx=10, pady=20)

    def show_plot(self):
        """
        Animate the movement of two actuators from given start to end positions in an oscillating motion.
        """
        Ax, Ay, Az = self.tumor_data[0]["entries"]
        Bx, By, Bz = self.tumor_data[0]["end_entries"]
        Cx, Cy, Cz = self.tumor_data[1]["entries"]
        Dx, Dy, Dz = self.tumor_data[1]["end_entries"]

        print(type(Ax), type(Dz))

        stepsize = 0.01
        max_step = 1
        increments = np.concatenate((np.linspace(0, max_step, int(max_step / stepsize)), np.linspace(max_step, 0, int(max_step / stepsize))))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(min(Ax, Bx, Cx, Dx) - 1, max(Ax, Bx, Cx, Dx) + 1)
        ax.set_ylim(min(Ay, By, Cy, Dy) - 1, max(Ay, By, Cy, Dy) + 1)
        ax.set_zlim(min(Az, Bz, Cz, Dz) - 1, max(Az, Bz, Cz, Dz) + 1)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        actuator1, = ax.plot([], [], [], 'ro', markersize=8)
        actuator2, = ax.plot([], [], [], 'bo', markersize=8)
        
        # Plot the dotted lines showing the actuator paths
        ax.plot([Ax, Bx], [Ay, By], [Az, Bz], 'r--', alpha=0.5)
        ax.plot([Cx, Dx], [Cy, Dy], [Cz, Dz], 'b--', alpha=0.5)
        
        def update(frame):
            t = increments[frame]
            T1x = Ax + (Bx - Ax) * t
            T1y = Ay + (By - Ay) * t
            T1z = Az + (Bz - Az) * t
            T2x = Cx + (Dx - Cx) * t
            T2y = Cy + (Dy - Cy) * t
            T2z = Cz + (Dz - Cz) * t
            actuator1.set_data([T1x], [T1y])
            actuator1.set_3d_properties(T1z)
            actuator2.set_data([T2x], [T2y])
            actuator2.set_3d_properties(T2z)
            return actuator1, actuator2
        
        ani = animation.FuncAnimation(fig, update, frames=len(increments), interval=10, blit=False)
        plt.show()


    def create_stage_5(self):
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Start Tumor Motion Control", font=("Segoe UI", 12)).pack(pady=10)
        
        self.status_labels = []
        for i in range(self.num_tumors.get()):
            status_label = ttk.Label(frame, text=f"Tumor {i+1}: Waiting...", bootstyle="info")
            status_label.pack()
            self.status_labels.append(status_label)
        
        self.back_button = ttk.Button(frame, text="Back", command=self.create_stage_3, style="danger.TButton")
        self.back_button.pack(side="left", padx=10, pady=20)
        self.stop_button = ttk.Button(frame, text="Stop", command=self.stop_control, style="primary.TButton")
        self.stop_button.pack(side="left", padx=10, pady=20)
        self.stop_button.config(state=tk.DISABLED)
        ttk.Button(frame, text="Start", command=self.start_control, style="success.TButton").pack(side="right", padx=10, pady=20)
    
    def load_file(self, index):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.tumor_data[index]["file"] = file_path
    
    def start_control(self):
        self.back_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        # for i, tumor in enumerate(self.tumor_data):
        #     x, y, z = [entry.get() for entry in tumor["entries"]]
        #     input_file = tumor["file"]
        #     if input_file:
        #         subprocess.Popen(["./tumor_control", x, y, z, input_file])
        #         self.status_labels[i]["text"] = f"Tumor {i+1}: Running..."
        #         self.status_labels[i]["bootstyle"] = "warning"
        if (self.actuator_process == None):
            self.actuator_process = subprocess.Popen("./actuator_run.exe")
        #self.create_stage_3()
    
    def stop_control(self):
        subprocess.Popen('powershell.exe -ExecutionPolicy RemoteSigned -file "cleanup.ps1"', stdout=sys.stdout)
        self.actuator_process = None
        self.stop_button.config(state=tk.DISABLED)
        self.back_button.config(state=tk.NORMAL)
        

    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # def calculate_angle(self, start_point, end_point):
    #     v = np.subtract(end_point, start_point)
    #     v_mag = np.sqrt(v[0]**2+)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = TumorControlApp(root)
    root.mainloop()

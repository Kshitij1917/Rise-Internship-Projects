
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from scanner import scan_wifi
from utils import export_to_csv, notify_new_networks

class WifiScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Network Scanner")
        self.root.geometry("700x500")
        self.root.configure(bg="#2b2b2b")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#3c3f41", foreground="white", rowheight=25, fieldbackground="#3c3f41")
        style.configure("Treeview.Heading", background="#2b2b2b", foreground="white")

        tk.Label(root, text="📶 Available Wi-Fi Networks", font=("Arial", 16), fg="white", bg="#2b2b2b").pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("SSID", "Signal", "Channel", "Security"), show="headings")
        for col in ("SSID", "Signal", "Channel", "Security"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        self.tree.pack(padx=10, pady=10, expand=True, fill="both")

        btn_frame = tk.Frame(root, bg="#2b2b2b")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔄 Refresh", command=self.load_networks, bg="#4caf50", fg="white", padx=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="⬇️ Export to CSV", command=self.export_csv, bg="#2196f3", fg="white", padx=10).pack(side="left", padx=10)

        self.networks = []
        self.load_networks()

        self.root.after(300000, self.auto_refresh)

    def load_networks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            current_scan = scan_wifi()
            current_ssids = {net["SSID"] for net in current_scan}
            previous_ssids = {net["SSID"] for net in self.networks}

            new_networks = [net for net in current_scan if net["SSID"] not in previous_ssids]
            self.networks = current_scan

            for net in self.networks:
                self.tree.insert("", "end", values=(net["SSID"], net["Signal"], net["Channel"], net["Security"]))

            if new_networks:
                notify_new_networks(new_networks)

        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {e}")

    def auto_refresh(self):
        self.load_networks()
        self.root.after(300000, self.auto_refresh)

    def export_csv(self):
        if not self.networks:
            messagebox.showwarning("No Data", "No network data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            export_to_csv(self.networks, file_path)
            messagebox.showinfo("Exported", f"Data exported to {file_path}")

def run_app():
    root = tk.Tk()
    app = WifiScannerApp(root)
    root.mainloop()

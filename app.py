# app.py

# 2. Create the main window
import tkinter as tk
from tkinter import ttk, messagebox
import json
import urllib.request  # part of stdlib; no external libs needed
import urllib.error

API_URL = "http://localhost:5000/submit"

root = tk.Tk()
root.title("Mini Form App")

# 3. Adding the form elements (controls-widgets)
# ---------- FORM VARIABLES ----------
name_var = tk.StringVar()
email_var = tk.StringVar()
Product_var = tk.IntVar(value=0)
description_var = tk.BooleanVar()
instore_var = tk.BooleanVar(value=False)
online_var = tk.BooleanVar(value=False)

# ---------- LAYOUT ----------
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Name
ttk.Label(frame, text="Name:").grid(column=0, row=0, sticky=tk.W)
name_entry = ttk.Entry(frame, width=30, textvariable=name_var)
name_entry.grid(column=1, row=0)

# Email
ttk.Label(frame, text="Email:").grid(column=0, row=1, sticky=tk.W)
email_entry = ttk.Entry(frame, width=30, textvariable=email_var)
email_entry.grid(column=1, row=1)

# Product
ttk.Label(frame, text="Product:").grid(column=0, row=2, sticky=tk.W)
Product_spinbox = ttk.Spinbox(frame, from_=0, to=120, textvariable=Product_var, width=5)
Product_spinbox.grid(column=1, row=2, sticky=tk.W)

# In-store checkbox
instore_cb = ttk.Checkbutton(frame, text="In-store", variable=instore_var)
instore_cb.grid(column=0, row=3, sticky=tk.W)

# Online checkbox
online_cb = ttk.Checkbutton(frame, text="Online", variable=online_var)
online_cb.grid(column=1, row=3, sticky=tk.W)

# Submit button
submit_btn = ttk.Button(frame, text="Submit", command=lambda: submit_form())
submit_btn.grid(row=4, columnspan=2, pady=(10, 0))


# 4. Local validation
def validate() -> bool:
    """Return True if all fields are valid; otherwise show an error."""
    # Simple non-empty checks
    if not name_var.get().strip():
        messagebox.showerror("Validation Error", "Name connot be empty.")
        return False

    email = email_var.get().strip()
    if not email or "@" not in email:
        messagebox.showerror("ValidationError", "Enter a valid email address,")
        return False

    price = Product_var.get()
    if price < 0 or price > 1000:
        messagebox.showerror("Validation Error", "Price must be between 0 and 1000.")
        return False

    return True


# 5. Convert form data to json
def collect_data() -> dict:
    """Return a dictionary that represents the form."""
    return {
        "name": name_var.get().strip(),
        "email": email_var.get().strip(),
        "price": Product_var.get(),
        "instore": instore_var.get(),
        "online": online_var.get(),
    }


# 6. Post the JSON to the API and Validate
def submit_form() -> None:
    if not validate():
        return

    # abort if validation failed

    payload = collect_data()
    json_payload = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=json_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            messagebox.showinfo("Success", f"Server replied: {result}")
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        messagebox.showerror("API Error", f"{e.code} – {error_msg}")
    except Exception as exc:
        messagebox.showerror("Connection Error", str(exc))


if __name__ == "__main__":
    root.mainloop()

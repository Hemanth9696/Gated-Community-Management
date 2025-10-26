import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# ==========================
# Database Management
# ==========================
class Database:
    def __init__(self, db_name="community.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS houses (
                        house_id INTEGER PRIMARY KEY,
                        owner TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS services (
                        service_id INTEGER PRIMARY KEY,
                        name TEXT,
                        cost INTEGER
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS requests (
                        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        house_id INTEGER,
                        service_id INTEGER,
                        status TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS bills (
                        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        house_id INTEGER,
                        amount REAL,
                        status TEXT
                    )''')
        self.conn.commit()

    def insert_house(self, house_id, owner):
        self.conn.execute("INSERT OR IGNORE INTO houses VALUES (?, ?)", (house_id, owner))
        self.conn.commit()

    def insert_service(self, service_id, name, cost):
        self.conn.execute("INSERT OR IGNORE INTO services VALUES (?, ?, ?)", (service_id, name, cost))
        self.conn.commit()

    def insert_request(self, req):
        self.conn.execute("INSERT INTO requests (house_id, service_id, status) VALUES (?, ?, ?)",
                          (req.house_id, req.service_id, req.status))
        self.conn.commit()

    def insert_bill(self, bill):
        self.conn.execute("INSERT INTO bills (house_id, amount, status) VALUES (?, ?, ?)",
                          (bill.house_id, bill.amount, bill.status))
        self.conn.commit()

    def update_bill_status(self, bill_id, status):
        self.conn.execute("UPDATE bills SET status = ? WHERE bill_id = ?", (status, bill_id))
        self.conn.commit()

# ==========================
# Core Classes
# ==========================
class House:
    def __init__(self, house_id, owner):
        self.house_id = house_id
        self.owner = owner
        self.residents = []

    def __str__(self):
        return f"House {self.house_id} - Owner: {self.owner}"

class Service:
    def __init__(self, service_id, name, cost):
        self.service_id = service_id
        self.name = name
        self.cost = cost

    def __str__(self):
        return f"Service {self.service_id}: {self.name} (₹{self.cost})"

class Request:
    def __init__(self, request_id, house_id, service_id, status="Pending"):
        self.request_id = request_id
        self.house_id = house_id
        self.service_id = service_id
        self.status = status

    def __str__(self):
        return f"Request #{self.request_id}: House {self.house_id} → Service {self.service_id} [{self.status}]"

class Bill:
    _id_counter = 1
    def __init__(self, house_id, amount):
        self.bill_id = Bill._id_counter
        Bill._id_counter += 1
        self.house_id = house_id
        self.amount = amount
        self.status = "Unpaid"

    def pay(self):
        self.status = "Paid"

    def __str__(self):
        return f"Bill #{self.bill_id}: ₹{self.amount} [{self.status}]"

class Community:
    def __init__(self):
        self.houses = []
        self.services = []
        self.requests = []
        self.bills = []

    def add_house(self, house):
        self.houses.append(house)

    def add_service(self, service):
        self.services.append(service)

    def request_service(self, house_id, service_id):
        house = next((h for h in self.houses if h.house_id == house_id), None)
        service = next((s for s in self.services if s.service_id == service_id), None)

        if house and service:
            req = Request(len(self.requests) + 1, house_id, service_id)
            bill = Bill(house_id, service.cost)
            self.requests.append(req)
            self.bills.append(bill)
            return req, bill
        return None, None

    def get_bills(self):
        return self.bills

# ==========================
# GUI Application
# ==========================
class GatedCommunityApp:
    def __init__(self, root, community, db):
        self.root = root
        self.community = community
        self.db = db
        self.root.title("🏡 Gated Community Management System")
        self.root.geometry("600x400")
        self.root.config(bg="#f8f9fa")

        title = tk.Label(root, text="🏠 Gated Community Management System", font=("Arial", 16, "bold"), bg="#f8f9fa")
        title.pack(pady=20)

        btn_view_houses = tk.Button(root, text="View Houses", command=self.view_houses, width=25, height=2, bg="#007bff", fg="white")
        btn_view_houses.pack(pady=10)

        btn_view_services = tk.Button(root, text="View Services", command=self.view_services, width=25, height=2, bg="#28a745", fg="white")
        btn_view_services.pack(pady=10)

        btn_request_service = tk.Button(root, text="Request a Service", command=self.request_service, width=25, height=2, bg="#ffc107", fg="black")
        btn_request_service.pack(pady=10)

        btn_view_bills = tk.Button(root, text="View My Bills", command=self.view_bills, width=25, height=2, bg="#17a2b8", fg="white")
        btn_view_bills.pack(pady=10)

        btn_pay_bill = tk.Button(root, text="Pay a Bill", command=self.pay_bill, width=25, height=2, bg="#dc3545", fg="white")
        btn_pay_bill.pack(pady=10)

    def view_houses(self):
        houses = "\n".join(str(h) for h in self.community.houses)
        messagebox.showinfo("Houses", houses if houses else "No houses found.")

    def view_services(self):
        services = "\n".join(str(s) for s in self.community.services)
        messagebox.showinfo("Services", services if services else "No services found.")

    def request_service(self):
        try:
            house_id = int(simpledialog.askstring("Request", "Enter your House ID:"))
            service_id = int(simpledialog.askstring("Request", "Enter Service ID:"))
            req, bill = self.community.request_service(house_id, service_id)
            if req:
                self.db.insert_request(req)
                self.db.insert_bill(bill)
                messagebox.showinfo("✅ Request Created", f"{req}\n💰 {bill}")
            else:
                messagebox.showerror("Error", "Invalid House ID or Service ID")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input.\n{e}")

    def view_bills(self):
        try:
            house_id = int(simpledialog.askstring("Bills", "Enter your House ID:"))
            bills = [str(b) for b in self.community.bills if b.house_id == house_id]
            messagebox.showinfo("Bills", "\n".join(bills) if bills else "No bills found.")
        except:
            messagebox.showerror("Error", "Invalid input.")

    def pay_bill(self):
        try:
            bill_id = int(simpledialog.askstring("Payment", "Enter Bill ID to pay:"))
            for bill in self.community.get_bills():
                if bill.bill_id == bill_id:
                    if bill.status == "Paid":
                        messagebox.showinfo("Info", "✅ Bill already paid.")
                    else:
                        bill.pay()
                        self.db.update_bill_status(bill.bill_id, "Paid")
                        messagebox.showinfo("💵 Payment Success", str(bill))
                    return
            messagebox.showerror("Error", "Bill not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input.\n{e}")

# ==========================
# Main Execution
# ==========================
if __name__ == "__main__":
    db = Database()

    community = Community()
    # Preload Data
    houses = [(1, "Rajesh"), (2, "Priya"), (3, "Hemanth")]
    services = [(1, "Plumbing", 200), (2, "Electrician", 250), (3, "Cleaning", 150)]

    for h in houses:
        db.insert_house(*h)
        community.add_house(House(*h))

    for s in services:
        db.insert_service(*s)
        community.add_service(Service(*s))

    root = tk.Tk()
    app = GatedCommunityApp(root, community, db)
    root.mainloop()

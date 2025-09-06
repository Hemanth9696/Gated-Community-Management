import tkinter as tk
from tkinter import messagebox, simpledialog

# ------------------ Core Classes ------------------

class House:
    def __init__(self, house_id, owner):
        self.house_id = house_id
        self.owner = owner
        self.residents = []

    def add_resident(self, name):
        self.residents.append(name)

    def __str__(self):
        return f"House {self.house_id} | Owner: {self.owner} | Residents: {', '.join(self.residents)}"


class Service:
    def __init__(self, service_id, name, provider, cost):
        self.service_id = service_id
        self.name = name
        self.provider = provider
        self.cost = cost

    def __str__(self):
        return f"Service {self.service_id} | {self.name} by {self.provider} | Cost: ₹{self.cost}"


class Request:
    def __init__(self, request_id, house, service):
        self.request_id = request_id
        self.house = house
        self.service = service
        self.status = "Pending"

    def complete_request(self):
        self.status = "Completed"

    def __str__(self):
        return f"Request {self.request_id} | {self.house.owner} requested {self.service.name} | Status: {self.status}"


class Bill:
    def __init__(self, bill_id, house, amount):
        self.bill_id = bill_id
        self.house = house
        self.amount = amount
        self.status = "Unpaid"

    def pay(self):
        self.status = "Paid"

    def __str__(self):
        return f"Bill {self.bill_id} | House {self.house.house_id} | Amount: ₹{self.amount} | Status: {self.status}"


class Community:
    def __init__(self, name):
        self.name = name
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
            request = Request(len(self.requests) + 1, house, service)
            self.requests.append(request)
            bill = Bill(len(self.bills) + 1, house, service.cost)
            self.bills.append(bill)
            return request, bill
        return None, None

    def get_houses(self):
        return self.houses

    def get_services(self):
        return self.services

    def get_requests(self):
        return self.requests

    def get_bills(self):
        return self.bills


# ------------------ GUI ------------------

class GatedCommunityApp:
    def __init__(self, root, community):
        self.root = root
        self.community = community
        self.root.title("🏡 Gated Community Management")
        self.root.geometry("600x400")

        tk.Label(root, text="Gated Community Management", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(root, text="View Houses", width=25, command=self.view_houses).pack(pady=5)
        tk.Button(root, text="View Services", width=25, command=self.view_services).pack(pady=5)
        tk.Button(root, text="Request a Service", width=25, command=self.request_service).pack(pady=5)
        tk.Button(root, text="View My Bills", width=25, command=self.view_bills).pack(pady=5)
        tk.Button(root, text="Pay a Bill", width=25, command=self.pay_bill).pack(pady=5)
        tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=20)

    def view_houses(self):
        houses = "\n".join(str(h) for h in self.community.get_houses())
        messagebox.showinfo("🏠 Houses", houses if houses else "No houses found.")

    def view_services(self):
        services = "\n".join(str(s) for s in self.community.get_services())
        messagebox.showinfo("🛠 Services", services if services else "No services found.")

    def request_service(self):
        try:
            house_id = int(simpledialog.askstring("Request", "Enter your House ID:"))
            service_id = int(simpledialog.askstring("Request", "Enter Service ID:"))
            req, bill = self.community.request_service(house_id, service_id)
            if req:
                messagebox.showinfo("✅ Request Created", f"{req}\n💰 {bill}")
            else:
                messagebox.showerror("Error", "Invalid House ID or Service ID")
        except Exception:
            messagebox.showerror("Error", "Invalid input.")

    def view_bills(self):
        try:
            house_id = int(simpledialog.askstring("Bills", "Enter your House ID:"))
            bills = [str(b) for b in self.community.get_bills() if b.house.house_id == house_id]
            messagebox.showinfo("💳 Bills", "\n".join(bills) if bills else "No bills found.")
        except Exception:
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
                        messagebox.showinfo("💵 Payment Success", str(bill))
                    return
            messagebox.showerror("Error", "Bill not found.")
        except Exception:
            messagebox.showerror("Error", "Invalid input.")


# ------------------ Run App ------------------

if __name__ == "__main__":
    community = Community("Green Valley Residency")

    h1 = House(1, "Ravi")
    h1.add_resident("Anita")
    community.add_house(h1)

    h2 = House(2, "John")
    h2.add_resident("Alice")
    community.add_house(h2)
    
    
    h3 = House(3, "Hemanth")
    h3.add_resident("jon snow")
    community.add_house(h3)

    community.add_service(Service(1, "Plumbing", "Mr. Kumar", 500))
    community.add_service(Service(2, "Grocery Delivery", "FreshMart", 200))
    community.add_service(Service(3, "Electrician", "PowerFix", 700))

    root = tk.Tk()
    app = GatedCommunityApp(root, community)
    root.mainloop()

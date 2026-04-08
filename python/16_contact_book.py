# Python Program 16: Simple Contact Book
# Author: Lydia S. Makiwa
# Description: Add, view, search, and delete contacts using a dictionary

contacts = {}

def add_contact(name, phone, email=""):
    contacts[name.lower()] = {"name": name, "phone": phone, "email": email}
    print(f"✅ Contact '{name}' added.")

def search_contact(query):
    results = {k: v for k, v in contacts.items() if query.lower() in k}
    if results:
        for v in results.values():
            print(f"  📞 {v['name']} | Phone: {v['phone']} | Email: {v['email'] or 'N/A'}")
    else:
        print("  No contacts found.")

def delete_contact(name):
    if name.lower() in contacts:
        del contacts[name.lower()]
        print(f"🗑️  Deleted contact: {name}")
    else:
        print("Contact not found.")

def list_all():
    if not contacts:
        print("  No contacts saved.")
        return
    print(f"  {'Name':<20} {'Phone':<15} Email")
    print("  " + "-" * 50)
    for v in sorted(contacts.values(), key=lambda x: x['name']):
        print(f"  {v['name']:<20} {v['phone']:<15} {v['email'] or '—'}")

# Demo
add_contact("Lydia Makiwa",   "+27 71 000 0001", "lydia@gmail.com")
add_contact("Alice Johnson",  "+1 555 123 4567",  "alice@example.com")
add_contact("Bob Smith",      "+44 20 7946 0958")
add_contact("Dr. Patel",      "+91 98765 43210", "patel@university.ac.in")

print()
list_all()
print()
search_contact("lydia")
delete_contact("Bob Smith")
list_all()

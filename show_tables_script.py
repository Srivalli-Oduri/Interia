from app import app, db, Designer, Quote

def show_data():
    with app.app_context():
        print("--- Designers ---")
        designers = Designer.query.all()
        if not designers:
            print("No designers found.")
        for d in designers:
            print(f"ID: {d.id}, Name: {d.name}, Email: {d.email}, Specialty: {d.specialty}")

        print("\n--- Quotes ---")
        quotes = Quote.query.all()
        if not quotes:
            print("No quotes found.")
        for q in quotes:
            print(f"ID: {q.id}, Customer: {q.customer_name}, Service: {q.service}, Status: {q.status}, Designer ID: {q.designer_id}")

if __name__ == "__main__":
    show_data()

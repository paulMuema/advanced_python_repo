# This script sets up a SQLite database for property listings in Nairobi, Kenya.

import sqlite3

conn = sqlite3.connect('properties.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    price INTEGER NOT NULL,
    bedrooms INTEGER NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT
)
''')

# Sample listings
listings = [
    ("1-Bedroom in Kilimani", "Kilimani", 55000, 1, "Spacious 1-bedroom apartment in Kilimani with modern amenities.", "https://example.com/kilimani.jpg"),
    ("2-Bedroom in Westlands", "Westlands", 75000, 2, "Beautiful 2-bedroom apartment in Westlands with a pool.", "https://example.com/westlands.jpg"),
    ("3-Bedroom in Parklands", "Parklands", 90000, 3, "Luxurious 3-bedroom apartment in Parklands with a gym.", "https://example.com/parklands.jpg"),
    ("Studio in CBD", "CBD", 40000, 0, "Cozy studio apartment in the heart of Nairobi CBD.", "https://example.com/cbd.jpg"),
    ("Penthouse in Kileleshwa", "Kileleshwa", 150000, 4, "Stunning penthouse in Kileleshwa with a rooftop terrace.", "https://example.com/kileleshwa.jpg")
]

cursor.executemany('''
INSERT INTO listings (title, location, price, bedrooms, description, image_url) VALUES (?, ?, ?, ?, ?, ?)''', listings)

conn.commit()
conn.close()
print("Database setup complete and sample listings added.")
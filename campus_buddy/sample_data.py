"""Sample demo dataset for Campus Buddy college assistant.

Note: This is demo data for college orientation and assistance. In a production
environment, these would be retrieved from university APIs or a database.
"""

# Demo schedule for Monday through Friday
SAMPLE_TIMETABLE: dict[str, list[str]] = {
    "monday": [
        "09:00 Python Programming",
        "11:00 Engineering Maths",
        "14:00 Digital Logic Lab",
    ],
    "tuesday": [
        "09:00 Physics",
        "11:00 Python Programming",
        "14:00 Communication Skills",
    ],
    "wednesday": [
        "09:00 Engineering Maths",
        "11:00 Data Structures",
        "14:00 Sports",
    ],
    "thursday": [
        "09:00 Data Structures",
        "11:00 Physics Lab",
        "14:00 Library Hour",
    ],
    "friday": [
        "09:00 AI Club Workshop",
        "11:00 Engineering Maths",
        "14:00 Mentor Meeting",
    ],
}

# Demo canteen menu for Monday through Friday
SAMPLE_CANTEEN_MENU: dict[str, str] = {
    "monday": "Idli, Sambar, Lemon Rice",
    "tuesday": "Poori, Aloo Curry, Curd Rice",
    "wednesday": "Dosa, Chutney, Veg Biryani",
    "thursday": "Upma, Rajma Chawal, Buttermilk",
    "friday": "Pongal, Chicken Biryani, Gulab Jamun",
}

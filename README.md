# Smart Waste Bin Monitoring System

A web-based application that simulates smart waste bin monitoring and helps track bin fill levels, identify bins requiring collection, and maintain collection records.

## Features

- **Bin Registration:** Register waste bins with unique IDs and locations.
- **Fill-Level Simulation:** Automatically simulate waste accumulation at regular intervals.
- **Bin Status Monitoring:** Track bin conditions as Normal, Filling Up, Almost Full, or Full.
- **Collection Alerts:** Display warnings for bins at 80% or above and urgent alerts at 95% or above.
- **Automatic Collection Simulation:** Select the most filled eligible bin for simulated collection every 30 seconds.
- **Collection History:** Maintain and display the 10 most recent collection records.
- **Dashboard:** View bin statistics and collection information in one place.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

```text
Smart_Waste_Bin_Monitoring/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    └── index.html
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project folder:

   ```bash
   cd Smart_Waste_Bin_Monitoring
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   python app.py
   ```

7. Open the following address in your browser:

   `http://127.0.0.1:5000/`

## Note

This project is a software-based prototype. Waste accumulation and collection activities are simulated using automatically generated values; physical sensors and collection vehicles are not connected.
import random
from flask import Flask, render_template, request, jsonify
from database import create_table, get_db_connection

app = Flask(__name__)

create_table()


@app.route("/")
def home():
    return render_template("index.html")


# Get all registered bins
@app.route("/api/bins", methods=["GET"])
def get_bins():
    conn = get_db_connection()
    bins = conn.execute("SELECT * FROM bins").fetchall()
    conn.close()

    return jsonify([dict(bin) for bin in bins])


# Add a new bin
@app.route("/api/bins", methods=["POST"])
def add_bin():
    data = request.get_json()

    bin_id = data.get("bin_id", "").strip()
    location = data.get("location", "").strip()

    if not bin_id or not location:
        return jsonify({"message": "Please enter Bin ID and Location"}), 400

    conn = get_db_connection()

    try:
        fill_rate = random.randint(1, 5)

        conn.execute(
            "INSERT INTO bins (bin_id, location, fill_rate) VALUES (?, ?, ?)",
            (bin_id, location, fill_rate)
        )

        conn.commit()
        return jsonify({"message": "Bin added successfully!"})

    except Exception:
        return jsonify({"message": "Bin ID already exists!"}), 400

    finally:
        conn.close()


# Generate automatic simulated sensor readings
@app.route("/api/simulate", methods=["POST"])
def simulate_readings():
    conn = get_db_connection()

    bins = conn.execute("SELECT * FROM bins").fetchall()

    for bin in bins:
        current_level = bin["fill_level"]

        # Skip bins that are already full
        if current_level >= 100:
            continue

        # Generate a random increment around the bin's base fill rate
        increment = max(1, bin["fill_rate"] + random.randint(-1, 1))

        new_level = min(100, current_level + increment)


        if new_level < 60:
            status = "Normal"
        elif new_level < 80:
            status = "Filling Up"
        elif new_level < 95:
            status = "Almost Full"
        else:
            status = "Full"

        conn.execute(
            "UPDATE bins SET fill_level = ?, status = ? WHERE bin_id = ?",
            (new_level, status, bin["bin_id"])
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "Sensor readings updated successfully!"})



# Simulate automatic waste collection
@app.route("/api/simulate-collection", methods=["POST"])
def simulate_collection():
    conn = get_db_connection()

    try:
        # Find one bin that urgently needs collection
        bin = conn.execute("""
            SELECT * FROM bins
            WHERE fill_level >= 95
            ORDER BY fill_level DESC, id ASC
            LIMIT 1
        """).fetchone()

        if bin is None:
            return jsonify({"message": "No bins require urgent collection."})

        # Record the automatic collection
        conn.execute(
            "INSERT INTO collection_history (bin_id, location) VALUES (?, ?)",
            (bin["bin_id"], bin["location"])
        )

        # Reset the bin after simulated collection
        conn.execute(
            "UPDATE bins SET fill_level = 0, status = 'Normal' WHERE bin_id = ?",
            (bin["bin_id"],)
        )

        conn.commit()

        return jsonify({
            "message": "Bin collected automatically!",
            "bin_id": bin["bin_id"]
        })

    except Exception:
        conn.rollback()
        return jsonify({"message": "Collection could not be recorded!"}), 500

    finally:
        conn.close()



# Get collection history
@app.route("/api/collection-history", methods=["GET"])
def get_collection_history():
    conn = get_db_connection()

    history = conn.execute("""
        SELECT * FROM collection_history
        ORDER BY collected_at DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return jsonify([dict(record) for record in history])



if __name__ == "__main__":
    app.run(debug=True)

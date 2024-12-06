from flask import Flask, request, jsonify
import pandas as pd
from methods.nsga2 import run_nsga2

app = Flask(__name__)

@app.route("/")
def home():
    return "Selamat datang di demo Optimasi Rute Inspeksi dengan NSGA-II!"

# Fungsi untuk load data pelanggan
def load_customer_data(file):
    data = pd.read_csv(file, sep=';', on_bad_lines='skip')
    return data

# Fungsi untuk default parameter
def get_default_settings():
    return {
        "min_customer_in_route": 15,
        "inspection_duration": 15,
        "uncertain_time_delay": 10,
        "vehicle_speed": 40 / 60,
        "working_hours": 7.5 * 60,
        "work_days": 20,
        "n_vehicles": 2,
        "fixed_length": 2 * 20 * 50,  # n_vehicles * work_days * 50
        "chunk_size": 10
    }

@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        # Ambil file CSV dari request
        csv_file = request.files['file']
        customers_data = load_customer_data(csv_file)

        # Ambil parameter tambahan dari request
        settings = get_default_settings()
        settings["min_customer_in_route"] = int(request.form.get("min_customer_in_route", settings["min_customer_in_route"]))
        settings["inspection_duration"] = int(request.form.get("inspection_duration", settings["inspection_duration"]))
        settings["uncertain_time_delay"] = int(request.form.get("uncertain_time_delay", settings["uncertain_time_delay"]))
        settings["vehicle_speed"] = float(request.form.get("vehicle_speed", settings["vehicle_speed"]))
        settings["working_hours"] = int(request.form.get("working_hours", settings["working_hours"]))
        settings["work_days"] = int(request.form.get("work_days", settings["work_days"]))
        settings["n_vehicles"] = int(request.form.get("n_vehicles", settings["n_vehicles"]))

        # Tambahkan data pelanggan ke settings
        settings["customers_data"] = customers_data

        # Jalankan NSGA-II
        result = run_nsga2(
            population_size=int(request.form.get("population_size", 50)),
            generations=int(request.form.get("generations", 50)),
            settings=settings
        )

        # Return hasil dalam format JSON
        return jsonify({"status": "success", "result": result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

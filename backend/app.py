from flask import Flask, jsonify, request
import psycopg2
import socket
import threading
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="photon",
            user="postgres",
            password="student"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

# UDP socket setup for broadcasting
udp_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# UDP socket setup for receiving
udp_socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket_receive.bind(('0.0.0.0', 7501))

# Function to listen for incoming data
def listen_udp():
    while True:
        try:
            data, addr = udp_socket_receive.recvfrom(1024)
            received_data = data.decode()
            print(f"Received data: {received_data} from {addr}")
            # TODO: Handle received data as per requirements
        except Exception as e:
            print(f"Error receiving UDP data: {e}")

# Start the UDP listener in a separate thread
listener_thread = threading.Thread(target=listen_udp, daemon=True)
listener_thread.start()

@app.route('/add_player', methods=['POST'])
def add_player():
    player_data = request.json

    # Validate input data
    if not all(k in player_data for k in ("id", "codename", "equipment_id")):
        return jsonify({"error": "Missing player data"}), 400

    try:
        player_id = int(player_data['id'])
        codename = str(player_data['codename'])
        equipment_id = int(player_data['equipment_id'])
    except ValueError:
        return jsonify({"error": "Invalid data types"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()

        # Optional: Check if player ID or equipment ID already exists
        cur.execute("SELECT * FROM players WHERE id = %s OR equipment_id = %s", (player_id, equipment_id))
        existing_player = cur.fetchone()
        if existing_player:
            return jsonify({"error": "Player ID or Equipment ID already exists"}), 400

        # Add player to database
        cur.execute(
            "INSERT INTO players (id, codename, equipment_id) VALUES (%s, %s, %s)",
            (player_id, codename, equipment_id)
        )

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return jsonify({"error": "Failed to add player to the database"}), 500
    finally:
        conn.close()

    # Broadcast equipment ID
    try:
        udp_socket_broadcast.sendto(
            str(equipment_id).encode(),
            ('<broadcast>', 7500)
        )
    except Exception as e:
        print(f"Error broadcasting UDP data: {e}")
        return jsonify({"error": "Failed to broadcast equipment ID"}), 500

    return jsonify({"message": "Player added successfully"}), 201

if __name__ == '__main__':
    # Ensure the application runs on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

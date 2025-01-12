from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class BabySleepTracker:
    def __init__(self, db_name="baby_sleep.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sleep_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                is_completed BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def start_sleep(self, start_time=None):
        if start_time is None:
            start_time = datetime.now()
        elif isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sleep_records (start_time)
            VALUES (?)
        ''', (start_time,))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        print(f"Created new sleep session with ID: {last_id}")  # Debug print
        return last_id
    
    def end_sleep(self, sleep_id=None, end_time=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if sleep_id is None:
            cursor.execute('''
                SELECT id FROM sleep_records 
                WHERE is_completed = 0 
                ORDER BY start_time DESC LIMIT 1
            ''')
            result = cursor.fetchone()
            if not result:
                conn.close()
                raise ValueError("No active sleep session found")
            sleep_id = result[0]
            
        if end_time is None:
            end_time = datetime.now()
        elif isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        
        cursor.execute('''
            UPDATE sleep_records 
            SET end_time = ?, is_completed = 1
            WHERE id = ?
        ''', (end_time, sleep_id))
        conn.commit()
        conn.close()
    
    def get_day_summary(self, date=None):
        if date is None:
            date = datetime.now().date()
        elif isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
            
        start_of_day = datetime.combine(date, datetime.min.time())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, start_time, end_time
            FROM sleep_records
            WHERE date(start_time) = date(?)
            AND is_completed = 1
            ORDER BY start_time
        ''', (start_of_day,))
        
        naps = cursor.fetchall()
        conn.close()
        
        if not naps:
            return {"message": f"No completed sleep sessions recorded for {date}", "naps": []}
        
        total_sleep = timedelta()
        nap_list = []
        
        for nap_id, start, end in naps:
            try:
                start_time_str = start.split('.')[0]  # Remove milliseconds if present
                end_time_str = end.split('.')[0]  # Remove milliseconds if present
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                duration = end_time - start_time
                total_sleep += duration
                
                nap_list.append({
                    "id": nap_id,
                    "start": start_time.strftime("%H:%M"),
                    "end": end_time.strftime("%H:%M"),
                    "duration": str(duration).split('.')[0]
                })
            except Exception as e:
                print(f"Error processing nap record: {e}")
                continue
        
        hours = total_sleep.total_seconds() / 3600
        return {
            "date": date.strftime("%Y-%m-%d"),
            "naps": nap_list,
            "total_sleep_hours": f"{hours:.2f}",
            "total_sleep_duration": str(total_sleep).split('.')[0]
        }

    def get_active_session(self):
        print("Checking for active session...")  # Debug print
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, start_time 
            FROM sleep_records 
            WHERE is_completed = 0 
            ORDER BY start_time DESC LIMIT 1
        ''')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            try:
                # Handle timestamps with potential milliseconds
                start_time_str = result[1].split('.')[0]  # Remove milliseconds if present
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                active_session = {
                    "id": result[0],
                    "start_time": start_time.strftime("%I:%M %p")
                }
                print(f"Found active session: {active_session}")  # Debug print
                return active_session
            except Exception as e:
                print(f"Error parsing datetime: {e}")
                return None
        print("No active session found")  # Debug print
        return None

    def delete_nap(self, nap_id):
        print(f"Deleting nap with ID: {nap_id}")  # Debug print
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # First check if the nap exists
        cursor.execute('SELECT id FROM sleep_records WHERE id = ?', (nap_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"No nap found with ID {nap_id}")
        
        cursor.execute('DELETE FROM sleep_records WHERE id = ?', (nap_id,))
        conn.commit()
        conn.close()
        return True

    def update_nap(self, nap_id, start_time=None, end_time=None):
        print(f"Updating nap {nap_id} with start: {start_time}, end: {end_time}")  # Debug print
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            
        if end_time and start_time and end_time <= start_time:
            raise ValueError("End time must be after start time")
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if nap exists
        cursor.execute('SELECT id FROM sleep_records WHERE id = ?', (nap_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"No nap found with ID {nap_id}")
        
        # Build update query based on provided values
        update_fields = []
        params = []
        if start_time:
            update_fields.append('start_time = ?')
            params.append(start_time)
        if end_time:
            update_fields.append('end_time = ?')
            params.append(end_time)
        
        if update_fields:
            query = f'UPDATE sleep_records SET {", ".join(update_fields)} WHERE id = ?'
            params.append(nap_id)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
        return True

tracker = BabySleepTracker()

@app.route('/start', methods=['POST'])
def start_sleep():
    print("Received start sleep request")  # Debug print
    data = request.get_json()
    start_time = data.get('start_time')
    try:
        sleep_id = tracker.start_sleep(start_time)
        return jsonify({"message": "Sleep session started", "id": sleep_id}), 201
    except Exception as e:
        print(f"Error starting sleep: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

@app.route('/end', methods=['POST'])
def end_sleep():
    print("Received end sleep request")  # Debug print
    data = request.get_json()
    sleep_id = data.get('sleep_id')
    end_time = data.get('end_time')
    try:
        tracker.end_sleep(sleep_id, end_time)
        return jsonify({"message": "Sleep session ended"}), 200
    except Exception as e:
        print(f"Error ending sleep: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

@app.route('/summary', methods=['GET'])
def get_summary():
    print("Received summary request")  # Debug print
    date = request.args.get('date')
    try:
        summary = tracker.get_day_summary(date)
        return jsonify(summary), 200
    except Exception as e:
        print(f"Error getting summary: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

@app.route('/active', methods=['GET'])
def get_active():
    print("Received active session request")  # Debug print
    try:
        active_session = tracker.get_active_session()
        return jsonify({"active_session": active_session}), 200
    except Exception as e:
        print(f"Error checking active session: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

@app.route('/manual-nap', methods=['POST'])
def add_manual_nap():
    print("Received manual nap request")  # Debug print
    data = request.get_json()
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    if not start_time or not end_time:
        return jsonify({"error": "Both start_time and end_time are required"}), 400
        
    try:
        nap_id = tracker.add_manual_nap(start_time, end_time)
        return jsonify({"message": "Manual nap added", "id": nap_id}), 201
    except Exception as e:
        print(f"Error adding manual nap: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

@app.route('/nap/<int:nap_id>', methods=['DELETE'])
def delete_nap(nap_id):
    print(f"Received delete request for nap {nap_id}")  # Debug print
    try:
        tracker.delete_nap(nap_id)
        return jsonify({"message": "Nap deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting nap: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

@app.route('/nap/<int:nap_id>', methods=['PUT'])
def update_nap(nap_id):
    print(f"Received update request for nap {nap_id}")  # Debug print
    data = request.get_json()
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    try:
        tracker.update_nap(nap_id, start_time, end_time)
        return jsonify({"message": "Nap updated successfully"}), 200
    except Exception as e:
        print(f"Error updating nap: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

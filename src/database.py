import sqlite3
from datetime import datetime
from typing import List, Tuple
import os

class SentimentDatabase:
    """Quản lý cơ sở dữ liệu SQLite cho lịch sử phân loại cảm xúc"""
    
    def __init__(self, db_path: str = "var/data/sentiment_history.db"):
       
        self.db_path = db_path
        # Ensure directory exists. If a legacy `data/` folder exists, prefer it for backwards compatibility.
        dir_name = os.path.dirname(db_path)
        if not os.path.exists(dir_name) and os.path.exists(os.path.join(os.path.dirname(dir_name), 'data')):
            # If repo still uses 'data/', use that folder
            dir_name = os.path.join(os.path.dirname(dir_name), 'data')
            db_path = os.path.join(dir_name, os.path.basename(db_path))
        os.makedirs(dir_name, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_classification(self, text: str, label: str, confidence: float = None):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tạo timestamp ISO format: YYYY-MM-DD HH:MM:SS
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Sử dụng parameterized query để tránh SQL injection
        cursor.execute(
            "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
            (text, label, timestamp)
        )
        
        conn.commit()
        conn.close()
    
    def get_history(self, limit: int = 50, offset: int = 0) -> List[Tuple]:
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sử dụng parameterized query
        cursor.execute(
            "SELECT id, text, sentiment, timestamp FROM sentiments ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def clear_history(self):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sentiments")
        conn.commit()
        conn.close()
    
    def get_total_count(self) -> int:
       
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sentiments")
        result = cursor.fetchone()
        conn.close()
        return result[0]
    
    def get_statistics(self) -> dict:
 
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN sentiment = 'POSITIVE' THEN 1 ELSE 0 END) as positive,
                SUM(CASE WHEN sentiment = 'NEUTRAL' THEN 1 ELSE 0 END) as neutral,
                SUM(CASE WHEN sentiment = 'NEGATIVE' THEN 1 ELSE 0 END) as negative
            FROM sentiments
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total': result[0],
            'positive': result[1],
            'neutral': result[2],
            'negative': result[3]
        }

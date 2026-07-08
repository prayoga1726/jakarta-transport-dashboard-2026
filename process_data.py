import pandas as pd
import numpy as np

def clean_and_process_data(file_path):
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Convert dates to datetime objects
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    # Extract date parts
    df['hari'] = df['tanggal'].dt.day_name()
    df['hari_dalam_minggu'] = df['tanggal'].dt.weekday  # 0: Monday, 6: Sunday
    df['bulan'] = df['tanggal'].dt.strftime('%B')
    df['jam'] = df['tanggal'].dt.hour
    
    # Map Indonesian day names
    indo_days = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }
    df['hari_indo'] = df['hari'].map(indo_days)
    
    # Categorize time range (Peak Hours vs Off-Peak)
    def categorize_time(hour):
        if 7 <= hour <= 9:
            return 'Peak Pagi (07:00 - 09:00)'
        elif 17 <= hour <= 19:
            return 'Peak Sore (17:00 - 19:00)'
        else:
            return 'Off-Peak'
            
    df['kategori_waktu'] = df['jam'].apply(categorize_time)
    
    # Save cleaned/processed file
    output_path = 'data/transportasi_jakarta_2026_clean.csv'
    df.to_csv(output_path, index=False)
    print(f"Data cleaning & processing done. Saved to {output_path}")

if __name__ == '__main__':
    clean_and_process_data('data/transportasi_jakarta_2026.csv')

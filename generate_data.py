import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)

# Create data directory if not exists
os.makedirs('data', exist_ok=True)

# Configuration
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 6, 30)
delta = end_date - start_date
days = delta.days + 1

# Transport Modes and Routes
modes = {
    'TransJakarta': {
        'routes': ['Koridor 1 (Blok M - Kota)', 'Koridor 9 (Pinang Ranti - Pluit)', 'Koridor 13 (Ciledug - Tendean)'],
        'fare': 3500,
        'capacity': 80
    },
    'MRT Jakarta': {
        'routes': ['Bundaran HI - Lebak Bulus', 'Lebak Bulus - Bundaran HI'],
        'fare': 14000, # Max fare
        'capacity': 300
    },
    'LRT Jakarta': {
        'routes': ['Pegangsaan Dua - Velodrome', 'Velodrome - Pegangsaan Dua'],
        'fare': 5000,
        'capacity': 150
    }
}

data = []

current_date = start_date
while current_date <= end_date:
    # Generate records per day
    # More passengers on weekdays, fewer on weekends
    is_weekend = current_date.weekday() >= 5
    base_trips = 150 if not is_weekend else 80
    
    for _ in range(base_trips):
        mode = np.random.choice(list(modes.keys()))
        route = np.random.choice(modes[mode]['routes'])
        
        # Hour of day (simulating peak hours: 07-09 and 17-19)
        # 18 hours in range(5, 23). We'll normalize the probability array.
        probs = np.array([0.02, 0.04, 0.12, 0.15, 0.08, 0.04, 0.04, 0.04, 0.04, 0.04, 0.08, 0.15, 0.10, 0.04, 0.02, 0.02, 0.01, 0.01])
        probs = probs / probs.sum()
        hour = np.random.choice(
            list(range(5, 23)),
            p=probs
        )
        
        timestamp = current_date.replace(hour=hour, minute=np.random.randint(0, 60))
        
        # Peak factor multiplier
        if hour in [7, 8, 9, 17, 18, 19]:
            passenger_multiplier = np.random.uniform(1.2, 1.8)
        else:
            passenger_multiplier = np.random.uniform(0.4, 0.9)
            
        capacity = modes[mode]['capacity']
        passengers = int(np.clip(np.random.normal(capacity * 0.6, capacity * 0.2) * passenger_multiplier, 10, capacity))
        
        # Calculate fare (MRT has variable fare, let's simulate)
        if mode == 'MRT Jakarta':
            fare = np.random.choice([3000, 4000, 7000, 10000, 14000], p=[0.1, 0.2, 0.3, 0.2, 0.2])
        else:
            fare = modes[mode]['fare']
            
        revenue = passengers * fare
        
        # Operational Status
        status = np.random.choice(['Normal', 'Terlambat', 'Gangguan'], p=[0.90, 0.08, 0.02])
        
        data.append({
            'tanggal': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'mode_transportasi': mode,
            'rute': route,
            'jumlah_penumpang': passengers,
            'tarif_rata_rata': fare,
            'total_pendapatan': revenue,
            'status_operasional': status
        })
        
    current_date += timedelta(days=1)

df = pd.DataFrame(data)
df.to_csv('data/transportasi_jakarta_2026.csv', index=False)
print(f"Dataset successfully created with {len(df)} records.")

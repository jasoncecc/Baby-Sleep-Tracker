![BabySleepTracker](https://github.com/user-attachments/assets/6cc47826-b0c7-4c71-902b-2533f69d8439)# Baby Sleep Tracker

Light weight docker web application for tracking baby sleep patterns. This application allows parents to log sleep sessions in real-time or manually add previous naps, providing insights into their baby's sleep patterns.

![Uploa<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
    <!-- Background Card -->
    <rect x="100" y="20" width="600" height="560" rx="10" fill="#ffffff" stroke="#e5e7eb" stroke-width="2"/>
    
    <!-- Header -->
    <rect x="120" y="40" width="560" height="60" rx="5" fill="#f8fafc"/>
    <text x="140" y="80" font-family="Arial" font-size="24" font-weight="bold" fill="#1f2937">Baby Sleep Tracker</text>
    <circle cx="640" cy="70" r="15" fill="#3b82f6"/> <!-- Moon icon -->

    <!-- Date Selector -->
    <rect x="120" y="120" width="460" height="40" rx="5" fill="#ffffff" stroke="#e5e7eb" stroke-width="2"/>
    <text x="140" y="145" font-family="Arial" font-size="14" fill="#6b7280">2025-01-05</text>
    <rect x="600" y="120" width="80" height="40" rx="5" fill="#f3f4f6"/>
    
    <!-- Action Buttons -->
    <rect x="120" y="180" width="270" height="50" rx="5" fill="#3b82f6"/>
    <text x="200" y="210" font-family="Arial" font-size="16" fill="#ffffff" text-anchor="middle">Manual Entry</text>
    
    <rect x="410" y="180" width="270" height="50" rx="5" fill="#ef4444"/>
    <text x="490" y="210" font-family="Arial" font-size="16" fill="#ffffff" text-anchor="middle">Clear Day</text>

    <!-- Start/Stop Buttons -->
    <rect x="120" y="250" width="270" height="50" rx="5" fill="#22c55e"/>
    <text x="200" y="280" font-family="Arial" font-size="16" fill="#ffffff" text-anchor="middle">Start Sleep</text>
    
    <rect x="410" y="250" width="270" height="50" rx="5" fill="#dc2626"/>
    <text x="490" y="280" font-family="Arial" font-size="16" fill="#ffffff" text-anchor="middle">End Sleep</text>

    <!-- Active Session -->
    <rect x="120" y="320" width="560" height="60" rx="5" fill="#dbeafe"/>
    <text x="400" y="355" font-family="Arial" font-size="16" fill="#1e40af" text-anchor="middle">Sleep session active since 2:30 PM</text>

    <!-- Nap Summary -->
    <text x="140" y="420" font-family="Arial" font-size="18" font-weight="bold" fill="#1f2937">Summary for 2025-01-05</text>
    
    <rect x="120" y="440" width="560" height="80" rx="5" fill="#f9fafb"/>
    <text x="140" y="470" font-family="Arial" font-size="16" font-weight="bold" fill="#1f2937">Nap #1</text>
    <text x="140" y="490" font-family="Arial" font-size="14" fill="#4b5563">Start: 2:30 PM</text>
    <text x="140" y="510" font-family="Arial" font-size="14" fill="#4b5563">Duration: 1:30:00</text>
</svg>ding BabySleepTracker.svg…]()


## Features

- Real-time sleep tracking (start/stop functionality)
- Manual nap entry for backdated sleep sessions
- Daily sleep summaries
- Clear data functionality
- Mobile-friendly interface
- Persistent data storage
- Containerized deployment

## Tech Stack

- **Frontend**: React.js with Tailwind CSS
- **Backend**: Python Flask API
- **Database**: SQLite
- **Containerization**: Docker
- **Reverse Proxy**: Nginx

## Project Structure

```
babysleep-docker/
├── backend/
│   ├── server.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
├── nginx/
│   └── nginx.conf
└── docker-compose.yml
```

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/baby-sleep-tracker.git
cd baby-sleep-tracker
```

2. Build and start the containers:
```bash
docker-compose up --build -d
```

3. Access the application:
- Web interface: `http://localhost`
- API endpoint: `http://localhost/api`

## API Endpoints

- `POST /api/start` - Start a sleep session
- `POST /api/end` - End current sleep session
- `GET /api/summary` - Get sleep summary for a specific date
- `GET /api/active` - Check for active sleep session
- `POST /api/manual-nap` - Add a manual nap entry
- `POST /api/clear-day` - Clear all data for a specific date

## Features in Detail

### Sleep Tracking
- Start/stop tracking for real-time monitoring
- Automatic duration calculation
- Active session indicator

### Data Management
- Add historical nap data
- Clear day's data with confirmation
- View daily summaries

### User Interface
- Mobile-responsive design
- Intuitive controls
- Clear visual indicators for active sessions
- Date selection for historical data

## Development

### Prerequisites
- Docker and Docker Compose
- Node.js (for local development)
- Python 3.9+ (for local development)

### Local Development
1. Start backend:
```bash
cd backend
pip install -r requirements.txt
python server.py
```

2. Start frontend:
```bash
cd frontend
npm install
npm start
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

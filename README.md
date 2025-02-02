## Baby Sleep Tracker

Light weight docker web application for tracking baby sleep patterns. This application allows parents to log sleep sessions in real-time or manually add previous naps, providing insights into their baby's sleep patterns.

![BabySleepTracker](https://github.com/user-attachments/assets/6cc47826-b0c7-4c71-902b-2533f69d8439)


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
## Upcoming

- Upcoming features include the ability for login, ability to stop, start and edit other user's nap entries.
- Correct time zone issue
- User login ability
- Add reporting and logging for backend servers via Promethesus and Grafana stack

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

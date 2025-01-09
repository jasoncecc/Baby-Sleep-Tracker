import React, { useState, useEffect, useCallback } from 'react';
import { Moon, Sun, Plus, StopCircle, Calendar, Trash2, PlusCircle } from 'lucide-react';

const API_URL = 'http://192.168.1.172:5000';  // Your backend server IP

const BabySleepTracker = () => {
  const [activeSession, setActiveSession] = useState(null);
  const [summary, setSummary] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showManualEntry, setShowManualEntry] = useState(false);
  const [manualStart, setManualStart] = useState('');
  const [manualEnd, setManualEnd] = useState('');

  const checkActiveSession = async () => {
    try {
      console.log('Checking active session...');
      const response = await fetch(`${API_URL}/active`);
      const data = await response.json();
      setActiveSession(data.active_session);
    } catch (err) {
      console.error('Error checking active session:', err);
    }
  };

  const fetchSummary = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/summary?date=${selectedDate}`);
      const data = await response.json();
      setSummary(data);
    } catch (err) {
      setError('Error fetching summary');
      console.error('Error fetching summary:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedDate]);

  useEffect(() => {
    checkActiveSession();
    fetchSummary();
    const interval = setInterval(checkActiveSession, 30000);
    return () => clearInterval(interval);
  }, [selectedDate, fetchSummary]);

  const startSleep = async () => {
    try {
      const response = await fetch(`${API_URL}/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_time: null })
      });
      if (response.ok) {
        checkActiveSession();
        fetchSummary();
      } else {
        setError('Failed to start sleep session');
      }
    } catch (err) {
      setError('Error starting sleep session');
      console.error('Error starting sleep:', err);
    }
  };

  const endSleep = async () => {
    try {
      const response = await fetch(`${API_URL}/end`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sleep_id: null, end_time: null })
      });
      if (response.ok) {
        setActiveSession(null);
        fetchSummary();
      } else {
        setError('Failed to end sleep session');
      }
    } catch (err) {
      setError('Error ending sleep session');
      console.error('Error ending sleep:', err);
    }
  };

  const clearDayData = async () => {
    if (!window.confirm('Are you sure you want to clear all sleep data for this day?')) {
      return;
    }
    
    try {
      const response = await fetch(`${API_URL}/clear-day`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: selectedDate })
      });
      
      if (response.ok) {
        fetchSummary();
        setError(null);
      } else {
        setError('Failed to clear day data');
      }
    } catch (err) {
      setError('Error clearing day data: ' + err.message);
    }
  };

  const addManualNap = async () => {
    if (!manualStart || !manualEnd) {
      setError('Please fill in both start and end times');
      return;
    }

    try {
      const startDateTime = `${selectedDate} ${manualStart}`;
      const endDateTime = `${selectedDate} ${manualEnd}`;
      
      const response = await fetch(`${API_URL}/manual-nap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_time: startDateTime,
          end_time: endDateTime
        })
      });

      if (response.ok) {
        setShowManualEntry(false);
        setManualStart('');
        setManualEnd('');
        fetchSummary();
        setError(null);
      } else {
        const data = await response.json();
        setError(data.error || 'Failed to add manual nap');
      }
    } catch (err) {
      setError('Error adding manual nap: ' + err.message);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 space-y-4">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Baby Sleep Tracker</h1>
          {activeSession ? (
            <Moon className="text-blue-500" size={24} />
          ) : (
            <Sun className="text-yellow-500" size={24} />
          )}
        </div>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded-md mb-4">
            {error}
          </div>
        )}

        <div className="flex items-center space-x-2 mb-6">
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="border rounded p-2 flex-grow"
          />
          <Calendar className="text-gray-500" size={20} />
        </div>

        <div className="flex justify-between items-center mb-6">
          <button
            onClick={() => setShowManualEntry(!showManualEntry)}
            className="flex items-center space-x-2 px-4 py-2 rounded-md bg-green-500 hover:bg-green-600 text-white"
          >
            <PlusCircle size={20} />
            <span>Manual Entry</span>
          </button>

          <button
            onClick={clearDayData}
            className="flex items-center space-x-2 px-4 py-2 rounded-md bg-red-500 hover:bg-red-600 text-white"
          >
            <Trash2 size={20} />
            <span>Clear Day</span>
          </button>
        </div>

        {showManualEntry && (
          <div className="bg-gray-50 p-4 rounded-md mb-6">
            <h3 className="font-semibold mb-4">Add Manual Nap</h3>
            <div className="space-y-4">
              <div className="flex flex-col">
                <label className="mb-1">Start Time (HH:MM)</label>
                <input
                  type="time"
                  value={manualStart}
                  onChange={(e) => setManualStart(e.target.value)}
                  className="border rounded p-2"
                />
              </div>
              <div className="flex flex-col">
                <label className="mb-1">End Time (HH:MM)</label>
                <input
                  type="time"
                  value={manualEnd}
                  onChange={(e) => setManualEnd(e.target.value)}
                  className="border rounded p-2"
                />
              </div>
              <button
                onClick={addManualNap}
                className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-md"
              >
                Add Nap
              </button>
            </div>
          </div>
        )}

        <div className="flex justify-center space-x-4 mb-6">
          <button
            onClick={startSleep}
            disabled={activeSession}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md ${
              activeSession
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            <Plus size={20} />
            <span>Start Sleep</span>
          </button>

          <button
            onClick={endSleep}
            disabled={!activeSession}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md ${
              !activeSession
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-red-500 hover:bg-red-600 text-white'
            }`}
          >
            <StopCircle size={20} />
            <span>End Sleep</span>
          </button>
        </div>

        {activeSession && (
          <div className="bg-blue-50 p-4 rounded-md mb-6">
            <p className="text-center">
              Sleep session active since {activeSession.start_time}
            </p>
          </div>
        )}

        {loading ? (
          <div className="text-center">Loading...</div>
        ) : (
          summary && (
            <div className="space-y-4">
              <h3 className="font-semibold">Summary for {summary.date}</h3>
              {summary.naps && summary.naps.length > 0 ? (
                <>
                  {summary.naps.map((nap, index) => (
                    <div
                      key={nap.id}
                      className="bg-gray-50 p-3 rounded-md"
                    >
                      <p className="font-medium">Nap #{index + 1}</p>
                      <p>Start: {nap.start}</p>
                      <p>End: {nap.end}</p>
                      <p>Duration: {nap.duration}</p>
                    </div>
                  ))}
                  <div className="border-t pt-3">
                    <p className="font-semibold">
                      Total Sleep: {summary.total_sleep_hours} hours
                    </p>
                    <p className="text-sm text-gray-600">
                      ({summary.total_sleep_duration})
                    </p>
                  </div>
                </>
              ) : (
                <p className="text-center text-gray-500">
                  No sleep sessions recorded for this date
                </p>
              )}
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default BabySleepTracker;

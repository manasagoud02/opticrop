import React, { createContext, useContext, useState, useEffect } from 'react';
import { predictCrop } from '../services/api';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [history, setHistory] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [inputs, setInputs] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [toasts, setToasts] = useState([]);

  // Load history from localStorage on initialization
  useEffect(() => {
    const savedHistory = localStorage.getItem('opticrop_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to parse history from localStorage', e);
      }
    }
  }, []);

  const launchToast = (message, type = 'success') => {
    const id = Date.now() + Math.random().toString(36).substr(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);

    // Auto dismiss after 4 seconds
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  const predictCropAction = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await predictCrop(formData);
      const mergedInputs = { ...data.inputs, ...formData };
      setPrediction({ ...data, inputs: mergedInputs });
      setInputs(mergedInputs);

      // Save to history list (max 5 logs)
      const newLog = {
        crop: data.result,
        confidence: data.top3[0]?.confidence || 0,
        inputs: mergedInputs,
        timestamp: Date.now()
      };
      
      const updatedHistory = [newLog, ...history.filter(h => JSON.stringify(h.inputs) !== JSON.stringify(data.inputs))].slice(0, 5);
      setHistory(updatedHistory);
      localStorage.setItem('opticrop_history', JSON.stringify(updatedHistory));

      launchToast('AI Analysis audit successfully generated!', 'success');
      
      // Scroll to results section smoothly after rendering
      setTimeout(() => {
        const resultsEl = document.getElementById('results');
        if (resultsEl) {
          resultsEl.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
      
    } catch (err) {
      const errMsg = err.response?.data?.error || err.message || 'Network request failed. Please check backend connection.';
      setError(errMsg);
      launchToast(errMsg, 'error');
    } finally {
      setLoading(false);
    }
  };

  const clearPrediction = () => {
    setPrediction(null);
    setInputs(null);
    setError(null);
  };

  return (
    <AppContext.Provider
      value={{
        history,
        prediction,
        inputs,
        loading,
        error,
        toasts,
        launchToast,
        predictCropAction,
        clearPrediction,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

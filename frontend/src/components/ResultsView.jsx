import React from 'react';
import { 
  Sparkles, 
  Download, 
  Share2, 
  CheckCircle, 
  Info, 
  AlertTriangle, 
  Droplet, 
  Thermometer, 
  CloudRain,
  RotateCcw
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler
} from 'chart.js';

// Register ChartJS modules
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler
);

export const ResultsView = () => {
  const { prediction, launchToast, clearPrediction } = useApp();

  if (!prediction) return null;

  const {
    result,
    inputs,
    crop_image,
    crop_summary,
    crop_ph,
    crop_temperature,
    crop_rainfall,
    crop_touchpoints,
    top3,
    match_status,
    match_message,
    match_color,
    param_advice
  } = prediction;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    launchToast('Workspace prediction link copied to clipboard!', 'success');
  };

  const handleDownloadPDF = () => {
    window.print();
  };

  const confidenceValue = top3[0]?.confidence || 0;
  
  // Radial Progress parameters
  const radius = 40;
  const strokeWidth = 8;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (confidenceValue / 100) * circumference;

  // Resolve API Base URL to fetch images
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
  const resolvedImageUrl = `${API_BASE_URL}/image/${crop_image}`;

  // ChartJS configurations
  const chartData = {
    labels: top3.map(item => item.crop),
    datasets: [{
      label: 'Match Confidence (%)',
      data: top3.map(item => item.confidence),
      borderColor: '#16A34A',
      borderWidth: 3,
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#16A34A',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 6,
      pointHoverRadius: 8,
      backgroundColor: (context) => {
        const chart = context.chart;
        const { ctx, chartArea } = chart;
        if (!chartArea) return null;
        const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
        gradient.addColorStop(0, 'rgba(22, 163, 74, 0.15)');
        gradient.addColorStop(1, 'rgba(22, 163, 74, 0.0)');
        return gradient;
      }
    }]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        grid: {
          borderDash: [5, 5],
          color: '#E2E8F0'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    }
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-scale-in" id="results">
      
      {/* 🏆 Centered Hero Result Section */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-8 shadow-sm flex flex-col items-center text-center gap-6 mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-36 h-36 bg-emerald-500/5 blur-2xl rounded-full"></div>
        <div className="absolute bottom-0 left-0 w-36 h-36 bg-blue-500/5 blur-2xl rounded-full"></div>

        {/* Suitability badge header */}
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-100 shadow-sm">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Field Audit Result</span>
        </div>

        {/* Circular Progress Gauge & Crop Image */}
        <div className="flex flex-col sm:flex-row items-center gap-8 my-2">
          {/* Progress Ring */}
          <div className="relative w-32 h-32 flex items-center justify-center shrink-0">
            <svg className="w-32 h-32 transform -rotate-90">
              <circle 
                stroke="rgba(241, 245, 249, 0.8)" 
                strokeWidth={strokeWidth} 
                fill="transparent" 
                r={radius} 
                cx="64" 
                cy="64" 
              />
              <circle 
                stroke="#16A34A" 
                strokeWidth={strokeWidth} 
                strokeDasharray={circumference} 
                strokeDashoffset={strokeDashoffset} 
                strokeLinecap="round" 
                fill="transparent" 
                r={radius} 
                cx="64" 
                cy="64" 
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
              <span className="text-3xl font-black text-slate-800 leading-none">{confidenceValue}%</span>
              <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest mt-1">Accuracy</span>
            </div>
          </div>

          {/* Crop Avatar */}
          <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-white shadow-md bg-slate-50 flex items-center justify-center shrink-0">
            <img 
              src={resolvedImageUrl} 
              alt={result} 
              className="w-full h-full object-cover" 
              onError={(e) => { e.target.src = '/img/default_hero.jpg'; }} 
            />
          </div>
        </div>

        {/* Recommendation Titles */}
        <div>
          <h2 className="text-4xl font-extrabold text-slate-900 tracking-tight capitalize">
            {result}
          </h2>
          <p className="text-slate-500 mt-2 max-w-2xl leading-relaxed text-sm md:text-base">
            {crop_summary}
          </p>
        </div>

        {/* Actions button group */}
        <div className="flex flex-wrap justify-center gap-3 pt-2">
          <button 
            onClick={handleDownloadPDF} 
            className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-all shadow-sm gap-2"
          >
            <Download className="w-4 h-4 text-slate-500" />
            <span>Download PDF</span>
          </button>
          
          <button 
            onClick={handleCopyLink} 
            className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-all shadow-sm gap-2"
            id="copyShareBtn"
          >
            <Share2 className="w-4 h-4 text-slate-500" />
            <span>Copy Link</span>
          </button>

          <button 
            onClick={clearPrediction} 
            className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl transition-all shadow-sm gap-2"
          >
            <RotateCcw className="w-4 h-4 text-slate-500" />
            <span>Analyze Again</span>
          </button>
        </div>
      </div>

      {/* Grid: Details Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start mb-8">
        
        {/* Left Column: Good Fit & Adjustments */}
        <div className="flex flex-col gap-6">
          
          {/* Success card - Good fit */}
          <div className="bg-white border border-slate-200/80 border-l-4 border-l-emerald-500 rounded-r-2xl p-6 shadow-sm text-left">
            <div className="flex gap-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 shrink-0 shadow-sm">
                <CheckCircle className="w-5.5 h-5.5" />
              </div>
              <div>
                <h4 className="font-extrabold text-slate-800 text-sm capitalize">{match_status} Fit Status</h4>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">{match_message}</p>
              </div>
            </div>
          </div>

          {/* Adjustments checklist */}
          {param_advice && param_advice.length > 0 && (
            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm">
              <h3 className="text-base font-bold text-slate-800 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-500" />
                <span>Adjustments Checklist</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {param_advice.map((advice, i) => {
                  const isLow = advice.status === 'low';
                  const borderClass = isLow ? 'border-l-4 border-l-rose-500' : 'border-l-4 border-l-amber-500';
                  const iconClass = isLow ? 'text-rose-600 bg-rose-50 border-rose-100' : 'text-amber-600 bg-amber-50 border-amber-100';
                  
                  return (
                    <div key={i} className={`flex items-start gap-3 p-4 bg-slate-50 border border-slate-200/60 rounded-r-xl ${borderClass} shadow-xs text-left`}>
                      <div className={`flex h-8 w-8 items-center justify-center rounded-lg border shrink-0 ${iconClass}`}>
                        {isLow ? <AlertTriangle className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-800 text-xs uppercase tracking-wide">
                          {advice.param} too {advice.status}
                        </h4>
                        <p className="text-[11px] text-slate-500 mt-1 leading-normal">{advice.msg}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Specifications Table & Probabilities */}
        <div className="flex flex-col gap-6">
          
          {/* Growing Specs Responsive Table */}
          <div className="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-sm">
            <div className="px-5 py-4 border-b border-slate-100 text-left">
              <h3 className="text-base font-bold text-slate-800">Agronomical Growing Parameters</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 text-[10px] font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100">
                    <th className="py-3 px-5">Growing Spec</th>
                    <th className="py-3 px-5 text-right">Ideal Range</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs text-slate-600 font-medium">
                  <tr className="hover:bg-slate-50/50 transition-colors">
                    <td className="py-3.5 px-5 flex items-center gap-2.5 text-slate-700">
                      <Droplet className="w-4 h-4 text-sky-500" />
                      <span>Soil pH Range</span>
                    </td>
                    <td className="py-3.5 px-5 text-right font-extrabold text-slate-800">{crop_ph}</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50 transition-colors">
                    <td className="py-3.5 px-5 flex items-center gap-2.5 text-slate-700">
                      <Thermometer className="w-4 h-4 text-orange-500" />
                      <span>Temperature Range</span>
                    </td>
                    <td className="py-3.5 px-5 text-right font-extrabold text-slate-800">{crop_temperature}</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50 transition-colors">
                    <td className="py-3.5 px-5 flex items-center gap-2.5 text-slate-700">
                      <CloudRain className="w-4 h-4 text-blue-500" />
                      <span>Rainfall Requirement</span>
                    </td>
                    <td className="py-3.5 px-5 text-right font-extrabold text-slate-800">{crop_rainfall}</td>
                  </tr>
                  {crop_touchpoints && crop_touchpoints.length > 0 && (
                    <tr className="bg-emerald-50/10 hover:bg-emerald-50/20 transition-colors text-emerald-800">
                      <td className="py-3.5 px-5 flex items-center gap-2.5 font-bold">
                        <Sparkles className="w-4 h-4 text-emerald-600" />
                        <span>Field Management Tip</span>
                      </td>
                      <td className="py-3.5 px-5 text-right font-medium text-[11px] leading-relaxed max-w-[240px]">
                        {crop_touchpoints[0]}
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Probabilities Spectrum with horizontal bars */}
          <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm">
            <h3 className="text-base font-bold text-slate-800 mb-4 text-left">Probabilities Spectrum</h3>
            <div className="space-y-4">
              {top3.map((item, index) => {
                const colors = 
                  index === 0 ? { bg: 'bg-emerald-500', text: 'text-emerald-700', card: 'border-emerald-100 bg-emerald-50/5' } :
                  index === 1 ? { bg: 'bg-sky-500', text: 'text-sky-700', card: 'border-sky-100 bg-sky-50/5' } :
                  { bg: 'bg-amber-500', text: 'text-amber-700', card: 'border-amber-100 bg-amber-50/5' };

                return (
                  <div key={index} className={`border rounded-xl p-4 text-left transition-all ${colors.card}`}>
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-extrabold text-slate-400">0{index + 1}</span>
                        <span className="font-extrabold text-slate-800 capitalize">{item.crop}</span>
                      </div>
                      <span className={`text-xs font-black ${colors.text}`}>{item.confidence}%</span>
                    </div>
                    {/* Animated bar wrapper */}
                    <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${colors.bg}`} 
                        style={{ width: `${item.confidence}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>

      </div>

      {/* Graphics Breakdown Chart */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm mb-8 text-left">
        <h3 className="text-base font-bold text-slate-800 mb-1">Confidence Index Comparisons</h3>
        <p className="text-xs text-slate-450 mb-4">Visual representation of comparative crop fit probability.</p>
        <div style={{ height: '220px', width: '100%' }}>
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* Submitted parameters profile */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm text-left">
        <h3 className="text-base font-bold text-slate-800 mb-4">Analyzed Parameter Profile</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-7 gap-4">
          {Object.entries(inputs).map(([key, value]) => {
            if (typeof value === 'string' && value.length > 20) return null;
            return (
              <div key={key} className="bg-slate-50 border border-slate-100 rounded-xl p-3 text-center">
                <span className="block text-[9px] font-bold text-slate-400 uppercase tracking-widest">{key}</span>
                <span className="block text-base font-extrabold text-slate-800 mt-1.5 capitalize">{value}</span>
              </div>
            );
          })}
        </div>
      </div>

    </section>
  );
};

export default ResultsView;

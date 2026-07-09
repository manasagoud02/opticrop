import React, { useState } from 'react';
import { 
  Sprout,
  Droplet, 
  Thermometer, 
  CloudRain, 
  Hash, 
  AlertTriangle, 
  TrendingUp, 
  Cpu, 
  MapPin, 
  Globe, 
  Maximize2, 
  Activity, 
  Layers, 
  HelpCircle 
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const WorkspaceForm = () => {
  const { predictCropAction, loading, error, history } = useApp();

  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: '',
    // Metadata fields
    soilType: 'Loamy',
    moisture: '',
    locationName: '',
    region: '',
    fieldSize: '',
    previousCrop: 'None',
    irrigationType: 'Drip'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Parse numeric values before submitting to prevent format mismatch
    const numericData = {
      N: parseFloat(formData.N),
      P: parseFloat(formData.P),
      K: parseFloat(formData.K),
      temperature: parseFloat(formData.temperature),
      humidity: parseFloat(formData.humidity),
      ph: parseFloat(formData.ph),
      rainfall: parseFloat(formData.rainfall),
      // Keep metadata
      soilType: formData.soilType,
      moisture: formData.moisture ? parseFloat(formData.moisture) : '',
      locationName: formData.locationName,
      region: formData.region,
      fieldSize: formData.fieldSize ? parseFloat(formData.fieldSize) : '',
      previousCrop: formData.previousCrop,
      irrigationType: formData.irrigationType
    };
    predictCropAction(numericData);
  };

  const loadHistoryItem = (item) => {
    setFormData({
      N: item.inputs.N?.toString() || '',
      P: item.inputs.P?.toString() || '',
      K: item.inputs.K?.toString() || '',
      temperature: item.inputs.temperature?.toString() || '',
      humidity: item.inputs.humidity?.toString() || '',
      ph: item.inputs.ph?.toString() || '',
      rainfall: item.inputs.rainfall?.toString() || '',
      soilType: item.inputs.soilType || 'Loamy',
      moisture: item.inputs.moisture?.toString() || '',
      locationName: item.inputs.locationName || '',
      region: item.inputs.region || '',
      fieldSize: item.inputs.fieldSize?.toString() || '',
      previousCrop: item.inputs.previousCrop || 'None',
      irrigationType: item.inputs.irrigationType || 'Drip'
    });
    predictCropAction(item.inputs);
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12" id="workspace-anchor">
      
      {/* Title block */}
      <div className="text-center md:text-left mb-8">
        <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest block mb-2">Agtech Workspace</span>
        <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Run Field Suitability Audit</h2>
        <p className="text-slate-500 mt-2">Provide local soil diagnostics and climate details below to query the prediction model.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Form (Groups all inputs) */}
        <div className="lg:col-span-8 bg-white border border-slate-200/65 rounded-2xl p-6 md:p-8 shadow-sm flex flex-col gap-6">
          <form onSubmit={handleSubmit} className="flex flex-col gap-8">
            
            {error && (
              <div className="flex items-center gap-3 p-4 rounded-xl bg-rose-50 border border-rose-100 text-rose-800 text-sm">
                <AlertTriangle className="h-5 w-5 text-rose-600 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* 🌱 Section 1: Soil Information */}
            <div>
              <div className="flex items-center gap-2 pb-3 mb-5 border-b border-slate-100">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600">
                  <Sprout className="h-4 w-4" />
                </div>
                <h3 className="text-base font-bold text-slate-800">Soil Information</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                {/* Nitrogen */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Nitrogen (N)</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 140 kg/ha</span>
                  </div>
                  <div className="relative flex items-center">
                    <Hash className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="N" 
                      value={formData.N} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 80" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Supports vegetative growth & foliage.</span>
                </div>

                {/* Phosphorus */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Phosphorus (P)</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 145 kg/ha</span>
                  </div>
                  <div className="relative flex items-center">
                    <Hash className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="P" 
                      value={formData.P} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 50" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Aids root development & maturation.</span>
                </div>

                {/* Potassium */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Potassium (K)</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 205 kg/ha</span>
                  </div>
                  <div className="relative flex items-center">
                    <Hash className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="K" 
                      value={formData.K} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 40" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Improves stress tolerance & quality.</span>
                </div>

                {/* Soil pH */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Soil pH</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 14</span>
                  </div>
                  <div className="relative flex items-center">
                    <Droplet className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="ph" 
                      value={formData.ph} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 6.5" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Acidity/alkalinity indicator.</span>
                </div>

                {/* Soil Type */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Soil Type</label>
                  <div className="relative flex items-center">
                    <Layers className="absolute left-3 w-4 h-4 text-slate-400" />
                    <select 
                      name="soilType"
                      value={formData.soilType}
                      onChange={handleInputChange}
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800 appearance-none"
                    >
                      <option value="Loamy">Loamy</option>
                      <option value="Clay">Clay</option>
                      <option value="Sandy">Sandy</option>
                      <option value="Silt">Silt</option>
                      <option value="Peaty">Peaty</option>
                    </select>
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">General texture profile.</span>
                </div>

              </div>
            </div>

            {/* 🌦 Section 2: Climate Information */}
            <div>
              <div className="flex items-center gap-2 pb-3 mb-5 border-b border-slate-100">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
                  <CloudRain className="h-4 w-4" />
                </div>
                <h3 className="text-base font-bold text-slate-800">Climate Information</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                {/* Temperature */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Temperature</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 45 °C</span>
                  </div>
                  <div className="relative flex items-center">
                    <Thermometer className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="temperature" 
                      value={formData.temperature} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 25.6" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Seasonal heat levels.</span>
                </div>

                {/* Humidity */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Relative Humidity</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 100 %</span>
                  </div>
                  <div className="relative flex items-center">
                    <Activity className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="humidity" 
                      value={formData.humidity} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 75.0" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Water vapor percentage.</span>
                </div>

                {/* Rainfall */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Rainfall</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 300 mm</span>
                  </div>
                  <div className="relative flex items-center">
                    <CloudRain className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="rainfall" 
                      value={formData.rainfall} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 150.0" 
                      required 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Cumulative water inputs.</span>
                </div>

                {/* Soil Moisture */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Soil Moisture</label>
                    <span className="text-[10px] text-slate-400 font-semibold bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">0 - 100 %</span>
                  </div>
                  <div className="relative flex items-center">
                    <Droplet className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="moisture" 
                      value={formData.moisture} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 45" 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Continuous sensor telemetry (Optional).</span>
                </div>

              </div>
            </div>

            {/* 📍 Section 3: Location Information */}
            <div>
              <div className="flex items-center gap-2 pb-3 mb-5 border-b border-slate-100">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
                  <MapPin className="h-4 w-4" />
                </div>
                <h3 className="text-base font-bold text-slate-800">Location & Operations Information</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                {/* Location Name */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Field Name / Label</label>
                  <div className="relative flex items-center">
                    <MapPin className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="text" 
                      name="locationName" 
                      value={formData.locationName} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. Valley Field 4" 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Unique audit label.</span>
                </div>

                {/* Region */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">State / Region</label>
                  <div className="relative flex items-center">
                    <Globe className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="text" 
                      name="region" 
                      value={formData.region} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. Punjab" 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Geographic zone.</span>
                </div>

                {/* Field Size */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Field Size (Acres)</label>
                  <div className="relative flex items-center">
                    <Maximize2 className="absolute left-3 w-4 h-4 text-slate-400" />
                    <input 
                      type="number" 
                      step="any" 
                      min="0" 
                      name="fieldSize" 
                      value={formData.fieldSize} 
                      onChange={handleInputChange} 
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800" 
                      placeholder="e.g. 15.5" 
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Total operational acreage.</span>
                </div>

                {/* Previous Crop */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Previous Crop</label>
                  <div className="relative flex items-center">
                    <Sprout className="absolute left-3 w-4 h-4 text-slate-400" />
                    <select 
                      name="previousCrop"
                      value={formData.previousCrop}
                      onChange={handleInputChange}
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800 appearance-none"
                    >
                      <option value="None">None</option>
                      <option value="Wheat">Wheat</option>
                      <option value="Maize">Maize</option>
                      <option value="Soybean">Soybean</option>
                      <option value="Paddy">Paddy</option>
                    </select>
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Aids rotation verification.</span>
                </div>

                {/* Irrigation Type */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Irrigation Type</label>
                  <div className="relative flex items-center">
                    <Droplet className="absolute left-3 w-4 h-4 text-slate-400" />
                    <select 
                      name="irrigationType"
                      value={formData.irrigationType}
                      onChange={handleInputChange}
                      className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200/80 rounded-xl text-sm focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none text-slate-800 appearance-none"
                    >
                      <option value="Drip">Drip Irrigation</option>
                      <option value="Sprinkler">Sprinkler</option>
                      <option value="Flood">Flood/Furrow</option>
                      <option value="Rainfed">Rainfed/Natural</option>
                    </select>
                  </div>
                  <span className="text-[10px] text-slate-400 mt-1">Water delivery systems.</span>
                </div>

              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4 border-t border-slate-100 flex justify-end">
              <button 
                type="submit" 
                className="w-full md:w-auto inline-flex items-center justify-center px-8 py-3.5 text-base font-bold text-white bg-emerald-600 hover:bg-emerald-700 active:scale-98 transition-all rounded-xl shadow-lg shadow-emerald-100/50 gap-2"
                disabled={loading}
              >
                <span>{loading ? 'Processing Analysis...' : 'Analyze Field'}</span>
                {loading ? (
                  <span className="spinner-border spinner-border-sm" role="status"></span>
                ) : (
                  <Sprout className="h-5 w-5" />
                )}
              </button>
            </div>

          </form>
        </div>

        {/* Right Column: Insights checklist & History logs */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          
          {/* Analysis Info */}
          <div className="bg-white border border-slate-200/65 rounded-2xl p-5 shadow-sm">
            <h3 className="text-base font-bold text-slate-800 mb-4">Field Analysis Insights</h3>
            <div className="flex flex-col gap-4">
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600 shrink-0">
                  <Cpu className="h-4.5 w-4.5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-800">Automatic Scaling</h4>
                  <p className="text-xs text-slate-500 mt-0.5">Adjusts variances across inputs using a standard scaler to protect accuracy.</p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 shrink-0">
                  <TrendingUp className="h-4.5 w-4.5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-800">2,100 Record Dataset</h4>
                  <p className="text-xs text-slate-500 mt-0.5">Compares metrics across thousands of verified crop climate growing logs.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Audit Banner Tip */}
          <div className="bg-emerald-50/40 border border-emerald-100/50 rounded-2xl p-4 flex gap-3">
            <HelpCircle className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider">Audit Tip</h4>
              <p className="text-xs text-slate-600 mt-1 leading-normal">Evaluate soil properties during seasonal transitions for optimal moisture insights.</p>
            </div>
          </div>

          {/* History logs */}
          {history.length > 0 && (
            <div className="bg-white border border-slate-200/65 rounded-2xl p-5 shadow-sm" id="history-anchor">
              <h3 className="text-base font-bold text-slate-800 mb-3">Recent Analysis Logs</h3>
              <div className="flex flex-col gap-2">
                {history.map((h, i) => (
                  <div 
                    key={i} 
                    className="flex justify-between items-center p-3 rounded-xl bg-slate-50 border border-slate-100 hover:border-slate-300 hover:bg-slate-100/30 transition-all cursor-pointer text-left"
                    onClick={() => loadHistoryItem(h)}
                    title="Click to reload this log into form and run analysis"
                  >
                    <div>
                      <span className="block text-sm font-bold text-slate-800 capitalize">{h.crop}</span>
                      <span className="block text-[10px] text-slate-400 mt-0.5">
                        {h.inputs.locationName ? `${h.inputs.locationName} - ` : ''}N:{h.inputs.N} P:{h.inputs.P} K:{h.inputs.K}
                      </span>
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                      h.confidence >= 70 ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' : 
                      h.confidence >= 40 ? 'bg-sky-50 text-sky-700 border border-sky-100' : 
                      'bg-slate-100 text-slate-600 border border-slate-200'
                    }`}>
                      {h.confidence}% Match
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

      </div>
    </section>
  );
};

export default WorkspaceForm;

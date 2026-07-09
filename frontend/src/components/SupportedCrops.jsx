import React from 'react';
import { Leaf } from 'lucide-react';

export const SupportedCrops = () => {
  const cropClasses = [
    'Rice / Paddy',
    'Maize',
    'Wheat',
    'Sugarcane',
    'Potato',
    'Apple'
  ];

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      
      {/* Title */}
      <div className="text-center mb-10">
        <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest block mb-2">Model Scope</span>
        <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">20+ Supported Crop Classes</h2>
        <p className="text-slate-500 mt-2">Our model is trained to recognize growth parameters for diverse crop categories.</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
        {cropClasses.map((cropName, i) => (
          <div 
            key={i} 
            className="bg-white border border-slate-200/80 rounded-2xl p-5 flex flex-col items-center gap-3 hover:-translate-y-1 hover:shadow-md transition-all shadow-sm group"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 group-hover:scale-105 transition-transform">
              <Leaf className="w-5 h-5" />
            </div>
            <span className="font-extrabold text-sm text-slate-800">{cropName}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

export default SupportedCrops;

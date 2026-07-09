import React from 'react';
import { Cpu, CloudRain, BarChart3 } from 'lucide-react';

export const Features = () => {
  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16" id="features-anchor">
      
      {/* Title */}
      <div className="text-center mb-12">
        <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest block mb-2">Enterprise Capabilities</span>
        <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Smart Agriculture Ecosystem</h2>
        <p className="text-slate-500 mt-2">Explore advanced agricultural features designed to increase crop yields and resource efficiency.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Feature 1 */}
        <div className="bg-white border border-slate-200/80 rounded-2xl p-6 hover:-translate-y-1 hover:shadow-md hover:border-slate-300 transition-all flex flex-col items-center md:items-start text-center md:text-left gap-4 shadow-sm">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 shadow-sm shadow-emerald-100/50">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">AI Crop Classifier</h3>
            <p className="text-sm text-slate-500 mt-2 leading-relaxed">Query state-of-the-art Random Forest classifiers trained on robust local soil diagnostics.</p>
          </div>
        </div>

        {/* Feature 2 */}
        <div className="bg-white border border-slate-200/80 rounded-2xl p-6 hover:-translate-y-1 hover:shadow-md hover:border-slate-300 transition-all flex flex-col items-center md:items-start text-center md:text-left gap-4 shadow-sm">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600 shadow-sm shadow-blue-100/50">
            <CloudRain className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Weather Intelligence</h3>
            <p className="text-sm text-slate-500 mt-2 leading-relaxed">Cross-references rainfall and temperature data to protect crops from climatic changes.</p>
          </div>
        </div>

        {/* Feature 3 */}
        <div className="bg-white border border-slate-200/80 rounded-2xl p-6 hover:-translate-y-1 hover:shadow-md hover:border-slate-300 transition-all flex flex-col items-center md:items-start text-center md:text-left gap-4 shadow-sm">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 shadow-sm shadow-indigo-100/50">
            <BarChart3 className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Yield Diagnostics</h3>
            <p className="text-sm text-slate-500 mt-2 leading-relaxed">Identifies variables preventing optimal growth and lists necessary soil improvements.</p>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Features;

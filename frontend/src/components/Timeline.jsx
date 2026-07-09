import React from 'react';
import { Sliders, BarChart3, Cpu, FileText } from 'lucide-react';

export const Timeline = () => {
  const steps = [
    {
      step: '01',
      icon: <Sliders className="w-5 h-5 text-emerald-600" />,
      title: 'Telemetry Input',
      description: 'Submit Nitrogen, Phosphorus, Potassium, temperature, and moisture variables from local field readings.'
    },
    {
      step: '02',
      icon: <BarChart3 className="w-5 h-5 text-emerald-600" />,
      title: 'Standardization',
      description: 'Inputs are scaled through a standard scaler to adjust variances and ensure correct classification weights.'
    },
    {
      step: '03',
      icon: <Cpu className="w-5 h-5 text-emerald-600" />,
      title: 'AI Classification',
      description: 'A trained Random Forest model parses variables across decision trees to calculate suitability probabilities.'
    },
    {
      step: '04',
      icon: <FileText className="w-5 h-5 text-emerald-600" />,
      title: 'Actionable Report',
      description: 'The system generates growing profiles, matching indicators, and corrective advice for your land.'
    }
  ];

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12" id="timeline-anchor">
      
      {/* Title */}
      <div className="text-center mb-12">
        <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest block mb-2">Interactive Process</span>
        <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Agronomical Analysis Pipeline</h2>
        <p className="text-slate-500 mt-2">Learn how OPTI-CROP converts raw environmental variables into verified farming recommendations in four steps.</p>
      </div>

      {/* Grid of Steps */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {steps.map((s, i) => (
          <div 
            key={i} 
            className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm flex flex-col justify-between hover:shadow-md hover:border-slate-300 transition-all text-left group relative"
          >
            <div className="flex flex-col gap-4">
              <div className="flex justify-between items-center">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 group-hover:scale-105 transition-transform">
                  {s.icon}
                </div>
                <span className="text-xs font-black text-slate-350 tracking-wider">STEP {s.step}</span>
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 leading-snug">{s.title}</h3>
                <p className="text-xs text-slate-500 mt-2 leading-relaxed">{s.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Timeline;

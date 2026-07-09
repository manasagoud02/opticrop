import React from 'react';
import { Sparkles, ArrowRight, CloudSun, CheckCircle } from 'lucide-react';

export const Hero = () => {
  const handleScrollToWorkspace = (e) => {
    e.preventDefault();
    const element = document.getElementById('workspace-anchor');
    if (element) {
      const headerOffset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    }
  };

  const handleScrollToFeatures = (e) => {
    e.preventDefault();
    const element = document.getElementById('features-anchor');
    if (element) {
      const headerOffset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    }
  };

  return (
    <section className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
      
      {/* Left Column */}
      <div className="lg:col-span-7 flex flex-col items-start text-left animate-slide-up">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100 shadow-sm mb-6">
          <Sparkles className="h-3.5 w-3.5 text-emerald-600" />
          <span>Enterprise AI Engine v2.4</span>
        </div>
        
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-black text-slate-900 tracking-tight leading-tight">
          Predict field suitability. <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-blue-600">
            Maximize crop yield.
          </span>
        </h1>
        
        <p className="text-lg text-slate-500 mt-6 leading-relaxed max-w-xl">
          OPTI-CROP integrates precision agronomical sensors and machine learning to analyze your soil, humidity, and temperature. Receive instant cultivation suitability advice.
        </p>
        
        <div className="flex flex-wrap gap-3 mt-8">
          <a 
            href="#workspace-anchor" 
            className="inline-flex items-center justify-center px-6 py-3.5 text-base font-bold text-white bg-emerald-600 hover:bg-emerald-700 hover:shadow-lg hover:shadow-emerald-100/50 transition-all rounded-xl shadow-md gap-2"
            onClick={handleScrollToWorkspace}
          >
            <span>Launch Analysis</span>
            <ArrowRight className="h-5 w-5" />
          </a>
          <a 
            href="#features-anchor" 
            className="inline-flex items-center justify-center px-6 py-3.5 text-base font-semibold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors shadow-sm"
            onClick={handleScrollToFeatures}
          >
            <span>Explore Platform</span>
          </a>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-3 gap-4 mt-12 w-full max-w-lg border-t border-slate-100 pt-8">
          <div>
            <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">AI Model</span>
            <strong className="block text-lg font-black text-emerald-600 mt-1">Random Forest</strong>
          </div>
          <div>
            <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">Accuracy</span>
            <strong className="block text-lg font-black text-slate-900 mt-1">92.4% Verified</strong>
          </div>
          <div>
            <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">Inference</span>
            <strong className="block text-lg font-black text-slate-900 mt-1">&lt; 50ms Speed</strong>
          </div>
        </div>
      </div>

      {/* Right Column: 3D perspective preview */}
      <div className="lg:col-span-5 relative w-full flex justify-center animate-fade-in">
        <div className="relative w-full max-w-[420px] aspect-[4/3] rounded-3xl bg-slate-100/50 border border-slate-200/50 p-6 flex flex-col justify-between overflow-hidden shadow-inner">
          <div className="absolute top-0 right-0 w-48 h-48 bg-blue-400/10 blur-3xl rounded-full"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-emerald-400/10 blur-3xl rounded-full"></div>

          {/* Floating Widget 1: Atmosphere */}
          <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-md w-3/4 self-start transform -rotate-2 hover:rotate-0 transition-transform duration-300">
            <div className="flex justify-between items-center border-b border-slate-50 pb-2 mb-2">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Atmosphere telemetry</span>
              <CloudSun className="h-4.5 w-4.5 text-blue-500" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-black text-slate-800">27°C</span>
              <span className="text-xs text-slate-500 font-medium">Temp average</span>
            </div>
            <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-slate-50 text-[11px]">
              <div>
                <span className="text-slate-400 block">Humidity</span>
                <strong className="text-slate-800">82%</strong>
              </div>
              <div>
                <span className="text-slate-400 block">Rainfall</span>
                <strong className="text-slate-800">200mm</strong>
              </div>
            </div>
          </div>

          {/* Floating Widget 2: Crop Suitability */}
          <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-md w-3/4 self-end transform rotate-3 hover:rotate-0 transition-transform duration-300 -mt-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Soil Match Score</span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-100">
                <CheckCircle className="w-3 h-3" />
                <span>98% Fit</span>
              </span>
            </div>
            <h3 className="text-lg font-black text-slate-900">Rice / Paddy</h3>
            <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-slate-50 text-[11px]">
              <div>
                <span className="text-slate-400 block">Exp. Yield</span>
                <strong className="text-slate-800">12.5 T/Ha</strong>
              </div>
              <div>
                <span className="text-slate-400 block">Profit Forecast</span>
                <strong className="text-emerald-600">+$2,450</strong>
              </div>
            </div>
          </div>

          {/* Floating Widget 3: Sparkline */}
          <div className="bg-white border border-slate-200/60 rounded-xl p-3 shadow-md w-1/2 self-start transform -rotate-1 hover:rotate-0 transition-transform duration-300">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Inference confidence</span>
            <svg className="w-full h-8" viewBox="0 0 100 30">
              <path d="M0,25 Q15,5 30,20 T60,5 T90,25 T100,10" fill="none" stroke="url(#cyanGrad)" strokeWidth="2.5" strokeLinecap="round" />
              <defs>
                <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#2563EB" />
                  <stop offset="100%" stopColor="#10B981" />
                </linearGradient>
              </defs>
            </svg>
          </div>

        </div>
      </div>
    </section>
  );
};

export default Hero;

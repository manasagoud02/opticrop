import React from 'react';
import { Sprout, Search } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const Header = ({ onOpenPalette }) => {
  const { history } = useApp();

  const handleScrollTo = (e, id) => {
    e.preventDefault();
    const element = document.getElementById(id);
    if (element) {
      const headerOffset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-slate-200/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between gap-4">
          
          {/* Logo Brand */}
          <div className="flex items-center gap-6">
            <a 
              href="/" 
              className="flex items-center gap-2 text-slate-900 hover:opacity-90 transition-opacity"
              onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-600 text-white shadow-md shadow-emerald-200/50">
                <Sprout className="h-5 w-5" />
              </div>
              <span className="font-display text-lg font-black tracking-tight uppercase">OPTI-CROP</span>
            </a>

            {/* Navigation links */}
            <nav className="hidden md:flex items-center gap-6">
              <a 
                href="#" 
                className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors"
                onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
              >
                Overview
              </a>
              <a 
                href="#workspace-anchor" 
                className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors"
                onClick={(e) => handleScrollTo(e, 'workspace-anchor')}
              >
                Workspace
              </a>
              <a 
                href="#features-anchor" 
                className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors"
                onClick={(e) => handleScrollTo(e, 'features-anchor')}
              >
                Features
              </a>
              <a 
                href="#faq-anchor" 
                className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors"
                onClick={(e) => handleScrollTo(e, 'faq-anchor')}
              >
                FAQ
              </a>
              {history.length > 0 && (
                <a 
                  href="#history-anchor" 
                  className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors"
                  onClick={(e) => handleScrollTo(e, 'history-anchor')}
                >
                  Analysis Logs
                </a>
              )}
            </nav>
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-3">
            <button 
              className="inline-flex items-center gap-2 px-3 py-1.5 text-xs font-semibold text-slate-400 bg-slate-50 border border-slate-200 rounded-xl hover:bg-slate-100 hover:text-slate-600 transition-all shadow-sm"
              onClick={onOpenPalette} 
              aria-label="Search Command Palette"
            >
              <Search className="h-3.5 w-3.5" />
              <span>Search console...</span>
              <kbd className="hidden sm:inline-flex h-4 items-center gap-0.5 rounded border border-slate-250 bg-white px-1 text-[10px] font-medium text-slate-400 shadow-sm ml-2">Ctrl K</kbd>
            </button>
            
            <a 
              href="#workspace-anchor" 
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 active:scale-95 transition-all rounded-xl shadow-md shadow-emerald-100/50 gap-2"
              onClick={(e) => handleScrollTo(e, 'workspace-anchor')}
            >
              <Sprout className="h-4 w-4" />
              <span>Analyze Field</span>
            </a>
          </div>

        </div>
      </div>
    </header>
  );
};

export default Header;

import React from 'react';
import { Sprout } from 'lucide-react';

export const Footer = () => {
  const handleScrollTo = (e, id) => {
    e.preventDefault();
    const element = document.getElementById(id);
    if (element) {
      const headerOffset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    }
  };

  return (
    <footer className="w-full bg-white border-t border-slate-200/50 mt-16 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Top links grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pb-10 border-b border-slate-100">
          
          {/* Brand Info */}
          <div className="md:col-span-5 flex flex-col items-start text-left gap-4">
            <a 
              href="/" 
              className="flex items-center gap-2"
              onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-600 text-white shadow-sm">
                <Sprout className="h-4.5 w-4.5" />
              </div>
              <span className="font-display text-base font-black tracking-tight uppercase text-slate-900">OPTI-CROP</span>
            </a>
            <p className="text-sm text-slate-500 leading-relaxed max-w-sm">
              Empowering agronomists and farmers with precision soil diagnostics and machine learning classifications.
            </p>
            <div className="flex items-center gap-3 mt-2">
              {/* Social icons */}
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-50 border border-slate-200 text-slate-400 hover:text-slate-650 hover:bg-slate-100 transition-colors" aria-label="Twitter">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/>
                </svg>
              </a>
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-50 border border-slate-200 text-slate-400 hover:text-slate-650 hover:bg-slate-100 transition-colors" aria-label="Github">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482C19.138 20.193 22 16.44 22 12.017 22 6.484 17.522 2 12 2z"/>
                </svg>
              </a>
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-50 border border-slate-200 text-slate-400 hover:text-slate-650 hover:bg-slate-100 transition-colors" aria-label="LinkedIn">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764.784-1.764 1.75-1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Links Column 1 */}
          <div className="md:col-span-2 md:col-start-7 flex flex-col items-start gap-3">
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-widest">Platform</h4>
            <ul className="flex flex-col gap-2 text-sm text-slate-500">
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>Overview</a></li>
              <li><a href="#workspace-anchor" className="hover:text-slate-950 transition-colors" onClick={(e) => handleScrollTo(e, 'workspace-anchor')}>Workspace</a></li>
              <li><a href="#timeline-anchor" className="hover:text-slate-950 transition-colors" onClick={(e) => handleScrollTo(e, 'timeline-anchor')}>Process</a></li>
            </ul>
          </div>

          {/* Links Column 2 */}
          <div className="md:col-span-2 flex flex-col items-start gap-3">
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-widest">Resources</h4>
            <ul className="flex flex-col gap-2 text-sm text-slate-500">
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => e.preventDefault()}>Documentation</a></li>
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => e.preventDefault()}>Telemetry API</a></li>
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => e.preventDefault()}>Help Desk</a></li>
            </ul>
          </div>

          {/* Links Column 3 */}
          <div className="md:col-span-2 flex flex-col items-start gap-3">
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-widest">Company</h4>
            <ul className="flex flex-col gap-2 text-sm text-slate-500">
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => e.preventDefault()}>About Us</a></li>
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => e.preventDefault()}>Careers</a></li>
              <li><a href="#" className="hover:text-slate-950 transition-colors" onClick={(e) => e.preventDefault()}>Contact</a></li>
            </ul>
          </div>

        </div>

        {/* Bottom copyright */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-8 text-xs text-slate-400">
          <span>&copy; 2026 OPTI-CROP. All rights reserved. Precision Agronomy Workspace.</span>
          <div className="flex gap-4">
            <a href="#" className="hover:text-slate-600 transition-colors" onClick={(e) => e.preventDefault()}>Privacy Policy</a>
            <a href="#" className="hover:text-slate-600 transition-colors" onClick={(e) => e.preventDefault()}>Terms of Service</a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;

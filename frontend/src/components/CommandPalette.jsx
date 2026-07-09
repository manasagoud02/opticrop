import React, { useEffect, useRef, useState } from 'react';
import { Search, Sprout, Cpu, HelpCircle, History } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const CommandPalette = ({ isOpen, onClose }) => {
  const { history } = useApp();
  const [searchQuery, setSearchQuery] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 50);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleCommandClick = (anchorId) => {
    onClose();
    const element = document.getElementById(anchorId);
    if (element) {
      const headerOffset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    }
  };

  const commands = [
    {
      id: 'workspace',
      label: 'Navigate to Workspace Form',
      anchor: 'workspace-anchor',
      icon: <Sprout className="w-5 h-5 text-slate-400" />
    },
    {
      id: 'features',
      label: 'Explore Ecosystem Features',
      anchor: 'features-anchor',
      icon: <Cpu className="w-5 h-5 text-slate-400" />
    },
    {
      id: 'faq',
      label: 'Browse Platform FAQ',
      anchor: 'faq-anchor',
      icon: <HelpCircle className="w-5 h-5 text-slate-400" />
    },
    ...(history.length > 0 ? [{
      id: 'history',
      label: 'Inspect Analysis Logs',
      anchor: 'history-anchor',
      icon: <History className="w-5 h-5 text-slate-400" />
    }] : [])
  ];

  const filteredCommands = commands.filter(cmd => 
    cmd.label.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div 
      className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-[9999] flex items-center justify-center p-4" 
      id="cmdPaletteBackdrop"
      onClick={(e) => { if (e.target.id === 'cmdPaletteBackdrop') onClose(); }}
    >
      <div className="w-full max-w-lg bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden animate-scale-in">
        
        {/* Search Input Row */}
        <div className="flex items-center gap-3 px-4 py-3.5 border-b border-slate-100">
          <Search className="w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            ref={inputRef}
            id="cmdPaletteSearch" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Type a command or query..." 
            aria-label="Search Command Palette"
            className="w-full text-sm text-slate-800 placeholder-slate-400 bg-transparent outline-none border-none focus:ring-0"
          />
        </div>

        {/* Results List */}
        <ul className="max-h-72 overflow-y-auto p-2">
          {filteredCommands.length > 0 ? (
            filteredCommands.map((cmd) => (
              <li 
                key={cmd.id} 
                className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 hover:bg-slate-50 hover:text-slate-950 cursor-pointer transition-colors text-sm font-semibold" 
                onClick={() => handleCommandClick(cmd.anchor)}
              >
                {cmd.icon}
                <span>{cmd.label}</span>
              </li>
            ))
          ) : (
            <li className="px-4 py-3 text-xs text-slate-400 font-medium">
              <span>No commands found matching "{searchQuery}"</span>
            </li>
          )}
        </ul>

        {/* Console Footer */}
        <div className="flex justify-between px-4 py-2.5 bg-slate-50 border-t border-slate-100 text-[10px] text-slate-400 font-bold uppercase tracking-wider">
          <span><kbd className="bg-white border border-slate-200 px-1 py-0.5 rounded shadow-sm text-slate-500 font-black">Esc</kbd> Close</span>
          <span><kbd className="bg-white border border-slate-200 px-1 py-0.5 rounded shadow-sm text-slate-500 font-black">Enter</kbd> Select</span>
        </div>

      </div>
    </div>
  );
};

export default CommandPalette;

import React, { useState, useEffect } from 'react';
import { MessageSquare } from 'lucide-react';
import { useApp } from './context/AppContext';
import Header from './components/Header';
import Hero from './components/Hero';
import Timeline from './components/Timeline';
import WorkspaceForm from './components/WorkspaceForm';
import ResultsView from './components/ResultsView';
import Features from './components/Features';
import SupportedCrops from './components/SupportedCrops';
import FaqAccordion from './components/FaqAccordion';
import Footer from './components/Footer';
import CommandPalette from './components/CommandPalette';
import ToastContainer from './components/ToastContainer';

export const App = () => {
  const { launchToast } = useApp();
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [scrollWidth, setScrollWidth] = useState('0%');

  // Handle Scroll Progress Indicator
  useEffect(() => {
    const handleScroll = () => {
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (height > 0) {
        const scrolled = (winScroll / height) * 100;
        setScrollWidth(`${scrolled}%`);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Handle Global Ctrl+K trigger for Command Palette
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        setPaletteOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
  return (
    <div className="min-h-screen bg-slate-50/50 text-slate-900">
      {/* Scroll Progress Indicator */}
      <div 
        className="scroll-progress" 
        id="scrollIndicator" 
        style={{ width: scrollWidth, display: 'block' }}
      ></div>

      <Header onOpenPalette={() => setPaletteOpen(true)} />

      <main className="space-y-4">
        <Hero />
        <Timeline />
        <WorkspaceForm />
        <ResultsView />
        <Features />
        <SupportedCrops />
        <FaqAccordion />
      </main>

      <Footer />

      {/* Floating Help Button */}
      <button 
        className="floating-help-btn" 
        id="helpBtn" 
        onClick={() => launchToast('Agtech Help Center is currently offline. Please try again later.', 'error')}
        aria-label="Help Center Dialog"
      >
        <MessageSquare style={{ width: '24px', height: '24px' }} />
      </button>

      {/* Command Palette Overlay Modal */}
      <CommandPalette isOpen={paletteOpen} onClose={() => setPaletteOpen(false)} />

      {/* Custom Toast Notifications Center */}
      <ToastContainer />
    </div>
  );
};

export default App;

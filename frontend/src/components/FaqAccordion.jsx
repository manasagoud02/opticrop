import React, { useState } from 'react';
import { ChevronDown, HelpCircle } from 'lucide-react';

export const FaqAccordion = () => {
  const [activeIndex, setActiveIndex] = useState(null);

  const faqData = [
    {
      question: 'How accurate are these crop recommendations?',
      answer: 'Our Random Forest Classifier achieves a verified 92.4% prediction accuracy score on independent test splits, validating its ability to match local parameters with historical crops records.'
    },
    {
      question: 'What do the low/high corrective badges represent?',
      answer: 'If a parameter in your field deviates by more than 15% from the ideal crop requirement, the system generates corrective checklists to guide your fertilization or soil preparation actions.'
    },
    {
      question: 'Are these predictions processed locally?',
      answer: 'Yes. The Flask server runs the compiled model artifacts (crop_recommendation_model.pkl) locally to process predictions in less than 50 milliseconds without calling external APIs.'
    }
  ];

  const handleToggle = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  return (
    <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16" id="faq-anchor">
      
      {/* Title */}
      <div className="text-center mb-10">
        <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest block mb-2">Assistance</span>
        <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Frequently Asked Questions</h2>
        <p className="text-slate-500 mt-2">Quick answers to common questions about our soil suitability prediction model.</p>
      </div>

      <div className="flex flex-col gap-4">
        {faqData.map((faq, i) => {
          const isActive = activeIndex === i;
          return (
            <div 
              key={i} 
              className="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-xs hover:border-slate-350 transition-all duration-300"
            >
              <button 
                type="button"
                className="w-full flex items-center justify-between px-6 py-4.5 text-left font-extrabold text-slate-800 text-sm md:text-base outline-none gap-4"
                onClick={() => handleToggle(i)}
                aria-expanded={isActive}
              >
                <span className="flex items-center gap-3">
                  <HelpCircle className="w-5 h-5 text-emerald-500 shrink-0" />
                  <span>{faq.question}</span>
                </span>
                <ChevronDown className="w-5 h-5 text-slate-400 shrink-0 transition-transform duration-300" style={{ 
                  transform: isActive ? 'rotate(180deg)' : 'rotate(0deg)'
                }} />
              </button>
              <div 
                className="transition-all duration-300 ease-in-out" 
                style={{ 
                  maxHeight: isActive ? '180px' : '0px',
                  overflow: 'hidden'
                }}
              >
                <div className="px-6 pb-6 pt-1 text-slate-500 text-xs md:text-sm leading-relaxed border-t border-slate-50">
                  {faq.answer}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default FaqAccordion;

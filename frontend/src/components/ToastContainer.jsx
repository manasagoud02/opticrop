import React from 'react';
import { CheckCircle, AlertTriangle } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const ToastContainer = () => {
  const { toasts } = useApp();

  return (
    <div className="fixed bottom-6 left-6 flex flex-col gap-2 z-[9999] pointer-events-none" id="toastCenter">
      {toasts.map((toast) => {
        const isSuccess = toast.type === 'success';
        const accentClass = isSuccess ? 'border-l-4 border-l-emerald-500' : 'border-l-4 border-l-rose-500';
        
        return (
          <div 
            key={toast.id} 
            className={`pointer-events-auto flex items-center gap-3 px-4 py-3 bg-white border border-slate-200/80 ${accentClass} rounded-r-xl shadow-lg max-w-sm min-w-[280px] animate-scale-in`}
          >
            {isSuccess ? (
              <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" />
            )}
            <div className="text-xs font-bold leading-normal text-slate-800">{toast.message}</div>
          </div>
        );
      })}
    </div>
  );
};

export default ToastContainer;

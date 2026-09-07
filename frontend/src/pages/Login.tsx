import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, Fingerprint } from 'lucide-react';

export default function Login() {
  const navigate = useNavigate();
  const [badge, setBadge] = useState('INV-7734');
  const [pin, setPin] = useState('••••••');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#0A0C0E]">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-refraction-glow pointer-events-none" />
      
      <div className="luminosity-card p-12 w-full max-w-md relative z-10">
        <div className="flex flex-col items-center mb-12">
          <ShieldAlert size={48} className="text-[#E8913C] mb-6" />
          <h1 className="text-3xl text-center">SYSTEM AUTH</h1>
          <span className="technical-label mt-4">RESTRICTED ACCESS ONLY</span>
        </div>

        <form onSubmit={handleLogin} className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label className="technical-label">BADGE ID</label>
            <input 
              type="text" 
              value={badge}
              onChange={(e) => setBadge(e.target.value)}
              className="bg-[#101317] border border-[rgba(237,231,220,0.13)] rounded-lg p-4 font-mono text-[#EDE7DC] focus:border-[#E8913C] focus:outline-none transition-colors"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="technical-label">SECURITY PIN</label>
            <input 
              type="password" 
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              className="bg-[#101317] border border-[rgba(237,231,220,0.13)] rounded-lg p-4 font-mono text-[#EDE7DC] focus:border-[#E8913C] focus:outline-none transition-colors"
            />
          </div>

          <button type="submit" className="laser-button mt-4 flex items-center justify-center gap-2">
            <Fingerprint size={18} />
            AUTHENTICATE
          </button>
        </form>
        
        <div className="mt-8 pt-8 border-t border-[rgba(237,231,220,0.13)] flex justify-between items-center text-[#6C7378]">
          <span className="technical-label">SECURE HASH: SHA-256</span>
          <span className="technical-label">NODE: 09</span>
        </div>
      </div>
    </div>
  );
}

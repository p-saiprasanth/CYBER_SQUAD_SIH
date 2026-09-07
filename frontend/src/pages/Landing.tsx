import React, { useEffect, useRef } from 'react';
import { PillNav } from '../components/PillNav';
import { ShieldAlert, Fingerprint, Network, ServerCrash, Cpu } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import gsap from 'gsap';

export default function Landing() {
  const navigate = useNavigate();
  const heroRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll reveal effects
    const elements = document.querySelectorAll('.scroll-reveal');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          gsap.to(entry.target, {
            y: 0,
            opacity: 1,
            duration: 0.8,
            ease: "cubic-bezier(0.16, 1, 0.3, 1)"
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    elements.forEach(el => {
      gsap.set(el, { y: 40, opacity: 0 });
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const navItems = [
    { label: 'Platform', href: '#platform' },
    { label: 'Capabilities', href: '#capabilities' },
    { label: 'System', href: '#system' }
  ];

  return (
    <div className="min-h-screen flex flex-col relative w-full overflow-hidden">
      <div className="bg-refraction-glow absolute top-0 left-0 w-full h-[800px] pointer-events-none -z-10" />
      
      <header className="w-full fixed top-0 z-[100] pt-6">
        <PillNav 
          logo={<ShieldAlert size={20} className="text-[#0A0C0E]" />}
          items={navItems}
          baseColor="#E8913C"
          pillColor="#101317"
          pillTextColor="white"
          hoveredPillTextColor="#000000"
        />
      </header>

      <main className="flex-grow pt-40 px-4 md:px-8 max-w-[1600px] mx-auto w-full">
        {/* HERO */}
        <section className="flex flex-col items-center justify-center min-h-[70vh] text-center scroll-reveal relative">
          <div 
            className="absolute -z-10 w-full h-full max-w-4xl mx-auto rounded-none border border-[rgba(237,231,220,0.13)] bg-white/5 backdrop-blur-md"
            style={{ transform: 'perspective(1000px) rotateX(15deg) scale(0.9)', bottom: '-10%' }}
          ></div>

          <div className="border-[12px] border-white px-8 py-12 md:py-16 md:px-24 mb-12 bg-[#0A0C0E]">
            <h1 className="text-[clamp(2.6rem,8vw,7rem)] leading-[0.9] text-[#EDE7DC]">
              AI-POWERED <br />
              <span className="text-[#E8913C]">CRIMINAL NETWORK</span><br />
              INTELLIGENCE
            </h1>
          </div>
          
          <div className="flex flex-col md:flex-row w-full max-w-4xl mx-auto justify-between items-center gap-8 border-t border-[rgba(237,231,220,0.2)] pt-8 mt-4">
            <div className="flex flex-col items-start gap-2">
              <span className="technical-label">SYS.STATUS // ACTIVE</span>
              <span className="technical-label">LOC // SECURE_NODE_09</span>
            </div>
            
            <button 
              onClick={() => navigate('/login')}
              className="laser-button"
            >
              Initialize System
            </button>
            
            <div className="flex flex-col items-end gap-2 text-right">
              <span className="technical-label text-[#E8913C]">T-MINUS</span>
              <span className="font-jakarta font-bold text-3xl tabular-nums tracking-tighter">
                24:00:00
              </span>
            </div>
          </div>
        </section>

        {/* BENTO GRID */}
        <section id="capabilities" className="py-32 scroll-reveal">
          <div className="flex flex-col gap-4 mb-16">
            <span className="technical-label text-[#E8913C]">01 / CORE MODULES</span>
            <h2 className="text-4xl md:text-5xl">INVESTIGATIVE PIPELINE</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="luminosity-card p-10 flex flex-col min-h-[450px]">
              <div className="technical-label mb-auto">MOD_A / EXTRACTION</div>
              <Cpu size={48} className="text-[#E8913C] mb-8" />
              <h3 className="text-3xl mb-4">ENTITY RESOLUTION</h3>
              <p className="text-[#9EA5A8] font-inter font-light">
                Transforms synthetic investigation data into evidence-linked entities. Identifies persons, organizations, locations, and assets from raw text using advanced NLP pipelines.
              </p>
            </div>
            
            <div className="luminosity-card p-10 flex flex-col min-h-[450px]">
              <div className="technical-label mb-auto">MOD_B / GRAPH</div>
              <Network size={48} className="text-[#E8913C] mb-8" />
              <h3 className="text-3xl mb-4">KNOWLEDGE GRAPH</h3>
              <p className="text-[#9EA5A8] font-inter font-light">
                Visualizes complex relationships through Cytoscape.js. Zoom, pan, and filter massive criminal networks to uncover hidden structural associations in real-time.
              </p>
            </div>
            
            <div className="luminosity-card p-10 flex flex-col min-h-[450px]">
              <div className="technical-label mb-auto">MOD_C / AI</div>
              <Fingerprint size={48} className="text-[#E8913C] mb-8" />
              <h3 className="text-3xl mb-4">LINK PREDICTION</h3>
              <p className="text-[#9EA5A8] font-inter font-light">
                Graph Neural Networks predict potential unobserved associations. Generates investigative leads backed by evidence integrity, without autonomous criminal declarations.
              </p>
            </div>
          </div>
        </section>

        {/* SOCIAL PROOF & FORM */}
        <section id="system" className="py-32 pb-40 scroll-reveal border-t border-[rgba(237,231,220,0.13)] flex flex-col items-center text-center">
          <span className="technical-label mb-12">CYBER SQUAD / SECURE ACCESS</span>
          
          <div className="flex -space-x-4 mb-12">
            {[1,2,3,4,5].map((i) => (
              <div key={i} className="w-16 h-16 rounded-full border-2 border-[#E8913C] shadow-[0_0_15px_rgba(191,255,0,0.2)] bg-[#101317] flex items-center justify-center">
                <span className="technical-label text-[#E8913C] m-0 tracking-normal">OP_{i}</span>
              </div>
            ))}
          </div>

          <h2 className="text-3xl md:text-5xl mb-12 max-w-2xl">
            REQUEST CLEARANCE FOR INVESTIGATIVE DASHBOARD
          </h2>

          <div className="flex p-2 rounded-full bg-white/5 border border-[rgba(237,231,220,0.13)] backdrop-blur-xl w-full max-w-xl mx-auto">
            <input 
              type="text" 
              placeholder="ENTER BADGE ID..." 
              className="bg-transparent border-none outline-none text-[#EDE7DC] px-6 flex-grow uppercase placeholder:text-[#EDE7DC]/30"
            />
            <button 
              onClick={() => navigate('/login')}
              className="laser-button !px-6 !py-3 text-sm"
            >
              VERIFY
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

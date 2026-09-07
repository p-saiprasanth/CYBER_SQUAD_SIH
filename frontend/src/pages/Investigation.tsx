import React, { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CytoscapeComponent from 'react-cytoscapejs';
import { PillNav } from '../components/PillNav';
import { ShieldAlert, Search, ZoomIn, ZoomOut, Filter, Info, BrainCircuit, Activity, Clock, FileCheck2, AlertTriangle } from 'lucide-react';
import { mockGraphElements, cytoscapeStylesheet } from '../lib/graphData';

export default function Investigation() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [cy, setCy] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Selection states
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [selectedEdge, setSelectedEdge] = useState<any>(null);

  const navItems = [
    { label: 'Back', href: '/dashboard' },
    { label: 'Export Report', href: '#' },
    { label: 'Security Audit', href: '#' }
  ];

  const handleSearch = () => {
    if (!cy || !searchQuery) return;
    
    // Reset selection
    cy.elements().removeClass('highlighted');
    
    // Find node
    const targetNode = cy.nodes().filter((node: any) => 
      node.data('label').toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (targetNode.length > 0) {
      targetNode.select();
      cy.animate({
        fit: {
          eles: targetNode,
          padding: 50
        },
        duration: 1000
      });
      setSelectedNode(targetNode[0].data());
      setSelectedEdge(null);
    }
  };

  useEffect(() => {
    if (cy) {
      cy.on('tap', 'node', (evt: any) => {
        setSelectedNode(evt.target.data());
        setSelectedEdge(null);
      });
      cy.on('tap', 'edge', (evt: any) => {
        setSelectedEdge(evt.target.data());
        setSelectedNode(null);
      });
      cy.on('tap', (evt: any) => {
        if (evt.target === cy) {
          setSelectedNode(null);
          setSelectedEdge(null);
        }
      });
    }
  }, [cy]);

  return (
    <div className="min-h-screen flex flex-col relative w-full overflow-hidden bg-[#0A0C0E]">
      <header className="w-full fixed top-0 z-[100] pt-6 px-4 pointer-events-none">
        <div className="pointer-events-auto">
          <PillNav 
            logo={<ShieldAlert size={20} className="text-[#0A0C0E]" />}
            items={navItems}
            baseColor="#E8913C"
            pillColor="#101317"
            pillTextColor="white"
            hoveredPillTextColor="#000000"
          />
        </div>
      </header>

      <main className="flex-grow pt-24 px-4 pb-4 w-full h-screen flex flex-col md:flex-row gap-4">
        
        {/* GRAPH AREA */}
        <div className="flex-grow relative luminosity-card rounded-none overflow-hidden flex flex-col">
          {/* Top Controls */}
          <div className="absolute top-4 left-4 z-10 flex gap-2 w-full max-w-md">
            <div className="flex bg-[#101317] backdrop-blur-md border border-[rgba(237,231,220,0.13)] p-2 rounded-full w-full">
              <input 
                type="text" 
                placeholder="SEARCH ENTITY (e.g. Raj)..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                className="bg-transparent border-none outline-none text-[#EDE7DC] font-mono text-sm px-4 flex-grow placeholder:text-[#EDE7DC]/30"
              />
              <button onClick={handleSearch} className="p-2 bg-[#E8913C] text-black rounded-full hover:scale-105 transition-transform">
                <Search size={16} />
              </button>
            </div>
          </div>
          
          <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
             <button onClick={() => cy?.zoom(cy.zoom() + 0.1)} className="p-3 bg-[#101317] backdrop-blur-md border border-[rgba(237,231,220,0.13)] rounded-full hover:border-[#E8913C] transition-colors"><ZoomIn size={16} /></button>
             <button onClick={() => cy?.zoom(cy.zoom() - 0.1)} className="p-3 bg-[#101317] backdrop-blur-md border border-[rgba(237,231,220,0.13)] rounded-full hover:border-[#E8913C] transition-colors"><ZoomOut size={16} /></button>
             <button onClick={() => cy?.fit()} className="p-3 bg-[#101317] backdrop-blur-md border border-[rgba(237,231,220,0.13)] rounded-full hover:border-[#E8913C] transition-colors"><Filter size={16} /></button>
          </div>

          <div className="absolute bottom-4 left-4 z-10">
            <span className="technical-label">CASE ID: {id} // GRAPH VISUALIZATION ACTIVE</span>
          </div>

          <CytoscapeComponent 
            elements={mockGraphElements} 
            stylesheet={cytoscapeStylesheet}
            style={{ width: '100%', height: '100%' }}
            layout={{ name: 'cose', padding: 50 }}
            cy={(cy) => setCy(cy)}
          />
        </div>

        {/* SIDE PANEL */}
        <div className="w-full md:w-[400px] shrink-0 flex flex-col gap-4 h-full overflow-y-auto pr-2 custom-scrollbar">
          
          {/* ENTITY DETAILS */}
          {selectedNode && (
            <div className="luminosity-card p-6 flex flex-col gap-6">
              <div className="flex items-center gap-4 border-b border-[rgba(237,231,220,0.13)] pb-4">
                <div className="w-12 h-12 bg-white/5 rounded-lg flex items-center justify-center border border-[rgba(237,231,220,0.13)]">
                  <Info className="text-[#E8913C]" size={24} />
                </div>
                <div>
                  <h3 className="text-2xl">{selectedNode.label}</h3>
                  <span className="technical-label text-[#E8913C]">{selectedNode.type}</span>
                </div>
              </div>
              
              <div className="flex flex-col gap-4 font-mono text-sm">
                <div className="flex justify-between border-b border-[rgba(237,231,220,0.05)] pb-2">
                  <span className="text-[#6C7378]">ID</span>
                  <span>{selectedNode.id}</span>
                </div>
                <div className="flex justify-between border-b border-[rgba(237,231,220,0.05)] pb-2">
                  <span className="text-[#6C7378]">ALIASES</span>
                  <span>{selectedNode.aliases || 'N/A'}</span>
                </div>
                <div className="flex justify-between border-b border-[rgba(237,231,220,0.05)] pb-2">
                  <span className="text-[#6C7378]">CONFIDENCE</span>
                  <span className="text-[#E8913C]">99.9%</span>
                </div>
              </div>
            </div>
          )}

          {/* AI POTENTIAL ASSOCIATION PANEL */}
          {selectedEdge?.type === 'PREDICTED' && (
            <div className="luminosity-card p-6 flex flex-col gap-6 border-[#E8913C]/50 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-[#E8913C]" />
              
              <div className="flex items-center gap-4">
                <BrainCircuit className="text-[#E8913C]" size={24} />
                <h3 className="text-xl">INVESTIGATIVE LEAD</h3>
              </div>

              <div className="flex justify-between items-center bg-[#101317] rounded-lg p-4 border border-[rgba(237,231,220,0.05)]">
                <span className="font-mono text-sm">{cy?.getElementById(selectedEdge.source).data('label')}</span>
                <Activity className="text-[#E8913C]" size={16} />
                <span className="font-mono text-sm">{cy?.getElementById(selectedEdge.target).data('label')}</span>
              </div>

              <div className="flex flex-col gap-2">
                <span className="technical-label">AI CONFIDENCE SCORE</span>
                <div className="w-full bg-white/5 rounded-full h-2 overflow-hidden">
                  <div className="bg-[#E8913C] h-full" style={{ width: `${selectedEdge.confidence}%` }} />
                </div>
                <span className="text-right font-mono text-xs text-[#E8913C]">{selectedEdge.confidence}%</span>
              </div>

              <div className="flex flex-col gap-2">
                <span className="technical-label">PREDICTION REASONS</span>
                <ul className="font-mono text-xs flex flex-col gap-2 text-[#EDE7DC]">
                  <li className="flex items-center gap-2"><div className="w-1 h-1 bg-[#E8913C] rounded-full" /> Shared contact (+91-9876543210)</li>
                  <li className="flex items-center gap-2"><div className="w-1 h-1 bg-[#E8913C] rounded-full" /> Network proximity (Depth 2)</li>
                </ul>
              </div>
            </div>
          )}

          {/* EVIDENCE PANEL */}
          <div className="luminosity-card p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between border-b border-[rgba(237,231,220,0.13)] pb-4">
              <div className="flex items-center gap-2">
                <FileCheck2 className="text-[#E8913C]" size={20} />
                <h3 className="text-lg">EVIDENCE CHAIN</h3>
              </div>
              <span className="technical-label">LEDGER</span>
            </div>
            
            <div className="flex flex-col gap-3">
              <div className="bg-black/40 border border-[rgba(237,231,220,0.05)] rounded-lg p-4 flex flex-col gap-2">
                <div className="flex justify-between items-start">
                  <span className="font-mono font-bold">E001</span>
                  <span className="technical-label text-[#E8913C] flex items-center gap-1"><FileCheck2 size={10}/> VERIFIED</span>
                </div>
                <p className="font-inter text-sm text-[#9EA5A8] text-balance">Surveillance footage corroborating physical presence.</p>
                <span className="technical-label mt-2">HASH: 8f434346648f6b96df89dda901c5176b</span>
              </div>

              {selectedEdge?.type === 'PREDICTED' && (
                <div className="bg-black/40 border border-red-500/30 rounded-lg p-4 flex flex-col gap-2">
                  <div className="flex justify-between items-start">
                    <span className="font-mono font-bold">E002</span>
                    <span className="technical-label text-red-500 flex items-center gap-1"><AlertTriangle size={10}/> INTEGRITY FAILED</span>
                  </div>
                  <p className="font-inter text-sm text-[#9EA5A8] text-balance">Unverified intercept log.</p>
                  <span className="technical-label mt-2 text-red-500/70">HASH MISMATCH DETECTED</span>
                </div>
              )}
            </div>
          </div>

          {/* TIMELINE */}
          <div className="luminosity-card p-6 flex flex-col gap-4">
             <div className="flex items-center gap-2 border-b border-[rgba(237,231,220,0.13)] pb-4">
                <Clock className="text-[#E8913C]" size={20} />
                <h3 className="text-lg">EVENT TIMELINE</h3>
              </div>
              
              <div className="flex flex-col relative pl-4 mt-2">
                <div className="absolute top-0 left-0 w-[1px] h-full bg-white/10" />
                
                {[
                  { t: '10:30', desc: 'Call intercepted (n4 to n5)' },
                  { t: '12:00', desc: 'Location visit (WH-04)' },
                  { t: '14:00', desc: 'Transaction (ACCT-9921)' },
                  { t: '16:30', desc: 'Meeting (Event-01)' }
                ].map((ev, i) => (
                  <div key={i} className="flex flex-col gap-1 mb-4 relative">
                    <div className="absolute -left-[21px] top-1.5 w-2 h-2 rounded-full bg-[#E8913C]" />
                    <span className="font-mono text-xs text-[#E8913C]">{ev.t}</span>
                    <span className="font-inter text-sm text-[#EDE7DC]">{ev.desc}</span>
                  </div>
                ))}
              </div>
          </div>

        </div>
      </main>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.02);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #E8913C;
        }
      `}</style>
    </div>
  );
}

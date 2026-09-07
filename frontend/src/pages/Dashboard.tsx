import React from 'react';
import { useNavigate } from 'react-router-dom';
import { PillNav } from '../components/PillNav';
import { ShieldAlert, FolderOpen, Network, Database, Activity } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();

  const navItems = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Entities', href: '#' },
    { label: 'Reports', href: '#' },
    { label: 'Logout', href: '/' }
  ];

  const cases = [
    { id: 'C-892', name: 'Operation Iron Vault', status: 'ACTIVE', entities: 142, risk: 'HIGH' },
    { id: 'C-893', name: 'Syndicate Alpha', status: 'ACTIVE', entities: 89, risk: 'CRITICAL' },
    { id: 'C-894', name: 'Nexus Cartel', status: 'PENDING', entities: 34, risk: 'MEDIUM' }
  ];

  return (
    <div className="min-h-screen flex flex-col relative w-full overflow-hidden bg-[#0A0C0E]">
      <header className="w-full fixed top-0 z-[100] pt-6 px-4">
        <PillNav 
          logo={<ShieldAlert size={20} className="text-[#0A0C0E]" />}
          items={navItems}
          activeHref="/dashboard"
          baseColor="#E8913C"
          pillColor="#101317"
          pillTextColor="white"
          hoveredPillTextColor="#000000"
        />
      </header>

      <main className="flex-grow pt-32 px-4 md:px-8 max-w-[1600px] mx-auto w-full flex flex-col gap-8 pb-20">
        
        <div className="flex justify-between items-end mb-8 border-b border-[rgba(237,231,220,0.13)] pb-8">
          <div>
            <span className="technical-label text-[#E8913C] mb-2 block">SYS.DASHBOARD // OVERVIEW</span>
            <h1 className="text-4xl md:text-5xl">INTELLIGENCE COMMAND</h1>
          </div>
          <div className="text-right hidden md:block">
            <span className="technical-label">AGENT: SOURABI</span><br/>
            <span className="technical-label">LAST SYNC: 00:00:12 AGO</span>
          </div>
        </div>

        {/* STATS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          <div className="luminosity-card p-6 flex flex-col gap-4">
            <FolderOpen className="text-[#E8913C]" size={24} />
            <div className="text-4xl font-jakarta font-bold tabular-nums">12</div>
            <span className="technical-label">ACTIVE CASES</span>
          </div>
          <div className="luminosity-card p-6 flex flex-col gap-4">
            <Database className="text-[#E8913C]" size={24} />
            <div className="text-4xl font-jakarta font-bold tabular-nums">1,492</div>
            <span className="technical-label">TOTAL ENTITIES</span>
          </div>
          <div className="luminosity-card p-6 flex flex-col gap-4">
            <Network className="text-[#E8913C]" size={24} />
            <div className="text-4xl font-jakarta font-bold tabular-nums">3,841</div>
            <span className="technical-label">RELATIONSHIPS</span>
          </div>
          <div className="luminosity-card p-6 flex flex-col gap-4">
            <Activity className="text-[#E8913C]" size={24} />
            <div className="text-4xl font-jakarta font-bold tabular-nums">87</div>
            <span className="technical-label">POTENTIAL LEADS</span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          {/* CASES LIST */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl">ACTIVE INVESTIGATIONS</h2>
              <button className="text-[10px] font-mono tracking-widest text-[#E8913C] uppercase hover:underline">View All</button>
            </div>
            
            <div className="flex flex-col gap-4">
              {cases.map((c) => (
                <div 
                  key={c.id} 
                  onClick={() => navigate(`/investigation/${c.id}`)}
                  className="luminosity-card p-6 flex flex-col md:flex-row justify-between items-start md:items-center cursor-pointer group"
                >
                  <div className="flex flex-col gap-1 mb-4 md:mb-0">
                    <span className="technical-label text-[#E8913C]">{c.id}</span>
                    <h3 className="text-xl group-hover:text-[#E8913C] transition-colors">{c.name}</h3>
                  </div>
                  
                  <div className="flex items-center gap-8">
                    <div className="flex flex-col text-right">
                      <span className="technical-label">ENTITIES</span>
                      <span className="font-mono text-sm">{c.entities}</span>
                    </div>
                    <div className="flex flex-col text-right">
                      <span className="technical-label">RISK LEVEL</span>
                      <span className={`font-mono text-sm ${c.risk === 'CRITICAL' ? 'text-red-500' : 'text-[#E8913C]'}`}>{c.risk}</span>
                    </div>
                    <div className="px-4 py-2 rounded-full border border-[rgba(237,231,220,0.2)] text-xs font-mono group-hover:bg-[#E8913C] group-hover:text-black group-hover:border-[#E8913C] transition-colors">
                      OPEN GRAPH
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* RECENT ACTIVITY */}
          <div className="flex flex-col gap-6">
            <h2 className="text-2xl">ACTIVITY LOG</h2>
            <div className="luminosity-card p-6 flex flex-col gap-6 h-full">
              {[
                { time: '10:32:41', action: 'EVIDENCE_VERIFIED', desc: 'Hash matched for E-881' },
                { time: '09:14:22', action: 'AI_LEAD_GEN', desc: 'New hidden link predicted in C-892' },
                { time: '08:45:10', action: 'GRAPH_UPDATE', desc: '4 nodes added by SYSTEM' },
                { time: '07:22:05', action: 'USER_LOGIN', desc: 'Agent Sourabi authenticated' }
              ].map((log, i) => (
                <div key={i} className="flex gap-4 items-start border-b border-[rgba(237,231,220,0.05)] pb-4 last:border-0">
                  <span className="technical-label text-[#6C7378] shrink-0">{log.time}</span>
                  <div className="flex flex-col gap-1">
                    <span className="technical-label text-[#E8913C]">{log.action}</span>
                    <span className="text-sm font-inter font-light text-[#EDE7DC]">{log.desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}

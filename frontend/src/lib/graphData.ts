export const mockGraphElements = [
  // NODES
  { data: { id: 'n1', label: 'Raj Kumar', type: 'PERSON', aliases: 'Raj, R.K.' } },
  { data: { id: 'n2', label: 'Nexus Cartel', type: 'ORGANIZATION', aliases: 'Nexus' } },
  { data: { id: 'n3', label: 'Warehouse 4', type: 'LOCATION', aliases: 'WH-04' } },
  { data: { id: 'n4', label: 'Amit Singh', type: 'PERSON', aliases: 'A.S.' } },
  { data: { id: 'n5', label: '+91-9876543210', type: 'PHONE', aliases: '' } },
  { data: { id: 'n6', label: 'ACCT-9921', type: 'ACCOUNT', aliases: 'Offshore 1' } },
  { data: { id: 'n7', label: 'Midnight Meeting', type: 'EVENT', aliases: 'Event-01' } },
  
  // EDGES
  { data: { source: 'n1', target: 'n2', label: 'MEMBER_OF', type: 'CONFIRMED' } },
  { data: { source: 'n1', target: 'n5', label: 'OWNS', type: 'CONFIRMED' } },
  { data: { source: 'n4', target: 'n5', label: 'CALLED', type: 'CONFIRMED' } },
  { data: { source: 'n2', target: 'n3', label: 'OPERATES_AT', type: 'CONFIRMED' } },
  { data: { source: 'n4', target: 'n6', label: 'TRANSFERRED', type: 'CONFIRMED' } },
  { data: { source: 'n1', target: 'n7', label: 'ATTENDED', type: 'CONFIRMED' } },
  
  // POTENTIAL CONNECTION (AI PREDICTION)
  { data: { id: 'e_hidden', source: 'n1', target: 'n4', label: 'POTENTIAL_ASSOCIATION', type: 'PREDICTED', confidence: 87 } }
];

export const cytoscapeStylesheet = [
  {
    selector: 'node',
    style: {
      'background-color': '#101317',
      'label': 'data(label)',
      'color': '#EDE7DC',
      'font-size': '10px',
      'font-family': 'JetBrains Mono, monospace',
      'text-valign': 'bottom',
      'text-halign': 'center',
      'text-margin-y': 4,
      'border-width': 2,
      'border-color': 'rgba(237,231,220,0.3)'
    }
  },
  {
    selector: 'node[type = "PERSON"]',
    style: { 'border-color': '#E8913C', 'shape': 'ellipse' }
  },
  {
    selector: 'node[type = "ORGANIZATION"]',
    style: { 'border-color': '#2E6B72', 'shape': 'hexagon' }
  },
  {
    selector: 'node[type = "LOCATION"]',
    style: { 'border-color': '#EDE7DC', 'shape': 'rectangle' }
  },
  {
    selector: 'node:selected',
    style: {
      'background-color': '#E8913C',
      'color': '#E8913C',
      'border-width': 4,
      'border-color': '#EDE7DC'
    }
  },
  {
    selector: 'edge',
    style: {
      'width': 2,
      'line-color': 'rgba(237,231,220,0.3)',
      'target-arrow-color': 'rgba(237,231,220,0.3)',
      'target-arrow-shape': 'triangle',
      'curve-style': 'bezier',
      'label': 'data(label)',
      'font-size': '8px',
      'color': '#9EA5A8',
      'text-rotation': 'autorotate',
      'text-margin-y': -10
    }
  },
  {
    selector: 'edge[type = "PREDICTED"]',
    style: {
      'line-color': '#E8913C',
      'target-arrow-color': '#E8913C',
      'line-style': 'dashed',
      'width': 3,
      'color': '#E8913C'
    }
  },
  {
    selector: 'edge:selected',
    style: {
      'line-color': '#EDE7DC',
      'target-arrow-color': '#EDE7DC',
      'color': '#EDE7DC',
      'width': 4
    }
  }
];

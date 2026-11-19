from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
s=(r/'captions.ass').read_text();end=json.loads((r/'edit.json').read_text())['speechDuration']
def ts(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02d}:{n//100%60:02d}.{n%100:02d}'
def event(layer,txt):return f'Dialogue: {layer},0:00:00.00,{ts(end)},Text,,0,0,0,,{txt}\n'
# Opaque card replaces the misspelled text already burned into the original.
s='\n'.join(line for line in s.splitlines() if not line.startswith(('Dialogue: 8,','Dialogue: 9,')))+'\n'
s+=event(8,r'{\an7\pos(130,198)\c&HFCFAF8&\3c&H2A170F&\bord3\shad0\p1}m 22 0 l 798 0 b 812 0 820 8 820 22 l 820 292 b 820 306 812 314 798 314 l 22 314 b 8 314 0 306 0 292 l 0 22 b 0 8 8 0 22 0{\p0}')
s+=event(9,r'{\an5\pos(540,263)\fs65\c&H2A170F&\bord0\shad0}SACOLAS E BOBINAS')
s+=event(9,r'{\an5\pos(540,337)\fs48\c&H2A170F&\bord0\shad0}CARUARU E REGIÃO')
s+=event(8,r'{\an7\pos(310,382)\c&H00B8FF&\bord0\shad0\p1}m 18 0 l 442 0 b 454 0 460 6 460 18 l 460 92 b 460 104 454 110 442 110 l 18 110 b 6 110 0 104 0 92 l 0 18 b 0 6 6 0 18 0{\p0}')
s+=event(9,r'{\an5\pos(540,437)\fs85\c&H2A170F&\bord0\shad0}R$ 16/kg')
(r/'captions.ass').write_text(s)

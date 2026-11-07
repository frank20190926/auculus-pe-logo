from pathlib import Path
import json
P=Path(__file__).parent
# Bespoke high-contrast Roman capitals, drawn in a 70 x 100 em square.
glyph={
'A':'M0 100V98H9L38 0H42L72 98H80V100H48V98H57L48 67H20L11 98H22V100ZM21 63H47L34 20Z',
'U':'M0 0H32V2H23V72C23 90 29 98 43 98C58 98 65 87 65 71V2H54V0H78V2H68V71C68 92 58 102 40 102C19 102 9 92 9 73V2H0Z',
'C':'M70 5V28H68C64 10 55 1 42 1C21 1 18 23 18 50C18 78 22 99 43 99C56 99 66 88 70 71H72V95C64 99 54 102 42 102C15 102 2 80 2 50C2 21 17 -2 43 -2C54 -2 63 1 70 5Z',
'L':'M0 0H34V2H24V98H46C59 98 64 90 69 74H71L68 100H0V98H10V2H0Z',
'S':'M62 4V26H60C56 8 48 1 36 1C23 1 15 9 15 20C15 32 27 38 40 44C57 52 67 59 67 74C67 91 53 102 34 102C23 102 10 99 3 94V70H5C9 90 19 99 34 99C47 99 56 91 56 79C56 67 46 62 31 55C15 48 5 40 5 25C5 9 18 -2 36 -2C46 -2 56 1 62 4Z',
'P':'M0 0H39C64 0 73 11 73 26C73 44 59 53 37 53H24V98H35V100H0V98H10V2H0ZM24 3V50H36C51 50 58 42 58 26C58 10 51 3 37 3Z',
'I':'M0 0H34V2H24V98H34V100H0V98H10V2H0Z',
'T':'M0 0H76L78 25H76C71 7 67 3 55 3H45V98H56V100H20V98H31V3H21C9 3 6 7 2 25H0Z'}
def word(s,y,scale,tracking,color,special=False):
 widths={'I':34,'A':80,'U':78,'C':74,'L':72,'S':68,'P':74,'T':78}
 total=sum(widths[c] for c in s)+tracking*(len(s)-1); x=(800-total*scale)/2
 out=f'<g transform="translate({x} {y}) scale({scale})" fill="{color}" fill-rule="evenodd">'
 pos=0
 for i,c in enumerate(s):
  fill='url(#gold)' if special and i<2 else color
  out+=f'<path transform="translate({pos} 0)" fill="{fill}" d="{glyph[c]}"/>'
  if special and c=='A':out+=f'<path transform="translate({pos} 0)" d="M18 62L53 56L55 62L18 68Z" fill="{bg_current}"/>'
  if special and c=='U' and i==1:out+=f'<path transform="translate({pos} 0)" d="M5 59L28 55V61L5 65Z" fill="{bg_current}"/>'
  pos+=widths[c]+tracking
 return out+'</g>'
def emblem(n,color='url(#gold)'):
 if n==1:return f'<g fill="none" stroke="{color}"><path stroke-width="6" d="M168 55A112 112 0 1 0 168 201"/><path stroke-width="1.5" d="M179 43A128 128 0 1 0 179 213"/></g><path fill="{color}" fill-rule="evenodd" d="M37 228L121 28H132L216 228H188L162 166H66L41 228ZM71 154H157L114 51Z"/><path d="M87 177H180V183H87Z" fill="{color}"/>'
 if n==2:return f'<path d="M128 4L230 53V152Q230 219 128 252Q26 219 26 152V53Z" fill="none" stroke="{color}" stroke-width="3"/><path d="M128 22V233" stroke="{color}" stroke-width="2"/><path fill="{color}" fill-rule="evenodd" d="M58 194V70L128 34L198 70V194ZM78 181L122 65H135L179 181H158L147 149H108L97 181ZM113 135H142L128 94Z"/><path d="M58 202H198" stroke="{color}" stroke-width="2"/>'
 return f'<path fill="{color}" fill-rule="evenodd" d="M22 230L110 25H122L209 230H178L151 164H55L27 230ZM61 150H145L103 49Z"/><path d="M139 42V181Q139 229 190 229Q239 229 239 180V42H233V180Q233 220 200 220Q168 220 168 180V42Z" fill="{color}"/><path d="M46 158L166 140V147L44 165Z" fill="{bg_current}"/>'
grad='<defs><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#F3E3B6"/><stop offset=".48" stop-color="#CFA64B"/><stop offset="1" stop-color="#9A7220"/></linearGradient></defs>'
data=[]
for n in range(1,4):
 variants={}
 for mode in ['dark','light','icon']:
  bg_current='#F8FAFC' if mode=='light' else '#060B16'; ink='#0A1324' if mode=='light' else '#CBD5E1'
  if mode=='icon': vb='0 0 512 512'; content=f'<rect width="512" height="512" fill="{bg_current}"/><g transform="translate(112 112) scale(1.125)">{emblem(n)}</g>'
  else:
   vb='0 0 800 400'; content=f'<rect width="800" height="400" fill="{bg_current}"/>'
   if n<3: content+=f'<g transform="translate(346 40) scale(.42)">{emblem(n)}</g>'
   content+=word('AUCULUS',194 if n<3 else 153,.84,15,ink,n==3)+word('CAPITAL',307 if n<3 else 272,.165,42,ink)
   if n==3:content+='<path d="M365 320H435" stroke="url(#gold)" stroke-width="1"/>'
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Auculus Capital, Marque {n}"><title>Auculus Capital | Marque {n}</title>{grad}{content}</svg>'
  filename=f'auculus-marque-{n}-{mode}.svg'; svg=svg.replace('viewBox="0 0 512 512"','width="512" height="512" viewBox="0 0 512 512"'); (P/'vectors'/filename).write_text(svg);variants[mode]=filename
 data.append(variants)
for mode,filename in [('dark','auculus-primary-dark.svg'),('light','auculus-reversed-light.svg'),('icon','auculus-monogram-icon.svg')]:
 (P/'vectors'/filename).write_text((P/'vectors'/data[0][mode]).read_text())
(P/'vector-manifest.js').write_text('const vectors = '+json.dumps(data)+';')

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
import math, zipfile, subprocess, xml.etree.ElementTree as ET
import fitz
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.pens.basePen import BasePen

NAVY='#060B16'; SILVER='#CBD5E1'; WHITE='#F8FAFC'; GOLD='#CFA64B'; PHI=(1+math.sqrt(5))/2
V=P/'vectors'; E=P/'exports'; V.mkdir(exist_ok=True); E.mkdir(exist_ok=True)
# Hand-drawn Roman capitals. Bracket transitions are cubic, never font references.
glyph['A']='M0 100V98H4C10 98 12 94 15 86L40 0H44L73 88C76 96 77 98 84 98V100H49V98H56C60 98 61 96 59 90L52 68H24L18 88C16 95 18 98 24 98H28V100ZM25 64H51L38 22Z'
glyph['U']='M0 0H36V2H31C26 2 25 5 25 11V70C25 88 31 97 45 97C59 97 67 87 67 70V12C67 5 64 2 58 2H55V0H82V2H79C73 2 71 5 71 12V70C71 92 60 102 42 102C20 102 10 92 10 72V11C10 5 9 2 4 2H0Z'
glyph['L']='M0 0H38V2H32C27 2 26 5 26 11V91C26 96 28 97 33 97H47C61 97 66 89 71 74H74L70 100H0V98H5C10 98 11 95 11 89V11C11 5 10 2 5 2H0Z'
glyph['I']='M0 0H38V2H33C28 2 26 5 26 11V89C26 95 28 98 33 98H38V100H0V98H5C10 98 12 95 12 89V11C12 5 10 2 5 2H0Z'
glyph['P']=glyph['P'].replace('H24V98H35V100H0V98H10V2H0','H24V89C24 95 26 98 31 98H35V100H0V98H4C9 98 10 95 10 89V11C10 5 9 2 4 2H0')
glyph['T']=glyph['T'].replace('H45V98H56V100H20V98H31V3','H45V89C45 95 47 98 52 98H56V100H20V98H24C29 98 31 95 31 89V3')
widths={'A':84,'U':82,'C':74,'L':74,'S':68,'P':74,'I':38,'T':78}
def transform(d, tx=0,ty=0,sx=1,sy=None):
 pen=SVGPathPen(None); parse_path(d,TransformPen(pen,(sx,0,0,sx if sy is None else sy,tx,ty))); return pen.getCommands()
def path(d,fill,**kw): return '<path '+ ' '.join(f'{k.replace("_","-")}="{v}"' for k,v in dict(d=d,fill=fill,fill_rule='evenodd',**kw).items())+'/>'
def circle(x,y,r):
 k=r*.5522847498307936
 return f'M{x+r} {y}C{x+r} {y+k} {x+k} {y+r} {x} {y+r}C{x-k} {y+r} {x-r} {y+k} {x-r} {y}C{x-r} {y-k} {x-k} {y-r} {x} {y-r}C{x+k} {y-r} {x+r} {y-k} {x+r} {y}Z'
def ring(x,y,r,t):return circle(x,y,r)+circle(x,y,r-t)
def word(s,x,y,scale,tracking,ink):
 out=''
 for c in s:
  out+=path(transform(glyph[c],x,y,scale),ink); x+=(widths[c]+tracking)*scale
 return out
# Each mark is built in a 256-unit design square. Empty counters are real holes.
def mark(n,ink='url(#gold)'):
 if n==1:
  return [(ring(128,128,112,3),ink),(ring(139,128,112/PHI,2),ink),(transform(glyph['A'],73,65,1.19),ink),(transform(glyph['C'],117,91,.72),ink)]
 if n==2:
  outer='M128 12L195 40L228 84L228 165L195 209L128 244L61 209L28 165L28 84L61 40Z'
  inner='M128 19L191 46L221 87L221 162L190 204L128 236L66 204L35 162L35 87L65 46Z'
  return [(outer+inner,ink),(transform(glyph['A'],64,68,1.15),ink),(transform(glyph['C'],119,95,.72),ink),('M127 28H130V57H127ZM127 204H130V226H127Z',GOLD)]
 # C embraces the A; a champagne diagonal joins the two without forming AU.
 return [(transform(glyph['C'],76,34,1.8),ink),(transform(glyph['A'],29,34,1.8),ink),('M48 170L202 133L204 141L51 178Z',GOLD)]
grad='<defs><linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0" stop-color="#F3E3B6"/><stop offset=".5" stop-color="#CFA64B"/><stop offset="1" stop-color="#9A7220"/></linearGradient></defs>'
def svg(w,h,body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{grad}{body}</svg>'
def artwork(n=1,mode='dark',transparent=False):
 icon=mode=='icon'; w,h=(512,512) if icon else (1200,600); bg=WHITE if mode=='light' else NAVY; ink=NAVY if mode=='light' else SILVER
 body='' if transparent else path(f'M0 0H{w}V{h}H0Z',bg)
 if icon:
  for d,c in mark(n):body+=path(transform(d,76,76,360/256),c)
 else:
  for d,c in mark(n):body+=path(transform(d,70,174,.98),c)
  body+=word('AUCULUS',386,226,.99,13,ink)+word('CAPITAL',391,359,.245,48,ink)
 return svg(w,h,body)
def micro(n):
 body=path('M0 0H16V16H0Z',NAVY)
 if n==1: d='M13 4C11 1 5 1 2 5C0 9 3 15 8 15C10 15 12 14 13 13L12 11C8 15 3 12 3 8C3 4 9 2 12 6Z'
 elif n==2:d='M8 1L14 4V11L8 15L2 11V4ZM8 3L4 5V10L8 13L12 10V5Z'
 else:d='M14 4C11 0 5 1 3 4C0 8 3 15 8 15C11 15 13 13 14 11L12 10C10 14 5 13 4 9C3 5 8 2 12 6Z'
 body+=path(d,GOLD)+path('M4 12L7.4 4H8.8L12 12H10L9.3 10H6.4L5.7 12ZM7 8.5H8.8L7.9 6Z',SILVER)
 return svg(16,16,body)
def svg_pdf(source):
 return fitz.open('pdf',subprocess.run(['/opt/homebrew/bin/rsvg-convert','--format=pdf'],input=source.encode(),capture_output=True,check=True).stdout)
def raster(source,w,h,dest):
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','--format=png','--width',str(w),'--height',str(h),'--output',str(dest)],input=source.encode(),check=True)
def pdf_page(doc,source):doc.insert_pdf(svg_pdf(source))
class PSPen(BasePen):
 def __init__(self):super().__init__(None);self.a=[]
 def _moveTo(self,p):self.a.append('%g %g moveto'%p)
 def _lineTo(self,p):self.a.append('%g %g lineto'%p)
 def _curveToOne(self,a,b,c):self.a.append('%g %g %g %g %g %g curveto'%(*a,*b,*c))
 def _closePath(self):self.a.append('closepath')
 def _endPath(self):pass
def rgb(c):return tuple(int(c[i:i+2],16)/255 for i in (1,3,5))
def eps(source,dest):
 root=ET.fromstring(source);w,h=int(root.get('width')),int(root.get('height'))
 out=['%!PS-Adobe-3.0 EPSF-3.0',f'%%BoundingBox: 0 0 {w} {h}','%%LanguageLevel: 3','%%EndComments',f'gsave 0 {h} translate 1 -1 scale']
 for el in root.findall('{*}path'):
  pen=PSPen();parse_path(el.get('d'),pen);out+=['gsave','newpath']+pen.a
  color=el.get('fill')
  if color.startswith('url'):
   out+=['eoclip newpath','<< /ShadingType 2 /ColorSpace /DeviceRGB /Coords [0 0 %s %s] /Function << /FunctionType 3 /Domain [0 1] /Functions [<< /FunctionType 2 /Domain [0 1] /C0 [.953 .890 .714] /C1 [.812 .651 .294] /N 1 >> << /FunctionType 2 /Domain [0 1] /C0 [.812 .651 .294] /C1 [.604 .447 .125] /N 1 >>] /Bounds [.5] /Encode [0 1 0 1] >> /Extend [true true] >> shfill'%(w,h)]
  else:out+=['%g %g %g setrgbcolor'%rgb(color),'eofill']
  out+=['grestore']
 out+=['grestore','showpage','%%EOF'];dest.write_text('\n'.join(out))
def guidelines():
 doc=fitz.open()
 def page(title,subtitle):
  p=doc.new_page(width=960,height=640);p.draw_rect(p.rect,color=None,fill=rgb(WHITE));p.insert_text((48,55),'AUCULUS CAPITAL   /   IDENTITY STANDARDS',fontsize=10,color=rgb(GOLD));p.insert_text((48,102),title,fontsize=29,fontname='tiro',color=rgb(NAVY));p.insert_text((48,128),subtitle,fontsize=11,color=rgb(NAVY));p.insert_text((48,610),f'Auculus Capital  |  Design specification  |  {len(doc):02}',fontsize=9,color=rgb(NAVY));return p
 def art(p,src,rect):
  d=svg_pdf(src);p.show_pdf_page(fitz.Rect(rect),d,0)
 for mode,title in [('dark','01  Primary signature'),('light','02  Reversed signature')]:
  p=page(title,'Outlined Roman capitals. Use the complete lockup above 320 px; use the monogram below.');art(p,artwork(1,mode),(48,160,912,580))
 p=page('03  Three architectural marques','I / Oculus Vault     II / Sovereign Seal     III / Bespoke Ligature')
 for n in range(1,4):art(p,artwork(n,'icon'),(48+(n-1)*300,190,312+(n-1)*300,454));p.insert_text((48+(n-1)*300,490),['Oculus Vault','Sovereign Seal','Bespoke Ligature'][n-1],fontsize=16,fontname='tiro')
 p=page('04  Proportion & exclusion zone','phi = 1.618034  |  R = 112  |  r = R / phi = 69.22  |  vault offset = +11 units')
 art(p,artwork(1,'icon'),(70,165,430,525))
 for r in [fitz.Rect(70,165,430,525),fitz.Rect(46,141,454,549)]:p.draw_rect(r,color=rgb(GOLD),width=.7)
 for i,t in enumerate(['1x = cap height of CAPITAL (24.5 design units).','Keep at least 1x clear on all four sides of visible artwork.','Do not stretch, rotate or alter the letter spacing.','Ring ratio is mathematical; letter spacing is optical.','Use the simplified micro mark at 16 px and 32 px.','Use full-detail icon at 64 px and above.']):p.insert_text((490,210+i*44),t,fontsize=11)
 p=page('05  Colour & production','Digital RGB references. Process values are starting approximations; proof with your printer.')
 colors=[(NAVY,'Midnight Obsidian','RGB 6 / 11 / 22  |  CMYK approx. 73 / 50 / 0 / 91'),(SILVER,'Platinum Silver','RGB 203 / 213 / 225  |  CMYK approx. 10 / 5 / 0 / 12'),(WHITE,'Alabaster','RGB 248 / 250 / 252  |  CMYK approx. 2 / 1 / 0 / 1'),(GOLD,'Brushed Champagne Gold','RGB 207 / 166 / 75  |  CMYK approx. 0 / 20 / 64 / 19')]
 for i,(c,n,t) in enumerate(colors):
  y=170+i*80;p.draw_rect(fitz.Rect(48,y,148,y+54),color=rgb(SILVER),fill=rgb(c));p.insert_text((170,y+18),n+'  '+c,fontsize=15);p.insert_text((170,y+42),t,fontsize=11)
 p.insert_text((48,525),'Screen gold: #F3E3B6 > #CFA64B > #9A7220 at 135 degrees (top-left to bottom-right).',fontsize=11)
 p.insert_text((48,550),'Pantone 871 C metallic ink / matched foil: physical proof required; not an RGB equivalence.',fontsize=11)
 p=page('06  Scale & delivery matrix','SVG / EPS Level 3 / vector PDF / transparent and solid PNG. No live fonts in logo artwork.')
 art(p,artwork(1,'dark'),(48,160,912,400));p.insert_text((48,423),'1200 px website header master (shown reduced)  /  minimum lockup width: 320 px',fontsize=11)
 for i,size in enumerate([64,32,16]):
  art(p,artwork(1,'icon') if size==64 else micro(1),(48+i*180,455,48+i*180+size,455+size));p.insert_text((48+i*180,550),f'{size} px / '+('full icon' if size==64 else 'micro'),fontsize=11)
 p.insert_text((610,480),'Do not reproduce fine gold gradients below 64 px.',fontsize=10);p.insert_text((610,505),'EPS uses RGB vector shading; convert with printer ICC.',fontsize=10)
 doc.save(E/'Auculus_Capital_Identity_Guidelines.pdf',deflate=True)
def build():
 data=[]
 for n in range(1,4):
  variants={}
  for mode in ['dark','light','icon']:
   filename=f'auculus-marque-{n}-{mode}.svg';(V/filename).write_text(artwork(n,mode));variants[mode]=filename
  (V/f'auculus-micro-{n}.svg').write_text(micro(n));data.append(variants)
 for mode,name in [('dark','primary-dark'),('light','reversed-light'),('icon','monogram-icon')]: (V/f'auculus-{name}.svg').write_text(artwork(1,mode))
 (P/'vector-manifest.js').write_text('const vectors = '+json.dumps(data)+';\n')
 for mode,name in [('dark','Primary_Dark'),('light','Reversed_Light'),('icon','Square_Icon')]:
  eps(artwork(1,mode),E/f'Auculus_{name}.eps')
  for transparent in [False,True]:raster(artwork(1,mode,transparent),1024 if mode=='icon' else 2400,1024 if mode=='icon' else 1200,E/f'Auculus_{name}_{"Transparent" if transparent else "Solid"}.png')
 guidelines()
 with zipfile.ZipFile(E/'Auculus_Capital_Identity_Master_Pack.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(V.glob('*.svg')):z.write(f,'vectors/'+f.name)
  for f in sorted(E.iterdir()):
   if f.suffix in ['.eps','.pdf','.png']:z.write(f,'exports/'+f.name)
 print('Built 15 SVG masters, 3 EPS, 6 PNG, 6-page vector guide and ZIP.')
if __name__=='__main__':build()

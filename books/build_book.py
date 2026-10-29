import sys,subprocess,glob,os,io,json,struct,hashlib,tempfile
from PIL import Image
pdf,out,width,q=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
d=tempfile.mkdtemp()
subprocess.run(['pdftoppm','-scale-to-x',str(width),'-scale-to-y','-1','-png',pdf,d+'/p'],check=True)
blobs=[];sizes=[]
for f in sorted(glob.glob(d+'/p-*.png')):
    im=Image.open(f).convert('RGB');b=io.BytesIO();im.save(b,'WEBP',quality=q,method=6);blobs.append(b.getvalue());sizes.append(im.size)
off=0;pages=[]
for b,(w,h) in zip(blobs,sizes):
    pages.append([off,len(b),w,h]);off+=len(b)
head=json.dumps({'v':1,'pages':pages},separators=(',',':')).encode()
with open(out,'wb') as o:
    o.write(struct.pack('>I',len(head)));o.write(head)
    for b in blobs:o.write(b)
print(out,len(pages),os.path.getsize(out),hashlib.sha256(open(out,'rb').read()).hexdigest())

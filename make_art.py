from PIL import Image, ImageFilter
import numpy as np, json
SRC="/mnt/user-data/uploads/3x5_jpg.jpeg"
W,CELL=44,0.47
im=Image.open(SRC).convert("RGB").crop((35,50,680,935))
im=im.filter(ImageFilter.UnsharpMask(radius=4,percent=170,threshold=2))
w,h=im.size
a=np.asarray(im).astype(np.int16); r,g,b=a[...,0],a[...,1],a[...,2]
bg=(b>150)&(g>140)&(r<150)&((b-r)>55)
lum=0.299*r+0.587*g+0.114*b
s=lum[~bg]; lo,hi=np.percentile(s,1),np.percentile(s,99)
norm=np.clip((lum-lo)/(hi-lo),0,1); norm[bg]=1.0
H=int(W*(h/w)*CELL)
sm=np.asarray(Image.fromarray((norm*255).astype(np.uint8)).resize((W,H),Image.LANCZOS)).astype(np.float32)/255
bm=np.asarray(Image.fromarray((bg*255).astype(np.uint8)).resize((W,H),Image.LANCZOS)).astype(np.float32)/255
RAMP="@%&#8Wo*=+~:-. "
n=len(RAMP)-1
chars=[];shade=[]
for y in range(H):
    cr=[];sr=[]
    for x in range(W):
        if bm[y,x]>0.5:
            cr.append(" ");sr.append(-1)
        else:
            v=sm[y,x]; cr.append(RAMP[min(int(round(v*n)),n)])
            sr.append(min(int(v*4),3))     # 0=darkest .. 3=lightest
    chars.append("".join(cr).rstrip());shade.append(sr)
while chars and not chars[0].strip(): chars.pop(0);shade.pop(0)
json.dump({"chars":chars,"shade":shade},open("art.json","w"))
print(len(chars),"rows",max(len(c) for c in chars),"cols")
print("\n".join(chars))

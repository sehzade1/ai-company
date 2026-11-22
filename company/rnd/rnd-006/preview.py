import sys
from PIL import Image, ImageDraw
d = sys.argv[1]; names = ['L1','L2','L3','S1']; T = 300
sheet = Image.new('RGB', (T*3, T*len(names)), 'white')
for r, n in enumerate(names):
    o = Image.open(f'{d}/{n}.png').convert('RGB'); o.thumbnail((T, T)); sheet.paste(o, (0, r*T))
    t = Image.open(f'{d}/{n}-t.png').convert('RGBA'); t.thumbnail((T-10, T-10))
    chk = Image.new('RGB', (T, T), (200, 200, 200)); dr = ImageDraw.Draw(chk)
    for y in range(0, T, 20):
        for x in range(0, T, 20):
            if (x//20 + y//20) % 2: dr.rectangle([x, y, x+19, y+19], fill=(255, 0, 255))
    chk.paste(t, ((T-t.width)//2, (T-t.height)//2), t); sheet.paste(chk, (T, r*T))
    dark = Image.new('RGB', (T, T), (25, 25, 35)); dark.paste(t, ((T-t.width)//2, (T-t.height)//2), t); sheet.paste(dark, (2*T, r*T))
sheet.save(f'{d}/preview.jpg', quality=90)

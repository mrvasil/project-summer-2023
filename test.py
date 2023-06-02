import shutil
import os
sp = os.listdir('db_backup/')
sp2 = []
for i in sp:
    sp2.append(int(i[:-3]))

c = sum([len(files) for r, d, files in os.walk("db_backup/")])

shutil.copyfile('data.db', f'db_backup/{c+1+min(sp2)}.db')

if c>=100:
    os.remove('db_backup/'+str(min(sp2))+'.db')
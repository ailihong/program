import os
for root, directories,filenames in os.walk('./test'):
    for filename in filenames:
        print os.path.join(root,filename)

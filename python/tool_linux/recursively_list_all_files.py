import os
for root, filenames in os.walk('./test'):
    for filename in filenames:
        print os.path.join(root,filename)

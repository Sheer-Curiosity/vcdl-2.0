import os

buildFiles = [f for f in os.listdir('./') if os.path.isfile(os.path.join('./', f))]

for file in buildFiles:
    if file.endswith('.spec'):
        os.remove(f"./{file}")
    else:
        continue
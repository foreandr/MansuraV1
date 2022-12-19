# WORKING LAST TIME I CHECKED
#NOT SURE WHAT THE INSTALLES ARE

# Import module
from nudenet import NudeClassifier

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()

# Classify single image
var = (classifier.classify('/root/mansura/#DemoData/brandi love bikini.jpg'))
print(type(var))
#print(var['safe'])
#print(var['unsafe'])

"working output {'/root/mansura/#DemoData/brandi love bikini.jpg': {'safe': 0.0005391701706685126, 'unsafe': 0.9994608759880066}}"
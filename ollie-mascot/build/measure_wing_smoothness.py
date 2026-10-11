import math
import sys
sys.path[:0]=['tools','artwork']
from wing_poses import SOURCE,soften,tuck_feathers,geometry
from build_artwork import vertices

for source in SOURCE:
    points,_=vertices(source['d'])
    current=soften(tuck_feathers(points,.35),19)
    def metric(items):
        turns=[]
        for point in items:
            vals=geometry(point,'L',(186,397),(114,397),.88)
            diff=(vals[4]-vals[2])%(2*math.pi)-math.pi
            turns.append(abs(diff))
        return round(max(turns),3),sum(t>.3 for t in turns)
    print(source['name'],metric(points),metric(current),len(points),len(current))

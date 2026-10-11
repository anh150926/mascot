"""Pose Ollie's wings with a fixed shoulder and a moving prop target.

All posed wings use the original seven feather contours with flat fills and
uniform rotation/scale. Both carrying and gestures are baked into the local .riv.
"""
from math import atan2, cos, sin, hypot, pi, acos
from build_artwork import PARTS, SCALE, vertices

# The supplied left and right wing samples are the front master's seven
# feathers. Reuse their exact contours for carrying poses. Flat fills remove
# the glossy spots while preserving the pointed lower feather silhouette.
HOLD_SOURCE = [
    {**shape, 'weight': shape['weight']*SCALE, 'gradient': None, 'master': True}
    for shape in next(part for part in PARTS if part['name']=='LeftWing')['shapes']
]
SOURCE = HOLD_SOURCE


def source_vertices(source):
    points, closed = vertices(source['d'])
    divisor=1 if source.get('master') else SCALE
    return [[tuple(v / divisor for v in p) for p in point] for point in points], closed


def mix(a, b, t):
    return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)


def rounded_bridge(incoming, outgoing):
    """Join two trimmed arcs with matching tangents at both ends."""
    start=incoming[3];end=outgoing[0]
    dx,dy=start[0]-incoming[2][0],start[1]-incoming[2][1]
    ex,ey=outgoing[1][0]-end[0],outgoing[1][1]-end[1]
    length=hypot(end[0]-start[0],end[1]-start[1])*.42
    before=max(hypot(dx,dy),.00001);after=max(hypot(ex,ey),.00001)
    return (start,(start[0]+dx/before*length,start[1]+dy/before*length),
            (end[0]-ex/after*length,end[1]-ey/after*length),end)


def split_cubic(segment, t):
    """De Casteljau split keeps the two surviving feather arcs unchanged."""
    p0,c1,c2,p3=segment
    a,b,c=mix(p0,c1,t),mix(c1,c2,t),mix(c2,p3,t)
    d,e=mix(a,b,t),mix(b,c,t)
    f=mix(d,e,t)
    return (p0,a,d,f),(f,e,c,p3)


def subcurve(segment, start, end):
    if start:
        _,segment=split_cubic(segment,start)
    if end<1:
        segment,_=split_cubic(segment,(end-start)/(1-start))
    return segment


def soften(points, radius=14):
    """Round feather tips and notches in posed wings, leaving the master intact.

    At a sharp joint, trim the two neighbouring Bézier arcs and join them with
    a short quadratic arc through the old tip. Smooth joints are untouched.
    """
    count=len(points)
    corners=[]
    for i,(xy,inc,out) in enumerate(points):
        before=points[i-1][0];after=points[(i+1)%count][0]
        incoming=(xy[0]-inc[0],xy[1]-inc[1])
        outgoing=(out[0]-xy[0],out[1]-xy[1])
        if hypot(*incoming)<.001:incoming=(xy[0]-before[0],xy[1]-before[1])
        if hypot(*outgoing)<.001:outgoing=(after[0]-xy[0],after[1]-xy[1])
        divisor=hypot(*incoming)*hypot(*outgoing)
        angle=acos(max(-1,min(1,(incoming[0]*outgoing[0]+incoming[1]*outgoing[1])/divisor))) if divisor else 0
        if angle>.72:
            corners.append((min(.36,radius/max(hypot(xy[0]-before[0],xy[1]-before[1]),1)),
                            min(.36,radius/max(hypot(after[0]-xy[0],after[1]-xy[1]),1))))
        else:corners.append((0,0))
    edges=[]
    for i in range(count):
        j=(i+1)%count
        segment=(points[i][0],points[i][2],points[j][1],points[j][0])
        edges.append(subcurve(segment,corners[i][1],1-corners[j][0]))
    segments=[]
    for i,edge in enumerate(edges):
        segments.append(edge)
        j=(i+1)%count
        if corners[j][0]:
            segments.append(rounded_bridge(edge,edges[j]))
    return [(segment[0],segments[i-1][2],segment[1]) for i,segment in enumerate(segments)]


def tuck_feathers(points, amount):
    """Fold the long feather ends behind a held prop without moving the shoulder."""
    def tuck(p):
        x,y=p;distance=max(y-398,0)
        return x,y-amount*distance*distance/(distance+25)
    return [tuple(tuck(p) for p in point) for point in points]


def warp(point, side, tip, bend, width=.88):
    """Bend the master centreline; retain its feather spacing and proportions."""
    x, y = point
    t = (y - 318) / 138
    across = (x - (162 - 32*t)) * width
    root = (166, 325) if side == 'L' else (334, 325)
    dx = 2*((1-t)*(bend[0]-root[0]) + t*(tip[0]-bend[0]))
    dy = 2*((1-t)*(bend[1]-root[1]) + t*(tip[1]-bend[1]))
    length = max(hypot(dx,dy),1)
    sign = 1 if side == 'L' else -1
    return ((1-t)**2*root[0] + 2*t*(1-t)*bend[0] + t*t*tip[0] + sign*across*dy/length,
            (1-t)**2*root[1] + 2*t*(1-t)*bend[1] + t*t*tip[1] - sign*across*dx/length)


def hug_warp(point, side, tip, bend, width=1):
    x,y=point
    if side=='R':x=500-x
    root=(155,322) if side=='L' else (345,322)
    anchor=(164,421) if side=='L' else (336,421)
    ax,ay=anchor[0]-root[0],anchor[1]-root[1]
    tx,ty=tip[0]-root[0],tip[1]-root[1]
    angle=atan2(ty,tx)-atan2(ay,ax)
    scale=hypot(tx,ty)/hypot(ax,ay)
    scale=max(.72,min(.84,scale))
    dx,dy=x-root[0],y-root[1]
    return (root[0]+scale*(dx*cos(angle)-dy*sin(angle)),
            root[1]+scale*(dx*sin(angle)+dy*cos(angle)))


def geometry(points, side, tip, bend, width, style='gesture'):
    transform=hug_warp if style=='hug' else warp
    xy, inc, out = [transform(p,side,tip,bend,width) for p in points]
    ix,iy=inc[0]-xy[0],inc[1]-xy[1]
    ox,oy=out[0]-xy[0],out[1]-xy[1]
    before,after=hypot(ix,iy),hypot(ox,oy)
    if style=='hug':
        return (xy[0],xy[1],atan2(iy,ix),before,atan2(oy,ox),after)
    if before>.00001 and after>.00001:
        # A nonlinear wing bend can break tangency even when the source path is
        # smooth. Align both controls again in the posed artboard coordinates.
        tx,ty=-ix/before+ox/after,-iy/before+oy/after
        if hypot(tx,ty)>.00001:
            tangent=atan2(ty,tx)
            return (xy[0],xy[1],tangent+pi,before,tangent,after)
    return (xy[0],xy[1],atan2(iy,ix),before,atan2(oy,ox),after)


def evaluate(animation, node, prop, frame, default):
    obj=animation.find(f"KeyedObject[@objectId='{node.get('id')}']")
    track=obj.find(f"KeyedProperty[@propertyKey='{prop}']") if obj is not None else None
    if track is None:return default
    points=[(float(k.get('frame')),float(k.get('value'))) for k in track]
    for (a,va),(b,vb) in zip(points,points[1:]):
        if a<=frame<=b:
            progress=(frame-a)/(b-a)
            # Invert the shared cubic-bezier(.42,0,.58,1) time curve.
            lo,hi=0.,1.
            for _ in range(24):
                u=(lo+hi)/2
                tx=3*(1-u)**2*u*.42+3*(1-u)*u*u*.58+u**3
                if tx<progress:lo=u
                else:hi=u
            u=(lo+hi)/2
            return va+(vb-va)*(3*(1-u)*u*u+u**3)
    return points[0][1] if frame<points[0][0] else points[-1][1]


class WingPoses:
    def __init__(self, api, foreground):
        self.api,self.foreground,self.wings=api,foreground,[]

    def add(self, name, side, tip, bend, follow=None, width=.88, motion=None, cadence=None, rounding=14, tuck=0, style='hug'):
        a=self.api
        node=a.N(self.foreground,name)
        pose=dict(name=name,side=side,tip=tip,bend=bend,follow=follow,width=width,
                  motion=motion,cadence=cadence,rounding=rounding,tuck=tuck,style=style,vertices=[],gradients=[],node=node)
        self.wings.append(pose)
        target=self.target(pose)
        transform=hug_warp if style=='hug' else warp
        for source in HOLD_SOURCE if style=='hug' else SOURCE:
            s=a.shape(node,source['name'])
            points,closed=source_vertices(source)
            if tuck:points=tuck_feathers(points,tuck)
            # The master has deliberate sharp feather tips; leave them intact.
            p=a.E(s,'PointsPath',isClosed=str(closed).lower())
            for point in points:
                values=geometry(point,side,target,bend,width,style)
                v=a.E(p,'CubicDetachedVertex',**dict(zip(('x','y','inRotation','inDistance','outRotation','outDistance'),values)))
                pose['vertices'].append((v,point))
            if source.get('gradient'):
                c1,c2,x1,y1,x2,y2=source['gradient']
                start=(x1,y1);end=(x2,y2)
                p1=transform(start,side,target,bend,width);p2=transform(end,side,target,bend,width)
                grad=a.E(a.E(s,'Fill'),'LinearGradient',startX=p1[0],startY=p1[1],endX=p2[0],endY=p2[1])
                a.E(grad,'GradientStop',position=0,colorValue='FF'+c1)
                a.E(grad,'GradientStop',position=1,colorValue='FF'+c2)
                pose['gradients'].append((grad,start,end))
                a.paint(s,None,'FF'+source['stroke'] if source['stroke'] else None,source['weight'])
            else:
                a.paint(s,'FF'+source['fill'],'FF'+source['stroke'] if source['stroke'] else None,source['weight'])
        return pose

    def hold(self, prop, offset=67, y=5):
        for side,sign in [('L',-1),('R',1)]:
            self.add('HoldingWing'+side,side,(sign*(offset-67),y+24),
                     (250+sign*121,385),follow=prop,style='hug')

    def target(self, pose, animation=None, frame=0):
        x,y=pose['tip'];follow=pose['follow']
        if follow is not None:
            def value(prop,attr,default=0):
                base=float(follow.get(attr,default))
                return evaluate(animation,follow,prop,frame,base) if animation is not None else base
            angle=value(15,'rotation');x,y=x*cos(angle)-y*sin(angle),x*sin(angle)+y*cos(angle)
            x+=value(13,'x');y+=value(14,'y')
        if animation is not None and pose['motion']:
            dx,dy=pose['motion'](frame,int(animation.get('duration')))
            x+=dx;y+=dy
        return x,y

    def animate(self, animation):
        a=self.api;duration=int(animation.get('duration'))
        for pose in self.wings:
            frames={0,duration//2,duration}
            if pose['follow'] is not None:
                obj=animation.find(f"KeyedObject[@objectId='{pose['follow'].get('id')}']")
                if obj is not None:
                    frames.update(int(k.get('frame')) for p in obj for k in p if k.tag=='KeyFrameDouble')
            if pose['cadence']:
                frames.update(range(0,duration+1,pose['cadence']))
            frames=sorted(frames)
            targets={t:self.target(pose,animation,t) for t in frames}
            for vertex,source in pose['vertices']:
                values=[geometry(source,pose['side'],targets[t],pose['bend'],pose['width'],pose['style']) for t in frames]
                # Unwrap bezier handle angles so interpolation never spins a feather.
                for column in (2,4):
                    for i in range(1,len(values)):
                        row=list(values[i]);previous=values[i-1][column]
                        row[column]=previous+(row[column]-previous+pi)%(2*pi)-pi
                        values[i]=tuple(row)
                for column,prop in enumerate((24,25,84,85,86,87)):
                    if max(v[column] for v in values)-min(v[column] for v in values)<.00001:continue
                    a.keys(animation,vertex,prop,[(t,round(values[i][column],6)) for i,t in enumerate(frames)])
            for grad,start,end in pose['gradients']:
                transform=hug_warp if pose['style']=='hug' else warp
                values=[(*transform(start,pose['side'],targets[t],pose['bend'],pose['width']),
                         *transform(end,pose['side'],targets[t],pose['bend'],pose['width'])) for t in frames]
                for column,prop in enumerate((42,33,34,35)):
                    a.keys(animation,grad,prop,[(t,round(values[i][column],6)) for i,t in enumerate(frames)])

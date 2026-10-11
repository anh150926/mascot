"""Pose seven soft, layered wing feathers along a shoulder-to-feather curve.

The root stays on the body. Only the distal end follows a prop or a gesture.
This is a baked vector deformation, so the exported .riv needs no host code.
"""
from math import atan2, cos, sin, hypot, pi, acos
from build_artwork import SCALE, vertices

# These are artboard (500px) paths. The neutral front master is deliberately
# untouched: only expression wings receive this rounder, more flowing anatomy.
# Each contour closes with cubic arcs, including the tips of the dark feathers.
SOURCE = [
    dict(name='SoftWingOutline', d='M 163 323 C 187 317 202 342 207 367 C 215 399 202 426 183 441 C 165 458 145 465 132 451 C 114 459 100 448 101 434 C 86 437 77 423 83 406 C 91 370 119 338 149 324 C 154 321 159 321 163 323 Z', fill='075338', stroke='06442B', weight=4.2),
    dict(name='LongLowerFeather', d='M 171 384 C 196 398 193 424 175 440 C 161 453 143 462 139 454 C 136 446 148 428 157 410 C 164 397 168 389 171 384 Z', fill='085638', stroke=None, weight=0),
    dict(name='MiddleLowerFeather', d='M 151 383 C 174 395 180 418 167 433 C 154 446 137 454 126 450 C 116 447 124 436 135 420 C 143 405 146 392 151 383 Z', fill='064F34', stroke='06442B', weight=2.7),
    dict(name='LongSideFeather', d='M 135 369 C 153 380 161 403 149 421 C 136 438 113 452 103 442 C 96 435 110 420 120 402 C 129 386 133 377 135 369 Z', fill='69AF47', stroke=None, weight=0),
    dict(name='FoldedUpperWing', d='M 156 322 C 183 317 199 340 202 365 C 205 392 193 418 175 427 C 157 437 146 431 142 417 C 125 431 106 433 94 420 C 83 405 97 375 111 353 C 124 334 143 324 156 322 Z', fill='287D43', stroke='06442B', weight=4, gradient=('4A9C47','196C3E',168,330,124,428)),
    dict(name='LongLimeCovert', d='M 189 366 C 194 384 187 402 172 409 C 163 413 161 405 166 394 C 172 382 181 375 189 366 Z', fill='A4D156', stroke=None, weight=0),
    dict(name='UpperLeafCovert', d='M 145 350 C 148 361 142 377 132 388 C 123 398 112 400 109 392 C 115 371 127 357 145 350 Z', fill='A9D75F', stroke=None, weight=0, gradient=('B1DB65','8EC94D',136,353,117,395)),
]

# A held object needs a different silhouette from a pointing gesture. The
# shoulder fans outward, while long rounded feathers sweep in front of and
# beneath the object. Base coordinates fit the 169px envelope at (250, 373).
HOLD_SOURCE = [
    dict(name='HugOutline', d='M 162 324 C 134 316 110 342 101 375 C 90 410 99 438 118 448 C 135 457 151 455 155 444 C 174 456 187 448 181 437 C 200 448 213 439 208 424 C 211 413 201 400 184 391 C 178 363 177 336 162 324 Z', fill='075338', stroke='06442B', weight=4.2),
    dict(name='HugLowerFeather', d='M 107 393 C 101 424 116 450 145 459 C 164 467 181 455 168 444 C 141 429 117 406 107 393 Z', fill='085638', stroke=None, weight=0),
    dict(name='HugMiddleFeather', d='M 116 388 C 119 422 142 446 181 452 C 201 456 211 447 198 434 C 177 411 145 392 116 388 Z', fill='064F34', stroke='06442B', weight=2.2),
    dict(name='HugInnerFeather', d='M 127 379 C 135 411 166 434 207 439 C 224 441 225 431 210 418 C 188 398 156 385 127 379 Z', fill='287D43', stroke='06442B', weight=2.2),
    dict(name='HugMainWing', d='M 159 325 C 132 325 113 349 107 377 C 103 397 109 411 122 416 C 131 420 137 413 139 405 C 149 419 160 425 170 421 C 178 417 173 409 166 400 C 181 411 195 416 201 408 C 205 400 187 388 178 375 C 174 344 172 329 159 325 Z', fill='287D43', stroke='06442B', weight=4, gradient=('4A9C47','196C3E',138,338,172,438)),
    dict(name='HugLimeScallops', d='M 110 394 C 108 411 114 425 123 430 C 129 433 133 426 132 419 C 139 430 147 433 152 426 C 155 421 151 413 146 406 C 131 393 117 388 110 394 Z', fill='A4D156', stroke=None, weight=0),
    dict(name='HugUpperCovert', d='M 145 348 C 131 350 120 363 117 380 C 115 390 118 398 123 400 C 128 400 130 392 132 386 C 137 393 141 394 145 387 C 151 374 150 359 145 348 Z', fill='A9D75F', stroke=None, weight=0, gradient=('B1DB65','8EC94D',137,352,125,397)),
]


def source_vertices(source):
    points, closed = vertices(source['d'])
    return [[tuple(v / SCALE for v in p) for p in point] for point in points], closed


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
    base=(208,410) if side=='L' else (292,410)
    shoulder=(162,324) if side=='L' else (338,324)
    # The broad outside arc is the feature that makes this read as a wing
    # rather than a narrow sleeve beside the envelope.
    if side=='L' and x<shoulder[0]:x=shoulder[0]+(x-shoulder[0])*1.42
    if side=='R' and x>shoulder[0]:x=shoulder[0]+(x-shoulder[0])*1.42
    reach=max(0,min(1,(y-shoulder[1])/88))
    reach=reach*reach*(3-2*reach)
    # Root is sewn into the body; the distal feather fan follows the prop.
    dx,dy=tip[0]-base[0],tip[1]-base[1]
    return x+dx*reach,y+dy*reach


def geometry(points, side, tip, bend, width, style='gesture'):
    transform=hug_warp if style=='hug' else warp
    xy, inc, out = [transform(p,side,tip,bend,width) for p in points]
    ix,iy=inc[0]-xy[0],inc[1]-xy[1]
    ox,oy=out[0]-xy[0],out[1]-xy[1]
    before,after=hypot(ix,iy),hypot(ox,oy)
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

    def add(self, name, side, tip, bend, follow=None, width=.88, motion=None, cadence=None, rounding=14, tuck=0, style='gesture'):
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
            if style=='hug' and closed:points=soften(points,8)
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
            self.add('HoldingWing'+side,side,(sign*(offset-39),y+33),
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

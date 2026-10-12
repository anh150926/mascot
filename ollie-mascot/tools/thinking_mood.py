"""The eighth everyday mood: a quiet, seamless pondering loop.

This is deliberately separate from the sticker-inspired `idea` scene. It uses
the same front rig and seven-feather wing geometry, without a solved-idea prop.
"""
from __future__ import annotations

from math import cos, pi

import expression_library as scene
from build_data import read
from expression_library import E, N, ellipse, keys, fixed, animate_scene
from wing_poses import WingPoses


DURATION = 180  # 3 seconds at 60 fps


def add_thinking_mood(artboard):
    character = artboard.find("Node[@id='0:10']")
    face = next(node for node in character.iter('Node') if node.get('id') == '0:15')
    props = next(slot for slot in character.iter('Solo') if slot.get('name') == 'SceneProps')
    face_slot = next(slot for slot in face.iter('Solo') if slot.get('name') == 'SceneFace')
    backdrop = next(slot for slot in character.iter('Solo') if slot.get('name') == 'SceneBackdrop')

    wing_group = N(props, 'ThinkingPose')
    wings = WingPoses(scene, wing_group)
    wings.add('ChinWing', 'L', (226, 301), (195, 326), width=.80, full_size=True,
              motion=lambda frame, length: (0, -4 * (1-cos(2*pi*frame/length))/2))

    marks = N(face_slot, 'ThinkingMarks')
    # Three graduated bubbles connect Ollie's head to the thought cloud,
    # replacing the old three free-floating dots with a classic thought-bubble
    # visual. Each bubble is slightly larger than the one below it.
    bubbles = [ellipse(marks, f'LinkBubble{i}', x, y, w, h,
                       'DDAEDDB5', 'BB72AA66', 1.5)
               for i, (x, y, w, h) in enumerate((
                   (403, 175, 9, 9),
                   (415, 148, 14, 13),
                   (430, 122, 19, 17)), 1)]

    # The thought cloud is built from four overlapping ellipse puffs so it
    # renders as soft, rounded vector art without needing an SVG path parser.
    cloud_group = N(marks, 'ThoughtCloud', x=468, y=68)
    for puff_name, px, py, pw, ph in [
        ('Puff1', -30,  5, 42, 34),
        ('Puff2',  -5, -8, 48, 38),
        ('Puff3',  25,  3, 40, 32),
        ('Puff4',   0,  8, 56, 28),
    ]:
        ellipse(cloud_group, puff_name, px, py, pw, ph,
                'DDECF7E8', 'BB72AA66', 1.8)

    # Five dots inside the cloud, evenly spaced on the horizontal centre line.
    cloud_dots = [ellipse(cloud_group, f'CloudDot{i}', x, 0, 6, 6,
                          'FF72AA66', None)
                  for i, x in enumerate((-24, -12, 0, 12, 24), 1)]

    animation = E(artboard, 'LinearAnimation', name='mood_thinking',
                  duration=DURATION, fps=60, loopValue='loop')
    animate_scene(animation, {'key': 'thinking', 'frames': DURATION}, {'wings': wings})
    fixed(animation, '0:17', 296, '0:9100', True)
    fixed(animation, '0:18', 296, '0:44', True)
    fixed(animation, '0:19', 296, '0:51', True)
    # A pause to consider, a slight upward glance and head tilt, then the
    # exact starting pose again. All tracks share frame 0/180 for a clean loop.
    keys(animation, '0:11', 15, [(0, -.035), (44, -.09), (94, -.11),
                                  (136, -.065), (DURATION, -.035)])
    keys(animation, '0:16', 17, [(0, 1), (126, 1), (132, .18),
                                  (138, 1), (DURATION, 1)])
    # Connecting bubbles fade in one after another, bottom to top.
    for i, bub in enumerate(bubbles):
        offset = i * 14
        keys(animation, bub, 18, [(0, 0), (15 + offset, 0),
                                  (35 + offset, .75), (120 + offset, .75),
                                  (145 + offset, 0), (DURATION, 0)])

    # The cloud group fades in after the last bubble and gently breathes.
    keys(animation, cloud_group, 18, [(0, 0), (30, 0), (55, .85),
                                       (130, .85), (155, 0), (DURATION, 0)])
    keys(animation, cloud_group, 16, [(0, .95), (DURATION // 2, 1.05),
                                       (DURATION, .95)])
    keys(animation, cloud_group, 17, [(0, .95), (DURATION // 2, 1.05),
                                       (DURATION, .95)])

    # Five interior dots appear left-to-right with staggered timing.
    for i, dot in enumerate(cloud_dots):
        offset = i * 8
        keys(animation, dot, 18, [(0, .12), (40 + offset, .12),
                                  (58 + offset, .85), (105 + offset, .85),
                                  (130 + offset, .12), (DURATION, .12)])
    fixed(animation, props, 296, wing_group.get('id'), True)
    fixed(animation, face_slot, 296, marks.get('id'), True)
    fixed(animation, backdrop, 296, backdrop.get('activeComponentId'), True)

    layer = artboard.find("StateMachine/StateMachineLayer[@name='Mood']")
    state = E(layer, 'AnimationState', animationId=animation.get('id'), x=600, y=200)
    transition = E(layer.find('AnyState'), 'StateTransition',
                   stateToId=state.get('id'), duration=220)
    condition = E(transition, 'TransitionViewModelCondition', opValue='equal')
    comparator = E(condition, 'TransitionPropertyViewModelComparator')
    binding = E(comparator, 'BindablePropertyEnum')
    E(binding, 'DataBindContext', sourcePathIds='0:610-0:611', propertyKey=637)
    mood_id = next(value['id'] for value in read('data/model.json')['enums'][0]['values']
                   if value['key'] == 'thinking')
    E(condition, 'TransitionValueEnumComparator', value=mood_id)

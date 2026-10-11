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
    wings.add('ChinWing', 'L', (226, 301), (195, 326), width=.80,
              motion=lambda frame, length: (0, -4 * (1-cos(2*pi*frame/length))/2))

    marks = N(face_slot, 'ThinkingMarks')
    # These small dots read as thought in the compact UI, without the question
    # mark of `confused` or the bulb that appears after an `idea` is found.
    dots = [ellipse(marks, f'ThoughtDot{i}', x, y, size, size,
                    'FF72AA66', None)
            for i, (x, y, size) in enumerate(((420, 165, 8), (438, 145, 11),
                                               (454, 124, 14)), 1)]

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
    for i, dot in enumerate(dots):
        offset = i * 12
        keys(animation, dot, 18, [(0, .12), (28+offset, .12),
                                  (53+offset, .8), (112+offset, .8),
                                  (145+offset, .12), (DURATION, .12)])
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

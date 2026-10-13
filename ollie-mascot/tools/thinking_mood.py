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
    face = next(node for node in character.iter("Node") if node.get("id") == "0:15")
    props = next(slot for slot in character.iter("Solo") if slot.get("name") == "SceneProps")
    face_slot = next(slot for slot in face.iter("Solo") if slot.get("name") == "SceneFace")
    backdrop = next(slot for slot in character.iter("Solo") if slot.get("name") == "SceneBackdrop")

    wing_group = N(props, "ThinkingPose")
    wings = WingPoses(scene, wing_group)
    wings.add(
        "ChinWing",
        "L",
        (226, 301),
        (195, 326),
        width=0.80,
        full_size=True,
        motion=lambda frame, length: (0, -4 * (1 - cos(2 * pi * frame / length)) / 2),
    )

    marks = N(face_slot, "ThinkingMarks")
    # Opaque artwork stays clean in both the transparent Rive artboard and
    # the browser fallback exported from CLI screenshots.
    bubbles = [
        ellipse(marks, f"LinkBubble{i}", x, y, w, h, "FFE8F5E8", "FF72AA66", 1.5)
        for i, (x, y, w, h) in enumerate(
            ((403, 175, 9, 9), (415, 148, 14, 13), (430, 122, 19, 17)), 1
        )
    ]

    # One closed contour avoids the dark overlaps produced by translucent
    # puffs when the CLI screenshot is converted into a fallback PNG.
    cloud_group = N(marks, "ThoughtCloud", x=448, y=75)
    scene._api.bezier(
        cloud_group,
        "CloudContour",
        "M -43 20 C -58 18 -64 2 -52 -11 "
        "C -57 -29 -38 -43 -22 -36 "
        "C -12 -53 17 -52 29 -36 "
        "C 47 -38 60 -22 52 -6 "
        "C 62 10 52 27 37 25 "
        "C 24 39 0 39 -13 29 "
        "C -26 35 -40 30 -43 20 Z",
        "FFE8F5E8",
        "FF72AA66",
        2.2,
    )

    # Five dots inside the cloud, evenly spaced on the horizontal centre line.
    cloud_dots = [
        ellipse(cloud_group, f"CloudDot{i}", x, 0, 6, 6, "FF72AA66", None)
        for i, x in enumerate((-24, -12, 0, 12, 24), 1)
    ]

    animation = E(
        artboard,
        "LinearAnimation",
        name="mood_thinking",
        duration=DURATION,
        fps=60,
        loopValue="loop",
    )
    animate_scene(animation, {"key": "thinking", "frames": DURATION}, {"wings": wings})
    fixed(animation, "0:17", 296, "0:9100", True)
    fixed(animation, "0:18", 296, "0:44", True)
    fixed(animation, "0:19", 296, "0:51", True)
    # A pause to consider, a slight upward glance and head tilt, then the
    # exact starting pose again. All tracks share frame 0/180 for a clean loop.
    keys(
        animation,
        "0:11",
        15,
        [(0, -0.035), (44, -0.09), (94, -0.11), (136, -0.065), (DURATION, -0.035)],
    )
    keys(animation, "0:16", 17, [(0, 1), (126, 1), (132, 0.18), (138, 1), (DURATION, 1)])
    # Connecting bubbles grow one after another, bottom to top.
    for i, bub in enumerate(bubbles):
        offset = i * 14
        for axis in (16, 17):
            keys(
                animation,
                bub,
                axis,
                [
                    (0, 0.001),
                    (15 + offset, 0.001),
                    (35 + offset, 1),
                    (120 + offset, 1),
                    (145 + offset, 0.001),
                    (DURATION, 0.001),
                ],
            )

    # The cloud follows the bubbles, then breathes gently at full size.
    for axis in (16, 17):
        keys(
            animation,
            cloud_group,
            axis,
            [
                (0, 0.001),
                (30, 0.001),
                (55, 1),
                (DURATION // 2, 1.05),
                (130, 1),
                (155, 0.001),
                (DURATION, 0.001),
            ],
        )

    # Five interior dots appear left-to-right with staggered timing.
    for i, dot in enumerate(cloud_dots):
        offset = i * 8
        for axis in (16, 17):
            keys(
                animation,
                dot,
                axis,
                [
                    (0, 0.001),
                    (40 + offset, 0.001),
                    (58 + offset, 1),
                    (105 + offset, 1),
                    (130 + offset, 0.001),
                    (DURATION, 0.001),
                ],
            )
    fixed(animation, props, 296, wing_group.get("id"), True)
    fixed(animation, face_slot, 296, marks.get("id"), True)
    fixed(animation, backdrop, 296, backdrop.get("activeComponentId"), True)

    layer = artboard.find("StateMachine/StateMachineLayer[@name='Mood']")
    state = E(layer, "AnimationState", animationId=animation.get("id"), x=600, y=200)
    transition = E(
        layer.find("AnyState"), "StateTransition", stateToId=state.get("id"), duration=220
    )
    condition = E(transition, "TransitionViewModelCondition", opValue="equal")
    comparator = E(condition, "TransitionPropertyViewModelComparator")
    binding = E(comparator, "BindablePropertyEnum")
    E(binding, "DataBindContext", sourcePathIds="0:610-0:611", propertyKey=637)
    mood_id = next(
        value["id"]
        for value in read("data/model.json")["enums"][0]["values"]
        if value["key"] == "thinking"
    )
    E(condition, "TransitionValueEnumComparator", value=mood_id)

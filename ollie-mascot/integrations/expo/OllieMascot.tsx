import React, { memo, useEffect, useRef, useState } from "react";
import {
  Image,
  StyleSheet,
  View,
  type StyleProp,
  type ViewStyle,
} from "react-native";
import {
  Fit,
  RiveView,
  useRive,
  useRiveBoolean,
  useRiveEnum,
  useRiveFile,
  useRiveTrigger,
  useViewModelInstance,
} from "@rive-app/react-native";

import { OLLIE_RIVE, type OllieMood } from "./OllieContract";

// Metro needs a literal require() so the .riv is included in release builds.
const riveAsset = require("./assets/ollie.riv");
const fallbackAsset = require("./assets/neutral.png");

export interface OllieMascotProps {
  mood?: OllieMood;
  asleep?: boolean;
  /** Increment to play one wave. The initial value does not trigger a wave. */
  waveToken?: number;
  /** Pause the native animation when the containing screen is not visible. */
  active?: boolean;
  /** Default is 200 logical pixels. */
  size?: number;
  /** Default is 30 FPS to limit work while Ollie is visible. */
  frameRate?: number;
  style?: StyleProp<ViewStyle>;
  onAsleepChange?: (asleep: boolean) => void;
  onError?: (message: string) => void;
}

export const OllieMascot = memo(function OllieMascot({
  mood = "neutral",
  asleep = false,
  waveToken = 0,
  active = true,
  size = 200,
  frameRate = 30,
  style,
  onAsleepChange,
  onError,
}: OllieMascotProps) {
  const { riveFile, error: fileError } = useRiveFile(riveAsset);
  const { instance, error: instanceError } = useViewModelInstance(riveFile, {
    async: true,
    viewModelName: OLLIE_RIVE.viewModel,
    instanceName: OLLIE_RIVE.instance,
  });
  const { riveViewRef, setHybridRef } = useRive();
  const {
    value: currentMood,
    setValue: setMood,
    error: moodError,
  } = useRiveEnum(OLLIE_RIVE.properties.mood, instance);
  const {
    value: currentAsleep,
    setValue: setAsleep,
    error: asleepError,
  } = useRiveBoolean(OLLIE_RIVE.properties.asleep, instance);
  const { trigger: triggerWave, error: waveError } = useRiveTrigger(
    OLLIE_RIVE.properties.wave,
    instance,
  );
  const [viewError, setViewError] = useState<string | null>(null);

  const appliedMood = useRef<{ instance: unknown; value: OllieMood } | null>(
    null,
  );
  const appliedAsleep = useRef<{ instance: unknown; value: boolean } | null>(
    null,
  );
  const previousAsleep = useRef<boolean | undefined>(undefined);
  const previousWaveToken = useRef(waveToken);

  useEffect(() => {
    if (!instance || moodError) return;
    if (
      appliedMood.current?.instance === instance &&
      appliedMood.current.value === mood
    )
      return;
    appliedMood.current = { instance, value: mood };
    if (currentMood !== mood) setMood(mood);
    if (active) riveViewRef?.playIfNeeded();
  }, [active, currentMood, instance, mood, moodError, riveViewRef, setMood]);

  useEffect(() => {
    if (!instance || asleepError) return;
    if (
      appliedAsleep.current?.instance === instance &&
      appliedAsleep.current.value === asleep
    )
      return;
    appliedAsleep.current = { instance, value: asleep };
    if (currentAsleep !== asleep) setAsleep(asleep);
    if (active) riveViewRef?.playIfNeeded();
  }, [
    active,
    asleep,
    asleepError,
    currentAsleep,
    instance,
    riveViewRef,
    setAsleep,
  ]);

  useEffect(() => {
    if (currentAsleep === undefined) return;
    if (
      previousAsleep.current !== undefined &&
      previousAsleep.current !== currentAsleep
    ) {
      onAsleepChange?.(currentAsleep);
    }
    previousAsleep.current = currentAsleep;
  }, [currentAsleep, onAsleepChange]);

  useEffect(() => {
    if (!instance || waveToken === previousWaveToken.current) return;
    previousWaveToken.current = waveToken;
    if (!active || (currentAsleep ?? asleep) || waveError) return;
    triggerWave();
    riveViewRef?.playIfNeeded();
  }, [
    active,
    asleep,
    currentAsleep,
    instance,
    riveViewRef,
    triggerWave,
    waveError,
    waveToken,
  ]);

  useEffect(() => {
    if (!riveViewRef) return;
    if (active) void riveViewRef.play();
    else void riveViewRef.pause();
  }, [active, riveViewRef]);

  const problem =
    viewError ??
    fileError?.message ??
    instanceError?.message ??
    moodError?.message ??
    asleepError?.message ??
    waveError?.message;

  useEffect(() => {
    if (problem) onError?.(problem);
  }, [onError, problem]);

  return (
    <View style={[{ width: size, height: size }, style]}>
      {riveFile && instance && !problem ? (
        <RiveView
          hybridRef={setHybridRef}
          file={riveFile}
          artboardName={OLLIE_RIVE.artboard}
          stateMachineName={OLLIE_RIVE.stateMachine}
          dataBind={instance}
          autoPlay={active}
          fit={Fit.Contain}
          frameRate={frameRate}
          onError={(error) => setViewError(error.message)}
          style={StyleSheet.absoluteFillObject}
        />
      ) : (
        <Image
          source={fallbackAsset}
          resizeMode="contain"
          accessibilityLabel="Ollie"
          style={StyleSheet.absoluteFillObject}
        />
      )}
    </View>
  );
});

import { useEffect, useRef } from "react";

type EffectCallback<T> = (previousValue: T | null, currentValue: T) => void;
type DependencyList = ReadonlyArray<unknown>;

export function usePreviousEffect<T>(
  value: T,
  effect: EffectCallback<T>,
  deps: DependencyList
) {
  const previousValueRef = useRef<T | null>(null);
  const isInitialRender = useRef(true);

  useEffect(() => {
    if (!isInitialRender.current) {
      effect(previousValueRef.current, value);
    } else {
      isInitialRender.current = false;
    }
    previousValueRef.current = value;
    // eslint-disable-next-line
  }, [effect, value, ...deps]);
}

import React, { useState, useEffect } from "react";
import "./slider.css";
import { formatToCelsius } from "../utilities/format";

interface Mark {
  value: number;
  label: string;
}

interface SliderProps {
  min: number;
  max: number;
  step: number;
  defaultValue?: number;
  marks: Mark[];
  onValueChange: (value: number) => void;
}

const Slider: React.FC<SliderProps> = ({
  min,
  max,
  step,
  defaultValue = 20,
  marks,
  onValueChange,
}) => {
  const [value, setValue] = useState<number>(defaultValue);
  const [isDragging, setIsDragging] = useState<boolean>(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(event.target.value, 10);
    setValue(newValue);
  };

  const handleTouchMove = (event: React.TouchEvent<HTMLInputElement>) => {
    const { clientX, target } = event.touches[0];
    const rect = (target as HTMLElement).getBoundingClientRect();
    const newValue =
      Math.round(((clientX - rect.left) / rect.width) * (max - min)) + min;
    setValue(newValue);
  };

  useEffect(() => {
    const handleSliderRelease = () => {
      if (isDragging && onValueChange) {
        onValueChange(value);
      }
      setIsDragging(false);
    };

    const handleMouseUp = () => {
      handleSliderRelease();
    };

    // Add event listeners for mouseup and touchend
    window.addEventListener("mouseup", handleMouseUp);
    window.addEventListener("touchend", handleSliderRelease);

    // Remove event listeners on component unmount
    return () => {
      window.removeEventListener("mouseup", handleMouseUp);
      window.removeEventListener("touchend", handleSliderRelease);
    };
  }, [isDragging, value, onValueChange]);

  return (
    <div className="flex w-full sm:w-2/3 flex-col gap-1">
      <div className="text-xs text-center">{formatToCelsius(value)}</div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleChange}
        onTouchMove={handleTouchMove}
        onMouseDown={() => setIsDragging(true)}
        onTouchStart={() => setIsDragging(true)}
        className="w-full h-4 bg-blue-100 rounded-full appearance-none focus:outline-none mt-2 thumb-variant"
        list="tickmarks"
      />
      {marks.map((mark, index) => (
        <div
          key={index}
          style={{
            left: `calc(${((mark.value - min) / (max - min)) * 100}% - 10px)`,
          }}
        ></div>
      ))}
      <div className="flex justify-between">
        {marks.map((mark, index) => (
          <span
            key={index}
            className="text-xs"
            style={{
              left: `calc(${((mark.value - min) / (max - min)) * 100}% - 10px)`,
            }}
          >
            {mark.label}
          </span>
        ))}
      </div>
    </div>
  );
};

export default Slider;

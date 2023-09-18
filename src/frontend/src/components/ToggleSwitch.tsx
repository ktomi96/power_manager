import React, { useState } from "react";

interface ToggleSwitchProps {
  defaultValue: boolean;
  onValueChange: (value: boolean) => void;
}
const ToggleSwitch: React.FC<ToggleSwitchProps> = ({
  defaultValue,
  onValueChange,
}) => {
  const [isChecked, setIsChecked] = useState(defaultValue);
  const toggleSwitch = (): void => {
    setIsChecked(!isChecked);
    onValueChange(!isChecked);
  };

  return (
    <div className="relative w-14 h-8 rounded-full p-1 transition-colors duration-300">
      <label htmlFor="toggleSwitch" className="sr-only">
        Toggle Switch
      </label>
      <input
        type="checkbox"
        id="toggleSwitch"
        className={`appearance-none w-full h-full rounded-full border-2 border-gray-300 cursor-pointer ${
          isChecked ? "bg-green-500" : "bg-white"
        }`}
        checked={isChecked}
        onChange={toggleSwitch}
      />
      <div
        className={`absolute left-1 top-1 w-6 h-6 rounded-full bg-gray-100 shadow-md transition-transform duration-300 ${
          isChecked ? "transform translate-x-full" : ""
        }`}
        onClick={toggleSwitch}
      ></div>
    </div>
  );
};

export default ToggleSwitch;

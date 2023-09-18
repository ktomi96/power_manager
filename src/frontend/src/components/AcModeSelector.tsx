import React, { useEffect } from "react";
import { useForm } from "react-hook-form";

export enum AcModes {
  heating = "heating_mode",
  auto = "auto_mode",
  cooling = "cooling_mode",
}

interface FormData {
  acMode: AcModes | null;
}

interface AcModeSelectorProps {
  defaultMode?: AcModes; // Optional default mode
  onModeChange: (selectedMode: AcModes) => void; // Function to handle mode change
}

const AcModeSelector: React.FC<AcModeSelectorProps> = ({
  defaultMode,
  onModeChange,
}) => {
  const { register, setValue, watch } = useForm<FormData>();
  const currentMode = watch("acMode");

  useEffect(() => {
    if (defaultMode) {
      setValue("acMode", defaultMode);
    }
  }, [defaultMode, setValue]);

  const handleRadioChange = (value: AcModes) => {
    setValue("acMode", value);
    onModeChange(value);
  };

  return (
    <form className="p-4">
      <div>
        <label className="text-xs sm:text-lg font-semibold">AC mode</label>
        <div className="space-y-2 space-x-2 mt-2">
          <label className="inline-flex items-center">
            <input
              type="radio"
              {...register("acMode")}
              value={AcModes.heating}
              checked={currentMode === AcModes.heating}
              onChange={() => handleRadioChange(AcModes.heating)}
              className="form-radio h-5 w-5  text-blue-500"
            />
            <span className="ml-2 text-xs sm:text-base">Heating</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="radio"
              {...register("acMode")}
              value={AcModes.auto}
              checked={currentMode === AcModes.auto}
              onChange={() => handleRadioChange(AcModes.auto)}
              className="form-radio h-5 w-5 text-blue-500"
            />
            <span className="ml-2 text-xs sm:text-base">Auto</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="radio"
              {...register("acMode")}
              value={AcModes.cooling}
              checked={currentMode === AcModes.cooling}
              onChange={() => handleRadioChange(AcModes.cooling)}
              className="form-radio h-5 w-5  text-blue-500"
            />
            <span className="ml-2 text-xs sm:text-base">Cooling</span>
          </label>
        </div>
      </div>
    </form>
  );
};

export default AcModeSelector;

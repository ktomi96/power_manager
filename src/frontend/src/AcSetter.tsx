import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import AcModeSelector, { AcModes } from "./components/AcModeSelector";
import Slider from "./components/Slider";
import ToggleSwitch from "./components/ToggleSwitch";
import Button from "./components/Button";
import Loader from "./components/Loader";

interface ACApiResponse {
  mode: AcModes;
  running: boolean;
  target_temperature: string;
}

const AcSetter: React.FC = () => {
  const acSetterDisplay = useRef(true);
  const [AcModeValue, setAcModeValue] = useState<AcModes>(AcModes.auto);

  const [AcStateValue, setAcStateValue] = useState<boolean>(false);

  const [AcTemperature, setAcTemperature] = useState<number>(20);
  const [isLoading, setIsLoading] = useState(true);
  const [isPosting, setIsPosting] = useState(false);

  useEffect(() => {
    axios
      .get("/ac")
      .then((response) => {
        const { mode, running, target_temperature } =
          response.data as ACApiResponse;
        setAcModeValue(mode ?? AcModes.auto);
        setAcStateValue(running);
        setAcTemperature(parseInt(target_temperature));
        setIsLoading(false);
      })
      .catch((error) => {
        setIsLoading(false);
        console.log(error);
        acSetterDisplay.current = false;
      });
  }, []);

  const setAcApi = () => {
    setIsPosting(true);
    const data = {
      mode: AcModeValue,
      running: AcStateValue,
      target_temperature: AcTemperature.toFixed(1),
    };

    axios
      .post("/ac", data)
      .then((response) => {
        if (response.status === 200) {
          const { mode, running, target_temperature } = response.data as ACApiResponse;

          setAcModeValue(mode);
          setAcStateValue(running);
          setAcTemperature(parseInt(target_temperature));
        }
        setIsPosting(false);
      })
      .catch((error) => {
        setIsPosting(false);
        console.log(error);
      });
  };
  const marks = [
    {
      value: 20,
      label: "20°C",
    },
    {
      value: 25,
      label: "25°C",
    },
    {
      value: 30,
      label: "30°C",
    },
  ];
  return (
    <div
      className="grow
    "
    >
      {isLoading ? (
        <div className="w-full grow">
          <Loader />
        </div>
      ) : acSetterDisplay ? (
        <div className="flex flex-row flex-wrap">
          <div className="w-full sm:w-1/3">
            <div>
              <AcModeSelector
                defaultMode={AcModeValue}
                onModeChange={setAcModeValue}
              />
            </div>
          </div>
          <div className="w-full sm:w-2/3">
            <Slider
              min={20}
              max={30}
              step={1}
              marks={marks}
              defaultValue={AcTemperature}
              onValueChange={setAcTemperature}
            />
          </div>
          <div className="w-1/2">
            <div className="flex gap-2">
              <div>Off</div>
              <ToggleSwitch
                defaultValue={AcStateValue}
                onValueChange={setAcStateValue}
              />
              <div>On</div>
            </div>
          </div>
          <div className="w-1/2 text-end sm:text-left">
            <Button
              onClick={setAcApi}
              disabled={isPosting}
              text={isPosting ? "Posting" : "Set State"}
              isLoading={isPosting}
            />
          </div>
        </div>
      ) : (
        <div className="flex grow w-full">
          <div>Error loading AC data</div>
        </div>
      )}
    </div>
  );
};

export default AcSetter;

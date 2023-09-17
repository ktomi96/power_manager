import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  CircularProgress,
  Button,
  Switch,
  Typography,
  Stack,
  useTheme,
} from "@mui/material";
import ContentLoader, { IContentLoaderProps } from "react-content-loader";
import { JSX } from "react/jsx-runtime";
import AcModeSelector, { AcModes } from "./components/AcModeSelector";
import Slider from "./components/Slider";

interface ACApiResponse {
  mode: AcModes;
  running: boolean;
  target_temperature: string;
}

const AcSetter: React.FC = () => {
  const acSetterDisplay = useRef(true);
  const [AcModeValue, setAcModeValue] = useState<AcModes>(AcModes.auto);

  const [AcStateValue, setAcStateValue] = useState<boolean>(false);
  const handleAcStateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAcStateValue(event.target.checked);
  };

  const [AcTemperature, setAcTemperature] = useState<number>(20);
  const [isLoading, setIsLoading] = useState(true);
  const [isPosting, setIsPosting] = useState(false);

  const MyLoader = (props: JSX.IntrinsicAttributes & IContentLoaderProps) => {
    const theme = useTheme();
    const classes = {
      root: {
        width: "100%",
        height: "100%",
      },
      loader: {
        [theme.breakpoints.down("sm")]: {
          width: "80%", // Adjust this value for smaller devices
        },
        [theme.breakpoints.up("md")]: {
          width: "100%",
        },
        [theme.breakpoints.up("lg")]: {
          width: "60%", // Adjust this value for larger devices
        },
      },
    };

    return (
      <ContentLoader
        speed={1}
        width={1180}
        height={115}
        viewBox="0 0 1180 115"
        className={`${classes.root} ${classes.loader}`}
        backgroundColor="#deddda"
        foregroundColor="#ecebeb"
        {...props}
      >
        <rect x="0" y="11" rx="0" ry="0" width="227" height="42" />
        <rect x="141" y="103" rx="0" ry="0" width="1" height="0" />
        <rect x="1" y="78" rx="0" ry="0" width="222" height="40" />
        <rect x="255" y="33" rx="0" ry="0" width="218" height="5" />
        <rect x="369" y="87" rx="0" ry="0" width="84" height="30" />
        <circle cx="364" cy="37" r="9" />
      </ContentLoader>
    );
  };

  useEffect(() => {
    axios
      .get("/ac_status")
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
      .post("/ac_set", data)
      .then((response) => {
        if (response.status === 200) {
          const { mode, running, target_temperature } = response.data;

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
          <MyLoader />
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
              onValueChange={setAcTemperature}
            />
          </div>
          <div className="w-1/2">
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography>Off</Typography>
              <Switch
                checked={AcStateValue}
                onChange={handleAcStateChange}
                color="success"
                inputProps={{ "aria-label": "ant design" }}
              />
              <Typography>On</Typography>
            </Stack>
          </div>
          <div className="w-1/2 text-end sm:text-left">
            <Button
              variant="contained"
              size="small"
              onClick={setAcApi}
              disabled={isPosting}
              style={{ position: "relative" }}
            >
              {isPosting && (
                <CircularProgress
                  size={24}
                  color="inherit"
                  style={{
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    marginTop: -12,
                    marginLeft: -12,
                  }}
                />
              )}
              {!isPosting ? "Set State" : "Posting"}
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex grow">
          <Typography>Error loading AC data</Typography>
        </div>
      )}
    </div>
  );
};

export default AcSetter;

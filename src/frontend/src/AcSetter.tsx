import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  CircularProgress,
  Grid,
  Button,
  Slider,
  Switch,
  Typography,
  Stack,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  useTheme,
} from "@mui/material";
import ContentLoader, { IContentLoaderProps } from "react-content-loader";
import { JSX } from "react/jsx-runtime";

const AcSetter: React.FC = () => {
  const acSetterDisplay = useRef(true);
  const [AcModeValue, setAcModeValue] = useState<string>("auto_mode");

  const handleAcModeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAcModeValue(event.target.value);
  };

  const [AcStateValue, setAcStateValue] = useState<boolean>(false);
  const handleAcStateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAcStateValue(event.target.checked);
  };

  const [AcTemperature, setAcTemperature] = useState<number>(20);
  const handleAcTemperatureChange = (
    event: React.SyntheticEvent | Event,
    value: number | Array<number>
  ) => {
    setAcTemperature(value as number);
  };
  const [isLoading, setIsLoading] = useState(true);
  const [isPosting, setIsPosting] = useState(false);

  const marks = [
    {
      value: 20,
      label: "20°C",
    },
    {
      value: 30,
      label: "30°C",
    },
  ];

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

  function valuetext(value: number) {
    return `${value}°C`;
  }

  useEffect(() => {
    axios
      .get("/ac_status")
      .then((response) => {
        const { mode, running, target_temperature } = response.data;
        setAcModeValue(mode);
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

  return (
    <Grid
      container
      direction="row"
      justifyContent="flex-start"
      alignItems="flex-start"
      spacing={2}
    >
      {isLoading ? (
        <Grid item xs={12} sm={6}>
          <MyLoader />
        </Grid>
      ) : acSetterDisplay ? (
        <>
          <Grid item xs={12} sm={6}>
            <FormControl>
              <FormLabel id="row-radio-buttons-group-label">AC mode</FormLabel>
              <RadioGroup
                row
                aria-labelledby="row-radio-buttons-group-label"
                name="row-radio-buttons-group"
                value={AcModeValue}
                onChange={handleAcModeChange}
              >
                <FormControlLabel
                  value="heating_mode"
                  control={<Radio />}
                  label="Heating"
                />
                <FormControlLabel
                  value="auto_mode"
                  control={<Radio />}
                  label="Auto"
                />
                <FormControlLabel
                  value="cooling_mode"
                  control={<Radio />}
                  label="Cooling"
                />
              </RadioGroup>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Slider
              aria-label="Custom marks"
              defaultValue={20}
              getAriaValueText={valuetext}
              step={1}
              valueLabelDisplay="auto"
              marks={marks}
              min={20}
              max={30}
              value={AcTemperature}
              onChangeCommitted={handleAcTemperatureChange}
            />
          </Grid>
          <Grid item xs={6}>
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
          </Grid>
          <Grid item xs={6}>
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
          </Grid>
        </>
      ) : (
        <Grid item xs={12}>
          <Typography>Error loading AC data</Typography>
        </Grid>
      )}
    </Grid>
  );
};

export default AcSetter;

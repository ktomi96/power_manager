import React, { useState, useEffect } from "react";
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
} from "@mui/material";

function AcSetter() {
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
        <CircularProgress /> // Render CircularProgress if isLoading is true
      ) : (
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
      )}
    </Grid>
  );
}

export default AcSetter;

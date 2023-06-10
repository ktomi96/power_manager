import React from "react";
import DatePicker from "react-datepicker";
import moment from "moment";
import { useState } from "react";
import { Grid, Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import ACPlot from "./AcPlot";
import SolarPlot from "./SolarPlot";
import AcSetter from "./AcSetter";
import "react-datepicker/dist/react-datepicker.css";
import { DateRange } from "./hooks/useChartData";
import SolarSum from "./SolarSum";

const App: React.FC = () => {
  const today = moment();
  const todayDate: Date = today.toDate();
  const yesterday = today.subtract(1, "day");
  const yesterdayDate = yesterday.toDate();
  const lastMonth = yesterday.subtract(1, "month").toDate();
  // Set default start date as the first day of the month and end date as yesterday for solar data
  const [solarDateRange, setSolarDateRange] = useState<DateRange>({
    startDate: lastMonth,
    endDate: yesterdayDate,
  });
  // Set default start date as today and end date as tomorrow for AC data
  const [acDateRange, setAcDateRange] = useState<DateRange>({
    startDate: todayDate,
    endDate: todayDate,
  });

  const onSolDateChange = (dates: [Date | null, Date | null]) => {
    const [start, end] = dates;
    setSolarDateRange({
      startDate: start,
      endDate: end,
    });
  };

  const onACDateChange = (dates: [Date | null, Date | null]) => {
    const [start, end] = dates;
    setAcDateRange({
      startDate: start,
      endDate: end,
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
      <Grid item xs={12}>
        <h1>Solar and AC data</h1>
      </Grid>
      <Grid item xs={12} sm={4}>
        <SolarSum solarDateRange={solarDateRange} />
      </Grid>
      <Grid item xs={12} sm={8}>
        <AcSetter />
      </Grid>
      <Grid item xs={12} sm={6}>
        <Grid
          container
          direction="row"
          justifyContent="flex-start"
          alignItems="flex-start"
        >
          <Grid item xs={8}>
            <DatePicker
              selectsRange={true}
              dateFormat="yyyy/MM/dd"
              startDate={solarDateRange.startDate}
              endDate={solarDateRange.endDate}
              onChange={onSolDateChange}
            />
          </Grid>
          <Grid item xs={4}>
            <Button
              variant="contained"
              color="primary"
              size="small"
              endIcon={<SendIcon />}
              onClick={() => {
                setSolarDateRange({
                  startDate: lastMonth,
                  endDate: yesterdayDate,
                }); // Reset start date as the first day of the month and end date as yesterday for solar data
              }}
            >
              Reset
            </Button>
          </Grid>
          <Grid item xs={12}>
            <SolarPlot solarDateRange={solarDateRange} />
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12} sm={6}>
        <Grid
          container
          direction="row"
          justifyContent="flex-start"
          alignItems="flex-start"
        >
          <Grid item xs={8}>
            <DatePicker
              selectsRange={true}
              dateFormat="yyyy/MM/dd"
              startDate={acDateRange.startDate}
              endDate={acDateRange.endDate}
              onChange={onACDateChange}
            />
          </Grid>
          <Grid item xs={4}>
            <Button
              variant="contained"
              color="primary"
              size="small"
              endIcon={<SendIcon />}
              onClick={() => {
                setAcDateRange({
                  startDate: todayDate,
                  endDate: todayDate,
                }); // Reset start date as today and end date as tomorrow for AC data
              }}
            >
              Reset
            </Button>
          </Grid>
          <Grid item xs={12}>
            <ACPlot acDateRange={acDateRange} />
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default App;

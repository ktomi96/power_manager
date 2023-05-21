import DatePicker from "react-datepicker";
import moment from "moment";
import { useEffect, useState } from "react";
import { Grid } from "@mui/material";
import ACPlot from "./acplot";
import SolarPlot from "./solarplot";
import "react-datepicker/dist/react-datepicker.css";

function formatDateToString(date: Date | null): string {
  if (date === null) {
    return "";
  }
  return moment(date).format("YYYY-MM-DD");
}
function useChartData(fetchUrl: string, dateRange: [Date | null, Date | null]) {
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    const [startDate, endDate] = dateRange;
    const formattedStartDate = formatDateToString(startDate);
    const formattedEndDate = formatDateToString(endDate);

    if (formattedStartDate && formattedEndDate) {
      fetch(
        `${fetchUrl}?start_date=${formattedStartDate}&end_date=${formattedEndDate}`
      )
        .then((res) => res.json())
        .then(setChartData);
    } else {
      setChartData([]);
    }
  }, [fetchUrl, dateRange]);

  return chartData;
}

function App() {
  const today = moment();
  const todayDate = today.toDate();
  const yesterday = today.subtract(1, "day");
  const yesterdayDate = yesterday.toDate();
  const lastMonth = yesterday.subtract(1, "month").toDate();
  const [solarDateRange, setSolarDateRange] = useState<
    [Date | null, Date | null]
  >([lastMonth, yesterdayDate]); // Set default start date as the first day of the month and end date as yesterday for solar data
  const [acDateRange, setAcDateRange] = useState<[Date | null, Date | null]>([
    todayDate,
    todayDate,
  ]); // Set default start date as today and end date as tomorrow for AC data

  const solarJson = useChartData("/solar", solarDateRange);
  const acJson = useChartData("/ac", acDateRange);

  return (
    <Grid
      container
      direction="row"
      justifyContent="flex-start"
      alignItems="flex-start"
      spacing={2}
      columns={{ xs: 4, sm: 8, md: 12 }}
    >
      <Grid item xs={12}>
        <h1>Solar and AC data</h1>
      </Grid>
      <Grid item xs={6} sm={2}>
        <p>Select date for Solar graph</p>
      </Grid>
      <Grid item xs={6} sm={3}>
        <DatePicker
          selectsRange={true}
          dateFormat="yyyy/MM/dd"
          startDate={solarDateRange[0]}
          endDate={solarDateRange[1]}
          onChange={setSolarDateRange}
        />
      </Grid>
      <Grid item xs={6} sm={2}>
        <p>Select date for AC graph</p>
      </Grid>
      <Grid item xs={6} sm={3}>
        <DatePicker
          selectsRange={true}
          dateFormat="yyyy/MM/dd"
          startDate={acDateRange[0]}
          endDate={acDateRange[1]}
          onChange={setAcDateRange}
        />
      </Grid>
      <Grid item xs={12} sm={2}>
        <button
          className="btn btn-secondary"
          onClick={() => {
            setSolarDateRange([lastMonth, yesterdayDate]); // Reset start date as the first day of the month and end date as yesterday for solar data

            setAcDateRange([todayDate, todayDate]); // Reset start date as today and end date as tomorrow for AC data
          }}
        >
          Reset
        </button>
      </Grid>
      <Grid item xs={12} sm={6}>
        <SolarPlot solarJson={solarJson} />
      </Grid>

      <Grid item xs={12} sm={6}>
        <ACPlot acJson={acJson} />
      </Grid>
    </Grid>
  );
}

export default App;

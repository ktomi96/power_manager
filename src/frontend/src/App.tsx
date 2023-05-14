import DatePicker from "react-datepicker";
import { useEffect, useState } from "react";
import ACPlot from "./acplot";
import SolarPlot from "./solarplot";
import "react-datepicker/dist/react-datepicker.css";

function formatDateToString(date: Date | null): string {
  if (date === null) {
    return "";
  }
  return date.toISOString().split("T")[0];
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
        .then((json) => {
          setChartData(json);
        });
    } else {
      setChartData([]);
    }
  }, [fetchUrl, dateRange]);

  return chartData;
}

function App() {
  const [solarDateRange, setSolarDateRange] = useState<
    [Date | null, Date | null]
  >([
    new Date(new Date().getFullYear(), new Date().getMonth(), 1),
    new Date(Date.now() - 24 * 60 * 60 * 1000),
  ]); // Set default start date as the first day of the month and end date as yesterday for solar data
  const [acDateRange, setAcDateRange] = useState<[Date | null, Date | null]>([
    new Date(),
    new Date(Date.now() + 24 * 60 * 60 * 1000),
  ]); // Set default start date as today and end date as tomorrow for AC data

  const solarJson = useChartData("/solar", solarDateRange);
  const acJson = useChartData("/ac", acDateRange);

  const handleSolarDateChange = (update: [Date | null, Date | null]) => {
    setSolarDateRange(update);
  };

  const handleACDateChange = (update: [Date | null, Date | null]) => {
    setAcDateRange(update);
  };

  return (
    <div className="row p-4">
      <div
        className="card m-auto"
        style={{ width: "90%" }}
        data-aos="fade-left"
      >
        <div className="card-body">
          <h1>Solar and AC data</h1>
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
        <p>Select date for Solar graph</p>
          <DatePicker
            selectsRange={true}
            dateFormat="yyyy/MM/dd"
            startDate={solarDateRange[0]}
            endDate={solarDateRange[1]}
            onChange={handleSolarDateChange}
          />
          <p>Select date for AC graph</p>
          <DatePicker
            selectsRange={true}
            dateFormat="yyyy/MM/dd"
            startDate={acDateRange[0]}
            endDate={acDateRange[1]}
            onChange={handleACDateChange}
          />
          <button
            className="btn btn-secondary"
            onClick={() => {
              setSolarDateRange([
                new Date(new Date().getFullYear(), new Date().getMonth(), 1),
                new Date(Date.now() - 24 * 60 * 60 * 1000),
              ]); // Reset start date as the first day of the month and end date as yesterday for solar data

              setAcDateRange([
                new Date(),
                new Date(Date.now() + 24 * 60 * 60 * 1000),
              ]); // Reset start date as today and end date as tomorrow for AC data
            }}
          >
            Clear
          </button>
        </div>
        <div>
          <SolarPlot solarJson={solarJson} />
        </div>
      </div>
      <ACPlot acJson={acJson} />
    </div>
  );
}

export default App;

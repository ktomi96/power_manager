import React from "react";
import DatePicker from "react-datepicker";
import moment from "moment";
import { useState } from "react";
import { Button } from "@mui/material";
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
    <div className="flex flex-row flex-wrap gap-2 flex-auto">
      <div className="w-full">
        <h1>Solar and AC data</h1>
      </div>
      <div className="flex w-full gap-4 flex-auto flex-wrap">
        <div className="sm:w-full sm:grow">
          <SolarSum solarDateRange={solarDateRange} />
        </div>
        <div className="grow">
          <AcSetter />
        </div>
      </div>
      <div className="flex grow w-full sm:w-1/2">
        <div className="grid grid-cols-2 gap-4 grow">
          <div>
            <DatePicker
              selectsRange={true}
              dateFormat="yyyy/MM/dd"
              startDate={solarDateRange.startDate}
              endDate={solarDateRange.endDate}
              onChange={onSolDateChange}
            />
          </div>
          <div>
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
          </div>

          <div className="col-span-2">
            <SolarPlot solarDateRange={solarDateRange} />
          </div>
        </div>
      </div>
      <div className="flex grow">
        <div className="grid grid-cols-2 gap-4 grow">
          <div>
            <DatePicker
              selectsRange={true}
              dateFormat="yyyy/MM/dd"
              startDate={acDateRange.startDate}
              endDate={acDateRange.endDate}
              onChange={onACDateChange}
            />
          </div>
          <div>
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
          </div>
          <div className="col-span-2">
            <ACPlot acDateRange={acDateRange} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

import { useEffect, useState } from "react";
import { formatDateToString } from "../utilities/format";
import axios from "axios";
import { DateRange } from "./useChartData";

export function useSumSolarData(fetchUrl: string, dateRange: DateRange) {
  const [sumSolarData, setSumSolarData] = useState<number>(0);
  const [error, setError] = useState<boolean>(false);

  useEffect(() => {
    const { startDate, endDate } = dateRange;
    const formattedStartDate = formatDateToString(startDate);
    const formattedEndDate = formatDateToString(endDate);

    if (formattedStartDate && formattedEndDate) {
      axios
        .get(
          `${fetchUrl}?start_date=${formattedStartDate}&end_date=${formattedEndDate}`
        )
        .then((res) => {
          setSumSolarData(res.data);
          setError(false);
        })
        .catch((error) => {
          setSumSolarData(0);
          console.error(error);
        });
    }
  }, [fetchUrl, dateRange]);

  if (error) {
    setSumSolarData(0);
  }

  return sumSolarData / 1000;
}

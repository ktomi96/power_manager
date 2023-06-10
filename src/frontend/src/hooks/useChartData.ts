import axios from "axios";
import { useEffect, useState } from "react";
import { formatDateToString } from "../utilities/format";

export type DateRange = {
  startDate: Date | null;
  endDate: Date | null;
};

export function useChartData<T>(fetchUrl: string, dateRange: DateRange): T[] | null {
  const [chartData, setChartData] = useState<T[]>([]);
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
          setChartData(res.data);
          setError(false);
        })
        .catch((error) => {
          console.error(error);
        });
    } else {
      setChartData([]);
      setError(false);
    }
  }, [fetchUrl, dateRange]);

  if (error) {
    return null;
  }

  return chartData;
}

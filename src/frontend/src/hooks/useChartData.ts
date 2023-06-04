import axios from "axios";
import { useEffect, useState } from "react";
import { formatDateToString } from "../utilities/format";

export type DateRange = {
  startDate: Date | null;
  endDate: Date | null;
};

export function useChartData<T>(fetchUrl: string, dateRange: DateRange): T[] {
  const [chartData, setChartData] = useState<T[]>([]);

  useEffect(() => {
    const { startDate, endDate } = dateRange;
    const formattedStartDate = formatDateToString(startDate);
    const formattedEndDate = formatDateToString(endDate);

    if (formattedStartDate && formattedEndDate) {
      axios
        .get(
          `${fetchUrl}?start_date=${formattedStartDate}&end_date=${formattedEndDate}`
        )
        .then((res) => res.data)
        .then(setChartData);
    } else {
      setChartData([]);
    }
  }, [fetchUrl, dateRange]);

  return chartData;
}

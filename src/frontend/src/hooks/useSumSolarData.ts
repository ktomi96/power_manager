import { useEffect, useState } from "react";
import { formatDateToString } from "../utilities/format";
import axios from "axios";
import { DateRange } from "./useChartData";

export function useSumSolarData(fetchUrl: string, dateRange: DateRange) {
    const [sumSolarData, setSumSolarData] = useState<number>(0);
  
    useEffect(() => {
      const {startDate, endDate} = dateRange;
      const formattedStartDate = formatDateToString(startDate);
      const formattedEndDate = formatDateToString(endDate);
  
      if (formattedStartDate && formattedEndDate) {
        axios
          .get(`${fetchUrl}?start_date=${formattedStartDate}&end_date=${formattedEndDate}`)
          .then((res) => res.data)
          .then(setSumSolarData);
      } else {
        setSumSolarData(0);
      }
    }, [fetchUrl, dateRange]);
  
    return sumSolarData / 1000;
  }
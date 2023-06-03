import React from "react";
import { DateRange } from "./hooks/useChartData";
import { useSumSolarData } from "./hooks/useSumSolarData";

interface SolarSumProperties {
  solarDateRange: DateRange;
}

const SolarSum: React.FC<SolarSumProperties> = ({ solarDateRange }) => {
  const TotalSolar = () => {
    const solarSum = useSumSolarData("/solar_sum", solarDateRange);
    if (solarSum > 1000) {
      return <>{(solarSum / 1000).toFixed(2)} MWh</>;
    }
    return <>{solarSum.toFixed(2)} kWh</>;
  };

  return <div>Total Solar power: {TotalSolar()}</div>;
};

export default SolarSum;

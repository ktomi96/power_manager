import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  ChartData,
  Chart as ChartJS,
  ChartOptions,
  Legend,
  Title,
  Tooltip,
} from "chart.js/auto";
import { DateRange, useChartData } from "./hooks/useChartData";
import { usePreviousEffect } from "./hooks/usePreviusEffect";

ChartJS.register(Title, Tooltip, Legend);

export interface ac {
  id: number;
  running: boolean;
  indoor_temperature: number;
  out_door_temperature: number;
  date_time: string;
}
interface AcPlotProps {
  acDateRange: DateRange;
}

const ACPlot: React.FC<AcPlotProps> = ({ acDateRange }) => {
  const acJson = useChartData<ac>("/ac_plot", acDateRange);
  const [currAcJson, setCurrAcJson] = useState<ac[] | null>(acJson);

  usePreviousEffect(
    acJson,
    (prev, curr) => {
      if (curr && curr.length > 0) {
        setCurrAcJson(curr);
      } else if (curr === null || (prev && prev.length === 0 && curr.length > prev.length)) {
        setCurrAcJson(curr);
      } else if (prev && curr && curr.length < prev.length) {
        setCurrAcJson(prev);
      }
    },
    [acJson, acDateRange]
  );
  if (!currAcJson || currAcJson.length === 0) {
    return <h1>There is no data for the AC chart</h1>;
  }

  const filteredAcJson = currAcJson.reduce((acc: ac[], curr: ac, i): ac[] => {
    const prev = acc[i - 1];
    const currIndoorTemp = curr.indoor_temperature;
    const currOutdoorTemp = curr.out_door_temperature;
    if (
      !prev ||
      Math.abs(currIndoorTemp - prev.indoor_temperature) > 10 ||
      !prev ||
      Math.abs(currOutdoorTemp - prev.out_door_temperature) > 10
    ) {
      acc.push({
        id: prev?.id ?? curr.id,
        date_time: curr.date_time,
        running: prev?.running ?? curr.running,
        out_door_temperature: prev?.out_door_temperature ?? currOutdoorTemp,
        indoor_temperature: prev?.indoor_temperature ?? currIndoorTemp,
      });
    } else {
      acc.push(curr);
    }
    return acc;
  }, []);

  const acDateMod = filteredAcJson.map((x) => {
    const date = new Date(x.date_time);
    return date.toLocaleString();
  });

  const acData: ChartData<"line", number[], string> = {
    labels: acDateMod,
    datasets: [
      {
        label: "Indoor temperature",
        data: filteredAcJson.map((x) => x.indoor_temperature),
        fill: false,
        yAxisID: "y",
      },
      {
        label: "Outdoor temperature",
        data: filteredAcJson.map((x) => x.out_door_temperature),
        fill: false,
        yAxisID: "y",
      },
      {
        label: "AC status",
        data: filteredAcJson.map((x) => (x.running ? 1 : 0)),
        fill: false,
        yAxisID: "y1",
      },
    ],
  };

  const acOptions: ChartOptions<"line"> = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: "right",
        align: "center",
        display: true,
        labels: {
          usePointStyle: true,
          boxWidth: 10,
          padding: 20,
        },
      },
      title: {
        display: true,
        text: "AC Plot",
      },
    },
    layout: {
      padding: {
        left: 0,
        right: 0,
        top: 10,
        bottom: 0,
      },
    },
    scales: {
      x: {
        display: true,
        type: "category",
        ticks: {
          display: false,
        },
        grid: {
          display: false,
        },
      },
      y: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          display: true,
        },
      },
      y1: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          display: false,
        },
      },
    },
    elements: {
      point: {
        radius: 0,
      },
    },
    interaction: {
      mode: "index",
      intersect: false,
    },
    animation: {
      duration: 0,
    },
  };

  return <Line data={acData} options={acOptions} />;
};

export default ACPlot;

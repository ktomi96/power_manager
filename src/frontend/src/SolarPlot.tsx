import React from "react";
import { Bar } from "react-chartjs-2";
import {
  ChartData,
  Chart as ChartJS,
  ChartOptions,
  Legend,
  Title,
  Tooltip,
} from "chart.js/auto";
import { DateRange, useChartData } from "./hooks/useChartData";

ChartJS.register(Title, Tooltip, Legend);

export interface solar {
  id: number;
  date_time: string;
  power_generated: number;
  production_time: number;
  daytime: number;
  efficiency: number;
}

interface SolarPlotProps {
  solarDateRange: DateRange;
}

const SolarPlot: React.FC<SolarPlotProps> = ({ solarDateRange }) => {
  const solarJson = useChartData<solar>("/solar", solarDateRange);
  if (!solarJson || solarJson.length === 0) {
    return <h1>There is no data for the Solar chart</h1>;
  }

  const solarData: ChartData<"bar", number[], string> = {
    labels: solarJson.map((x) => x.date_time),
    datasets: [
      {
        label: "Power Generated",
        data: solarJson.map((y) => y.power_generated),
        backgroundColor: "green",
        borderColor: "green",
        borderWidth: 1,
      },
    ],
  };

  const solarOptions: ChartOptions<"bar"> = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      title: {
        display: true,
        text: "Solar Plot",
      },
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
    },
    scales: {
      x: {
        ticks: {
          display: true,
          autoSkip: true,
          maxTicksLimit: 10,
          maxRotation: 0,
          minRotation: 0,
        },
      },
      y: {
        type: "linear",
        position: "left",
        grid: {
          display: true,
        },
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
    animation: {
      duration: 0,
    },
  };

  return <Bar data={solarData} options={solarOptions} />;
};

export default SolarPlot;

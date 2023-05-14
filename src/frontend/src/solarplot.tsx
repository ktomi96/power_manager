import { Data, Layout, Template } from "plotly.js";
import Plot from "react-plotly.js";

export interface solar {
  id: number;
  date_time: string;
  power_generated: number;
  production_time: number;
  daytime: number;
  efficeny: number;
}

interface SolarPlotProps {
  solarJson: solar[];
}

function SolarPlot({ solarJson }: SolarPlotProps) {
  if (!solarJson || solarJson.length === 0) {
    return <h1>There is no data for the Solar chart</h1>;
  }

  const solarData: Data[] = [
    {
      x: solarJson.map((x) => x.date_time),
      y: solarJson.map((y) => y.power_generated),
      type: "bar",
      mode: "lines+markers",
      marker: { color: "green" },
    },
  ];

  const solarLayout: Partial<Layout> = {
    template: "plotly_white" as Template,
    width: 800,
    height: 400,
    title: "Solar Plot",
  };

  return <Plot data={solarData} layout={solarLayout} />;
}

export default SolarPlot;

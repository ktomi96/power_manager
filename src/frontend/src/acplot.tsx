import { Template } from 'plotly.js';
import { Data, Layout } from 'plotly.js';
import Plot from 'react-plotly.js';

export interface ac {
  id: number;
  running: boolean;
  indoor_temperature: number;
  out_door_temperature: number;
  date_time: string;
}

interface ACPlotProps {
  acJson: ac[];
}

function ACPlot({ acJson }: ACPlotProps) {
  if (!acJson || acJson.length === 0) {
    return <h1>There is no data for the AC chart</h1>;
  }

  const filteredAcJson = acJson.reduce((acc: ac[], curr: ac, i): ac[] => {
    const prev = acc[i - 1];
    const currIndoorTemp = curr.indoor_temperature;
    const currOutdoorTemp = curr.out_door_temperature;
    if (
      (!prev || Math.abs(currIndoorTemp - prev.indoor_temperature) > 10) ||
      (!prev || Math.abs(currOutdoorTemp - prev.out_door_temperature) > 10)
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

  const acData: Data[] = [
    {
      x: acDateMod,
      y: filteredAcJson.map((x) => x.indoor_temperature),
      type: "scatter",
      name: "Indoor temperature",
      yaxis: "y1",
    },
    {
      x: acDateMod,
      y: filteredAcJson.map((x) => x.out_door_temperature),
      type: "scatter",
      name: "Outdoor temperature",
      yaxis: "y1",
    },
    {
      x: acDateMod,
      y: filteredAcJson.map((x) => (x.running ? "Running" : "Not Running")),
      type: "scatter",
      name: "AC status",
      yaxis: "y2",
    },
  ];

  const acLayout: Partial<Layout> = {
    template: "plotly_white" as Template,
    width: 800,
    height: 400,
    title: "AC Plot",
    xaxis: {
      showticklabels: false,
    },
    yaxis: {
      side: "left",
      showgrid: false,
    },
    yaxis2: {
      side: "right",
      overlaying: "y",
      showgrid: false,
    },
  };

  return <Plot data={acData} layout={acLayout} />;
}

export default ACPlot;

import { Line } from 'react-chartjs-2';
import { ChartData, Chart as ChartJS, ChartOptions, Legend, Title, Tooltip } from 'chart.js/auto';

ChartJS.register(
  Title,
  Tooltip,
  Legend
);

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

  const acData: ChartData<'line', number[], string> = {
    labels: acDateMod,
    datasets: [
      {
        label: 'Indoor temperature',
        data: filteredAcJson.map((x) => x.indoor_temperature),
        fill: false,
        yAxisID: 'y',
      },
      {
        label: 'Outdoor temperature',
        data: filteredAcJson.map((x) => x.out_door_temperature),
        fill: false,
        yAxisID: 'y',
      },
      {
        label: 'AC status',
        data: filteredAcJson.map((x) => (x.running ? 1 : 0)),
        fill: false,
        yAxisID: 'y1',
      },
    ],
  };

  const acOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'right',
        align: 'center',
        display: true,
        labels: {
          usePointStyle: true,
          boxWidth: 10,
          padding: 20,
        },
      },
      title: {
        display: true,
        text: 'AC Plot',
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
        type: 'category',
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
        }
      },
      y1: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          display: false,}

      },
    },
    elements: {
      point: {
        radius: 0,
      },
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
    animation: {
      duration: 0,
    },
  };

  return <Line data={acData} options={acOptions} />;
}

export default ACPlot;

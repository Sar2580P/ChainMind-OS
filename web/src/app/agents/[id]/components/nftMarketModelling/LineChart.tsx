"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const LineChart = ({
  title,
  dataset,
}: {
  title: string;
  dataset: { [key: string]: number[] };
}) => {
  const labels = Array.from(
    { length: dataset[Object.keys(dataset)[0]].length },
    (_, i) => i + 1
  );

  const chartData = {
    labels,
    datasets: Object.keys(dataset).map((key, index) => ({
      label: key,
      data: dataset[key],
      borderColor: `hsl(${index * 90}, 70%, 50%)`,
      backgroundColor: `hsl(${index * 90}, 70%, 80%)`,
    })),
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: title,
        color: "#ffffff",
      },
    },
    scales: {
      x: {
        type: "linear" as const,
        grid: {
          color: "#ffffff" as const,
        },
      },
      y: {
        type: "linear" as const,
        grid: {
          color: "#ffffff" as const,
        },
      },
    },
    animation: {
      duration: 0,
    },
  };

  return (
    <Line
      data={chartData}
      options={options}
      style={{
        width: "-webkit-fill-available",
        borderBottom: "2px dashed #ffffff",
      }}
    />
  );
};

export default LineChart;

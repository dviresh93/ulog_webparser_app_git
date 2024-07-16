import React from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const AccelChart = ({ accelData }) => {
  const data = {
    labels: accelData.accel_x_hover.map((_, index) => index), // Assuming equal length arrays
    datasets: [
      {
        label: 'Accel X',
        data: accelData.accel_x_hover,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Accel Y',
        data: accelData.accel_y_hover,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
      {
        label: 'Accel Z',
        data: accelData.accel_z_hover,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  };

  return <Line data={data} />;
};

export default AccelChart;
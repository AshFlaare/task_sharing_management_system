<template>
    <Bar
      :data="chartData"
      :options="chartOptions"
    />
  </template>
  
  <script setup>
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
  } from 'chart.js';
  import { Bar } from 'vue-chartjs';
  import { computed } from 'vue';
  
  ChartJS.register(
    Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale
  );
  
  const props = defineProps({
    statusCounts: Object
  });
  
  // Сделать chartData реактивным, чтобы он обновлялся при изменении props
  const chartData = computed(() => ({
    labels: Object.keys(props.statusCounts || {}),
    datasets: [
      {
        label: 'Количество задач',
        backgroundColor: '#3498db',
        data: Object.values(props.statusCounts || {})
      }
    ]
  }));
  
  const chartOptions = {
    responsive: true,
    indexAxis: 'y', // горизонтальная диаграмма
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        beginAtZero: true
      }
    }
  };
  </script>
  
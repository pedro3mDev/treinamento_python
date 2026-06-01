/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'Organic',
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: [43, 48, 40, 54, 67, 73, 70],
        fill: false,
      },
      {
        label: 'Paid',
        fill: false,
        backgroundColor: '#1c64f2',
        borderColor: '#1c64f2',
        data: [24, 50, 64, 74, 52, 51, 65],
      },
    ],
  },
  options: {
    responsive: true,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Month',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Value',
        },
      },
    },
  },
}
const lineConfigEnc = {
  type: 'line',
  data: {
    labels: ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
    datasets: [
      {
        label: 'Organic',
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: [43, 48, 40, 54, 67, 73, 70],
        fill: false,
      },
      {
        label: 'Encomendas',
        fill: false,
        backgroundColor: '#1c64f2',
        borderColor: '#1c64f2',
        data: [24, 50, 64, 74, 52, 51, 65],
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
   
  },
}
const lineCtx = document.getElementById('line')
window.myLine = new Chart(lineCtx, lineConfig)
const lineCtx0 = document.getElementById('line0')
window.myLine = new Chart(lineCtx0, lineConfig)
const lineCtxEnc = document.getElementById('lineEnc')
window.myLine = new Chart(lineCtxEnc, lineConfigEnc)
window.myLine = new Chart(lineCtx0, lineConfig)
const lineCtxE = document.getElementById('lineE')
window.myLine = new Chart(lineCtxE, lineConfigEnc)

/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const barConfig = {
  type: 'bar',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'Shoes',
        backgroundColor: '#0694a2',
        // borderColor: window.chartColors.red,
        borderWidth: 1,
        data: [-3, 14, 52, 74, 33, 90, 70],
      },
      {
        label: 'Bags',
        backgroundColor: '#7e3af2',
        // borderColor: window.chartColors.blue,
        borderWidth: 1,
        data: [66, 33, 43, 12, 54, 62, 84],
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
  },
}
const barConfigMF = {
  type: 'bar',
  data: {
    labels: ['Cozinheiro', 'Gerente', 'Garçon', 'ssss', 'ssss', 'ssss', 'ssss'],
    datasets: [
      {
        label: 'Mulheres',
        backgroundColor: '#ca4a4a',
        // borderColor: window.chartColors.red,
        borderWidth: 1,
        data: [-3, 14, 52, 74, 33, 90, 70],
      },
      {
        label: 'Homens',
        backgroundColor: '#3f83f8',
        // borderColor: window.chartColors.blue,
        borderWidth: 1,
        data: [66, 33, 43, 12, 54, 62, 84],
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
  },
}

const barsCtx = document.getElementById('bars')
window.myBar = new Chart(barsCtx, barConfig)
const barsCtxMF = document.getElementById('barsMF')
window.myBar = new Chart(barsCtxMF, barConfigMF)

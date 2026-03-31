<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Linearity Assessment' },
  /**
   * Array of data points: [{ x: logConcentration, y: ctValue }]
   */
  points: { type: Array, required: true },
  /** Regression slope */
  slope: { type: Number, default: -3.32 },
  /** Regression intercept */
  intercept: { type: Number, default: 38 },
  /** R-squared value */
  rSquared: { type: Number, default: 0.998 },
  height: { type: Number, default: 380 },
})

const chartEl = ref(null)

async function render() {
  const Plotly = await import('plotly.js-dist-min')

  const xs = props.points.map(p => p.x)
  const ys = props.points.map(p => p.y)

  // Data points
  const dataTrace = {
    x: xs,
    y: ys,
    mode: 'markers',
    type: 'scatter',
    marker: { color: '#64B5F6', size: 9, symbol: 'circle',
      line: { color: '#fff', width: 1 } },
    name: 'Observed',
    showlegend: true,
    hovertemplate: 'Log conc: %{x:.1f}<br>Ct: %{y:.1f}<extra></extra>',
  }

  // Regression line
  const xMin = Math.min(...xs) - 0.3
  const xMax = Math.max(...xs) + 0.3
  const regX = [xMin, xMax]
  const regY = regX.map(x => props.slope * x + props.intercept)

  const regTrace = {
    x: regX,
    y: regY,
    mode: 'lines',
    type: 'scatter',
    line: { color: '#43A047', width: 2 },
    name: `Regression (R² = ${props.rSquared.toFixed(3)})`,
    showlegend: true,
    hoverinfo: 'skip',
  }

  const efficiency = (Math.pow(10, -1 / props.slope) - 1) * 100

  const annotations = [
    {
      x: 0.98, y: 0.05, xref: 'paper', yref: 'paper',
      text: `y = ${props.slope.toFixed(2)}x + ${props.intercept.toFixed(1)}<br>R² = ${props.rSquared.toFixed(4)}<br>Efficiency = ${efficiency.toFixed(1)}%`,
      showarrow: false,
      font: { color: '#B6BDC7', size: 11 },
      align: 'right',
      xanchor: 'right',
      bgcolor: 'rgba(18, 22, 27, 0.85)',
      bordercolor: '#262D36',
      borderwidth: 1,
      borderpad: 6,
    },
  ]

  const layout = {
    title: { text: props.title, font: { color: '#F3F4F6', size: 15 } },
    paper_bgcolor: '#12161B',
    plot_bgcolor: '#12161B',
    margin: { l: 55, r: 30, t: 50, b: 50 },
    height: props.height,
    xaxis: {
      title: { text: 'Log Concentration (copies/mL)', font: { color: '#8E97A3', size: 12 } },
      color: '#8E97A3', gridcolor: '#262D36', zerolinecolor: '#262D36',
    },
    yaxis: {
      title: { text: 'Ct Value', font: { color: '#8E97A3', size: 12 } },
      color: '#8E97A3', gridcolor: '#262D36', zerolinecolor: '#262D36',
      autorange: 'reversed', // Higher Ct = lower concentration, so reverse
    },
    annotations,
    legend: {
      font: { color: '#8E97A3', size: 11 },
      bgcolor: 'rgba(18, 22, 27, 0.8)',
      bordercolor: '#262D36',
      borderwidth: 1,
    },
  }

  const config = { displayModeBar: false, responsive: true }

  Plotly.default.newPlot(chartEl.value, [dataTrace, regTrace], layout, config)
}

onMounted(render)
watch(() => props.points, render)
</script>

<template>
  <div ref="chartEl" class="plotly-linearity-diagram"></div>
</template>

<style scoped>
.plotly-linearity-diagram {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  border: 1px solid var(--border-subtle);
}
</style>

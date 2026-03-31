<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  title: { type: String, default: 'NMEDx Chart (Normalized Method Decision Chart)' },
  /**
   * Array of assay data points:
   * [{ name: 'Assay A', cvTEa: 0.12, biasTEa: 0.25, sigma: 4.5 }]
   */
  assays: { type: Array, required: true },
  height: { type: Number, default: 400 },
})

const chartEl = ref(null)

function sigmaColor(sigma) {
  if (sigma >= 6) return '#43A047'
  if (sigma >= 5) return '#66BB6A'
  if (sigma >= 4) return '#F9A825'
  if (sigma >= 3) return '#FF9800'
  if (sigma >= 2) return '#E53935'
  return '#B71C1C'
}

function sigmaLabel(sigma) {
  if (sigma >= 6) return 'World Class'
  if (sigma >= 5) return 'Excellent'
  if (sigma >= 4) return 'Good'
  if (sigma >= 3) return 'Marginal'
  if (sigma >= 2) return 'Poor'
  return 'Unacceptable'
}

async function render() {
  const Plotly = await import('plotly.js-dist-min')

  // Background sigma band shapes
  // On the NMEDx chart: sigma = (1 - biasTEa) / cvTEa
  // So biasTEa = 1 - sigma * cvTEa
  // Each sigma line goes from (0, 1-sigma*0) to (cvMax, 1-sigma*cvMax)
  // Clipped to biasTEa >= 0

  const sigmaLines = [
    { sigma: 6, color: '#43A047', label: '6 Sigma' },
    { sigma: 5, color: '#66BB6A', label: '5 Sigma' },
    { sigma: 4, color: '#F9A825', label: '4 Sigma' },
    { sigma: 3, color: '#FF9800', label: '3 Sigma' },
    { sigma: 2, color: '#E53935', label: '2 Sigma' },
  ]

  const shapes = []
  const annotations = []

  // Draw filled bands between sigma lines
  // We use shapes with type 'path' or overlay traces for filled regions
  // Simpler: use scatter traces with fill

  const bandTraces = []
  const cvMax = 0.40

  // Create filled area traces for each band (from outer to inner so layering is correct)
  const bandDefs = [
    { sigmaLow: null, sigmaHigh: 2, color: 'rgba(183, 28, 28, 0.15)', name: '< 2 Sigma' },
    { sigmaLow: 2, sigmaHigh: 3, color: 'rgba(229, 57, 53, 0.12)', name: '2-3 Sigma' },
    { sigmaLow: 3, sigmaHigh: 4, color: 'rgba(255, 152, 0, 0.10)', name: '3-4 Sigma' },
    { sigmaLow: 4, sigmaHigh: 5, color: 'rgba(249, 168, 37, 0.08)', name: '4-5 Sigma' },
    { sigmaLow: 5, sigmaHigh: 6, color: 'rgba(102, 187, 106, 0.08)', name: '5-6 Sigma' },
    { sigmaLow: 6, sigmaHigh: null, color: 'rgba(67, 160, 71, 0.10)', name: '>= 6 Sigma' },
  ]

  // For each sigma boundary, draw a dashed line
  for (const sl of sigmaLines) {
    const xEnd = Math.min(cvMax, 1 / sl.sigma)
    shapes.push({
      type: 'line',
      x0: 0, y0: 1,
      x1: xEnd, y1: Math.max(0, 1 - sl.sigma * xEnd),
      line: { color: sl.color, width: 1.5, dash: 'dash' },
    })
    // Label at the end of the line
    annotations.push({
      x: xEnd,
      y: Math.max(0, 1 - sl.sigma * xEnd),
      text: sl.label,
      showarrow: false,
      font: { color: sl.color, size: 10 },
      xanchor: 'left',
      xshift: 4,
    })
  }

  // Data points
  const traces = []
  for (const assay of props.assays) {
    traces.push({
      x: [assay.cvTEa],
      y: [assay.biasTEa],
      mode: 'markers+text',
      type: 'scatter',
      marker: { color: sigmaColor(assay.sigma), size: 12, symbol: 'circle',
        line: { color: '#fff', width: 1 } },
      text: [assay.name],
      textposition: 'top center',
      textfont: { color: '#F3F4F6', size: 11 },
      name: `${assay.name} (${assay.sigma.toFixed(1)}σ)`,
      showlegend: true,
      hovertemplate: `<b>${assay.name}</b><br>CV/TEa: %{x:.3f}<br>Bias/TEa: %{y:.3f}<br>Sigma: ${assay.sigma.toFixed(1)}<extra></extra>`,
    })
  }

  const layout = {
    title: { text: props.title, font: { color: '#F3F4F6', size: 15 } },
    paper_bgcolor: '#12161B',
    plot_bgcolor: '#12161B',
    margin: { l: 60, r: 30, t: 50, b: 50 },
    height: props.height,
    xaxis: {
      title: { text: 'CV / TEa (Imprecision)', font: { color: '#8E97A3', size: 12 } },
      color: '#8E97A3', gridcolor: '#262D36', zerolinecolor: '#262D36',
      range: [0, cvMax],
    },
    yaxis: {
      title: { text: 'Bias / TEa (Inaccuracy)', font: { color: '#8E97A3', size: 12 } },
      color: '#8E97A3', gridcolor: '#262D36', zerolinecolor: '#262D36',
      range: [0, 1.0],
    },
    shapes,
    annotations,
    legend: {
      font: { color: '#8E97A3', size: 11 },
      bgcolor: 'rgba(18, 22, 27, 0.8)',
      bordercolor: '#262D36',
      borderwidth: 1,
    },
  }

  const config = { displayModeBar: false, responsive: true }

  Plotly.default.newPlot(chartEl.value, traces, layout, config)
}

onMounted(render)
watch(() => props.assays, render)
</script>

<template>
  <div ref="chartEl" class="plotly-nmedx-diagram"></div>
</template>

<style scoped>
.plotly-nmedx-diagram {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  border: 1px solid var(--border-subtle);
}
</style>

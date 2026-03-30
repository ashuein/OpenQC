<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps({
  results: {
    type: Array,
    required: true,
    default: () => [],
  },
})

const chartRef = ref(null)
let Plotly = null

const classColors = {
  'World Class': '#43A047',
  Excellent: '#66BB6A',
  Good: '#F9A825',
  Marginal: '#FB8C00',
  Poor: '#E53935',
}

function getPointColor(classification) {
  return classColors[classification] || '#8E97A3'
}

async function renderChart() {
  if (!chartRef.value || !props.results.length) return

  if (!Plotly) {
    Plotly = await import('plotly.js-dist-min')
  }

  const x = props.results.map((r) => r.nmedx_x)
  const y = props.results.map((r) => r.nmedx_y)
  const text = props.results.map((r) => r.assay)
  const colors = props.results.map((r) => getPointColor(r.classification))

  // Zone boundaries for sigma bands on NMEDx chart
  // NMEDx: x = |bias|/TEa, y = CV/TEa
  // Sigma = (TEa - |bias|) / CV = (1 - x) / y  when normalized
  // So sigma contours satisfy y = (1 - x) / sigma_level
  const zoneShapes = [
    // < 3 sigma zone (red) - full background
    {
      type: 'rect',
      x0: 0, x1: 1.2, y0: 0, y1: 0.8,
      fillcolor: 'rgba(229, 57, 53, 0.06)',
      line: { width: 0 },
      layer: 'below',
    },
    // 3-4 sigma zone (orange)
    {
      type: 'path',
      path: 'M 0,0 L 0,0.333 L 0.6667,0.111 L 1,0 Z',
      fillcolor: 'rgba(251, 140, 0, 0.08)',
      line: { width: 0 },
      layer: 'below',
    },
    // 4-5 sigma zone (yellow)
    {
      type: 'path',
      path: 'M 0,0 L 0,0.25 L 0.5,0.1 L 1,0 Z',
      fillcolor: 'rgba(249, 168, 37, 0.08)',
      line: { width: 0 },
      layer: 'below',
    },
    // 5-6 sigma zone (lighter green)
    {
      type: 'path',
      path: 'M 0,0 L 0,0.2 L 0.4,0.08 L 1,0 Z',
      fillcolor: 'rgba(102, 187, 106, 0.08)',
      line: { width: 0 },
      layer: 'below',
    },
    // >= 6 sigma zone (green)
    {
      type: 'path',
      path: 'M 0,0 L 0,0.1667 L 0.3333,0.0667 L 1,0 Z',
      fillcolor: 'rgba(67, 160, 71, 0.1)',
      line: { width: 0 },
      layer: 'below',
    },
  ]

  // Sigma contour lines
  const annotations = []
  const contourTraces = []
  const sigmaLevels = [3, 4, 5, 6]
  const contourColors = ['#E53935', '#FB8C00', '#F9A825', '#43A047']

  sigmaLevels.forEach((s, i) => {
    const xVals = []
    const yVals = []
    for (let xv = 0; xv <= 1.0; xv += 0.01) {
      const yv = (1 - xv) / s
      if (yv >= 0 && yv <= 0.8) {
        xVals.push(xv)
        yVals.push(yv)
      }
    }
    contourTraces.push({
      x: xVals,
      y: yVals,
      mode: 'lines',
      line: { color: contourColors[i], width: 1, dash: 'dot' },
      showlegend: false,
      hoverinfo: 'skip',
    })
    // Label at the y-axis
    if (yVals.length > 0) {
      annotations.push({
        x: 0.02,
        y: yVals[0],
        text: `${s}σ`,
        showarrow: false,
        font: { size: 10, color: contourColors[i] },
        xanchor: 'left',
      })
    }
  })

  const scatterTrace = {
    x,
    y,
    text,
    mode: 'markers+text',
    type: 'scatter',
    marker: {
      size: 10,
      color: colors,
      line: { width: 1, color: 'rgba(255,255,255,0.2)' },
    },
    textposition: 'top center',
    textfont: { size: 11, color: '#B6BDC7' },
    hovertemplate: '<b>%{text}</b><br>Bias/TEa: %{x:.3f}<br>CV/TEa: %{y:.3f}<extra></extra>',
    showlegend: false,
  }

  const layout = {
    paper_bgcolor: '#0B0D10',
    plot_bgcolor: '#12161B',
    margin: { l: 56, r: 24, t: 24, b: 48 },
    xaxis: {
      title: { text: '|Bias| / TEa', font: { size: 12, color: '#8E97A3' } },
      gridcolor: '#262D36',
      zerolinecolor: '#343D48',
      tickfont: { size: 11, color: '#8E97A3' },
      range: [0, Math.max(1, ...x) + 0.1],
    },
    yaxis: {
      title: { text: 'CV / TEa', font: { size: 12, color: '#8E97A3' } },
      gridcolor: '#262D36',
      zerolinecolor: '#343D48',
      tickfont: { size: 11, color: '#8E97A3' },
      range: [0, Math.max(0.5, ...y) + 0.05],
    },
    shapes: zoneShapes,
    annotations,
    font: { family: 'Inter, system-ui, sans-serif' },
  }

  const config = {
    displayModeBar: false,
    responsive: true,
  }

  await Plotly.default.newPlot(chartRef.value, [...contourTraces, scatterTrace], layout, config)
}

onMounted(() => {
  if (props.results.length) {
    nextTick(renderChart)
  }
})

watch(
  () => props.results,
  () => {
    nextTick(renderChart)
  },
  { deep: true }
)

onBeforeUnmount(() => {
  if (chartRef.value && Plotly) {
    Plotly.default.purge(chartRef.value)
  }
})
</script>

<template>
  <div class="nmedx-chart">
    <div class="nmedx-chart__header">
      <span class="nmedx-chart__title">Normalized Method Decision Chart</span>
    </div>
    <div ref="chartRef" class="nmedx-chart__plot"></div>
  </div>
</template>

<style scoped>
.nmedx-chart {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.nmedx-chart__header {
  margin-bottom: 12px;
}

.nmedx-chart__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.nmedx-chart__plot {
  width: 100%;
  min-height: 380px;
}
</style>

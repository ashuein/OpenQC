<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
  points: { type: Array, required: true }, // [{x: runNum, y: value, color: 'normal'|'warning'|'reject'}]
  mean: { type: Number, default: 0 },
  sd: { type: Number, default: 1 },
  height: { type: Number, default: 320 },
  annotation: { type: String, default: '' },
})

const chartEl = ref(null)

async function render() {
  const Plotly = await import('plotly.js-dist-min')

  const normalPts = props.points.filter(p => p.color === 'normal')
  const warningPts = props.points.filter(p => p.color === 'warning')
  const rejectPts = props.points.filter(p => p.color === 'reject')

  const m = props.mean
  const s = props.sd

  // Build a single connected line through ALL points in x-order
  const sorted = [...props.points].sort((a, b) => a.x - b.x)

  const traces = []

  // Connecting line (all points, no markers)
  traces.push({
    x: sorted.map(p => p.x),
    y: sorted.map(p => p.y),
    mode: 'lines',
    type: 'scatter',
    line: { color: '#B6BDC7', width: 1, dash: 'dot' },
    showlegend: false,
    hoverinfo: 'skip',
  })

  if (normalPts.length) {
    traces.push({
      x: normalPts.map(p => p.x),
      y: normalPts.map(p => p.y),
      mode: 'markers',
      type: 'scatter',
      marker: { color: '#B6BDC7', size: 8 },
      name: 'Normal',
      showlegend: false,
    })
  }
  if (warningPts.length) {
    traces.push({
      x: warningPts.map(p => p.x),
      y: warningPts.map(p => p.y),
      mode: 'markers',
      type: 'scatter',
      marker: { color: '#F9A825', size: 10, symbol: 'circle' },
      name: 'Warning',
      showlegend: false,
    })
  }
  if (rejectPts.length) {
    traces.push({
      x: rejectPts.map(p => p.x),
      y: rejectPts.map(p => p.y),
      mode: 'markers',
      type: 'scatter',
      marker: { color: '#E53935', size: 12, symbol: 'diamond' },
      name: 'Reject',
      showlegend: false,
    })
  }

  // Reference lines as shapes
  const shapes = [
    { type: 'line', y0: m, y1: m, x0: 0, x1: 1, xref: 'paper', line: { color: '#43A047', width: 2 }, name: 'Mean' },
    { type: 'line', y0: m + s, y1: m + s, x0: 0, x1: 1, xref: 'paper', line: { color: '#8E97A3', width: 1, dash: 'dot' } },
    { type: 'line', y0: m - s, y1: m - s, x0: 0, x1: 1, xref: 'paper', line: { color: '#8E97A3', width: 1, dash: 'dot' } },
    { type: 'line', y0: m + 2 * s, y1: m + 2 * s, x0: 0, x1: 1, xref: 'paper', line: { color: '#F9A825', width: 1, dash: 'dash' } },
    { type: 'line', y0: m - 2 * s, y1: m - 2 * s, x0: 0, x1: 1, xref: 'paper', line: { color: '#F9A825', width: 1, dash: 'dash' } },
    { type: 'line', y0: m + 3 * s, y1: m + 3 * s, x0: 0, x1: 1, xref: 'paper', line: { color: '#E53935', width: 1, dash: 'dash' } },
    { type: 'line', y0: m - 3 * s, y1: m - 3 * s, x0: 0, x1: 1, xref: 'paper', line: { color: '#E53935', width: 1, dash: 'dash' } },
  ]

  // Y-axis annotations for SD lines
  const annotations = [
    { x: -0.02, y: m, text: 'Mean', xref: 'paper', showarrow: false, font: { color: '#43A047', size: 11 } },
    { x: -0.02, y: m + 2 * s, text: '+2SD', xref: 'paper', showarrow: false, font: { color: '#F9A825', size: 10 } },
    { x: -0.02, y: m - 2 * s, text: '-2SD', xref: 'paper', showarrow: false, font: { color: '#F9A825', size: 10 } },
    { x: -0.02, y: m + 3 * s, text: '+3SD', xref: 'paper', showarrow: false, font: { color: '#E53935', size: 10 } },
    { x: -0.02, y: m - 3 * s, text: '-3SD', xref: 'paper', showarrow: false, font: { color: '#E53935', size: 10 } },
  ]

  if (props.annotation) {
    annotations.push({
      x: 0.5, y: 1.08, text: props.annotation, xref: 'paper', yref: 'paper',
      showarrow: false, font: { color: '#F9A825', size: 12 },
    })
  }

  const layout = {
    title: { text: props.title, font: { color: '#F3F4F6', size: 15 } },
    paper_bgcolor: '#12161B',
    plot_bgcolor: '#12161B',
    margin: { l: 55, r: 20, t: 50, b: 40 },
    height: props.height,
    xaxis: {
      title: { text: 'Run Number', font: { color: '#8E97A3', size: 12 } },
      color: '#8E97A3', gridcolor: '#262D36', zerolinecolor: '#262D36',
    },
    yaxis: {
      title: { text: 'QC Value', font: { color: '#8E97A3', size: 12 } },
      color: '#8E97A3', gridcolor: '#262D36', zerolinecolor: '#262D36',
      range: [m - 4 * s, m + 4 * s],
    },
    shapes,
    annotations,
  }

  const config = { displayModeBar: false, responsive: true }

  Plotly.default.newPlot(chartEl.value, traces, layout, config)
}

onMounted(render)
watch(() => props.points, render)
</script>

<template>
  <div ref="chartEl" class="plotly-lj-diagram"></div>
</template>

<style scoped>
.plotly-lj-diagram {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  border: 1px solid var(--border-subtle);
}
</style>

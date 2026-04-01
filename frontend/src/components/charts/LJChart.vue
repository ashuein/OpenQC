<script setup>
import { computed, ref, watchEffect } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { ScatterChart, LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  MarkLineComponent,
  MarkAreaComponent,
  LegendComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer,
  ScatterChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  MarkLineComponent,
  MarkAreaComponent,
  LegendComponent,
])

const props = defineProps({
  dataPoints: { type: Array, required: true },
  mean: { type: Number, required: true },
  sd: { type: Number, required: true },
})

function fmt(v) {
  if (v == null) return 'N/A'
  return Number.isInteger(v) ? String(v) : v.toFixed(2)
}

const option = computed(() => {
  const m = props.mean
  const s = props.sd

  const rejectRules = new Set(['1-3s', '2-2s', 'R-4s', '4-1s', '10x'])
  const normalPoints = []
  const warningPoints = []
  const rejectPoints = []

  for (const pt of props.dataPoints) {
    const entry = [pt.cycle ?? pt.sequence_index, pt.ct_value]
    if (pt.violations && pt.violations.length > 0) {
      const hasReject = pt.violations.some(v => rejectRules.has(v))
      if (hasReject) { rejectPoints.push(entry) }
      else { warningPoints.push(entry) }
    } else {
      normalPoints.push(entry)
    }
  }

  return {
    backgroundColor: '#FFFFFF',
    grid: { left: 120, right: 40, top: 40, bottom: 50 },
    tooltip: {
      trigger: 'item',
      backgroundColor: '#fff',
      borderColor: '#ddd',
      textStyle: { color: '#333', fontSize: 13, fontWeight: 500 },
      formatter(params) {
        const d = props.dataPoints.find(p => (p.cycle ?? p.sequence_index) === params.value[0])
        if (!d) return ''
        let html = `<strong style="color:#111">Point ${d.cycle ?? d.sequence_index}</strong><br/>`
        html += `Value: <b>${fmt(d.ct_value)}</b><br/>`
        html += `Z-Score: <b>${fmt(d.z_score)}</b><br/>`
        if (d.control_level) html += `Level: ${d.control_level}<br/>`
        if (d.violations && d.violations.length > 0) {
          html += `<span style="color:#E53935">Rules: ${d.violations.join(', ')}</span>`
        }
        return html
      },
    },
    xAxis: {
      type: 'value',
      name: 'Run #',
      nameTextStyle: { color: '#555', fontSize: 13, fontWeight: 'bold' },
      axisLine: { lineStyle: { color: '#999' } },
      axisTick: { lineStyle: { color: '#bbb' } },
      axisLabel: { color: '#444', fontSize: 12, fontWeight: 'bold' },
      splitLine: { show: false },
      min: (value) => Math.max(0, value.min - 1),
      max: (value) => value.max + 1,
    },
    yAxis: {
      type: 'value',
      name: 'QC Value',
      nameTextStyle: { color: '#555', fontSize: 13, fontWeight: 'bold' },
      axisLine: { lineStyle: { color: '#999' } },
      axisTick: { lineStyle: { color: '#bbb' } },
      axisLabel: {
        color: '#444',
        fontSize: 12,
        fontWeight: 'bold',
        formatter: (v) => fmt(v),
      },
      splitLine: { lineStyle: { color: '#e0e0e0', type: 'dashed' } },
      min: m - 4 * s,
      max: m + 4 * s,
    },
    series: [
      {
        name: 'Normal',
        type: 'scatter',
        data: normalPoints,
        symbolSize: 9,
        itemStyle: { color: '#1976D2' },
        z: 3,
      },
      {
        name: 'Warning',
        type: 'scatter',
        data: warningPoints,
        symbolSize: 11,
        itemStyle: { color: '#F9A825' },
        z: 4,
      },
      {
        name: 'Reject',
        type: 'scatter',
        data: rejectPoints,
        symbolSize: 12,
        symbol: 'diamond',
        itemStyle: { color: '#E53935' },
        z: 5,
      },
      {
        name: 'Reference',
        type: 'line',
        data: [],
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { type: 'solid', width: 1.5 },
          label: { position: 'start', fontSize: 12, fontWeight: 'bold' },
          data: [
            { yAxis: m, label: { formatter: `Mean (${fmt(m)})`, color: '#2E7D32' }, lineStyle: { color: '#43A047', width: 2 } },
            { yAxis: m + s, label: { formatter: `+1SD (${fmt(m+s)})`, color: '#888' }, lineStyle: { color: '#bbb', type: 'dotted' } },
            { yAxis: m - s, label: { formatter: `-1SD (${fmt(m-s)})`, color: '#888' }, lineStyle: { color: '#bbb', type: 'dotted' } },
            { yAxis: m + 2*s, label: { formatter: `+2SD (${fmt(m+2*s)})`, color: '#E65100' }, lineStyle: { color: '#F9A825', width: 1.5, type: 'dashed' } },
            { yAxis: m - 2*s, label: { formatter: `-2SD (${fmt(m-2*s)})`, color: '#E65100' }, lineStyle: { color: '#F9A825', width: 1.5, type: 'dashed' } },
            { yAxis: m + 3*s, label: { formatter: `+3SD (${fmt(m+3*s)})`, color: '#C62828' }, lineStyle: { color: '#E53935', width: 1.5, type: 'dashed' } },
            { yAxis: m - 3*s, label: { formatter: `-3SD (${fmt(m-3*s)})`, color: '#C62828' }, lineStyle: { color: '#E53935', width: 1.5, type: 'dashed' } },
          ],
        },
        markArea: {
          silent: true,
          data: [
            [{ yAxis: m - s, itemStyle: { color: 'rgba(67, 160, 71, 0.08)' } }, { yAxis: m + s }],
            [{ yAxis: m - 2*s, itemStyle: { color: 'rgba(249, 168, 37, 0.06)' } }, { yAxis: m - s }],
            [{ yAxis: m + s, itemStyle: { color: 'rgba(249, 168, 37, 0.06)' } }, { yAxis: m + 2*s }],
            [{ yAxis: m - 3*s, itemStyle: { color: 'rgba(229, 57, 53, 0.06)' } }, { yAxis: m - 2*s }],
            [{ yAxis: m + 2*s, itemStyle: { color: 'rgba(229, 57, 53, 0.06)' } }, { yAxis: m + 3*s }],
          ],
        },
      },
    ],
  }
})
</script>

<template>
  <div class="lj-chart">
    <VChart :option="option" :autoresize="true" class="lj-chart__canvas" />
  </div>
</template>

<style scoped>
.lj-chart {
  width: 100%;
  display: flex;
  justify-content: center;
  border-radius: 8px;
  overflow: hidden;
  background: #FFFFFF;
}

.lj-chart__canvas {
  width: 100%;
  max-width: 900px;
  height: 520px;
}
</style>

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
  dataPoints: {
    type: Array,
    required: true,
  },
  mean: {
    type: Number,
    required: true,
  },
  sd: {
    type: Number,
    required: true,
  },
})

const chartRef = ref(null)

const option = computed(() => {
  const m = props.mean
  const s = props.sd

  const normalPoints = []
  const warningPoints = []
  const rejectPoints = []

  // Reject-level rules per the Westgard spec; 1-2s is warning-only
  const rejectRules = new Set(['1-3s', '2-2s', 'R-4s', '4-1s', '10x'])

  for (const pt of props.dataPoints) {
    const entry = [pt.cycle ?? pt.sequence_index, pt.ct_value]
    if (pt.violations && pt.violations.length > 0) {
      const hasReject = pt.violations.some(v => rejectRules.has(v))
      if (hasReject) {
        rejectPoints.push(entry)
      } else {
        warningPoints.push(entry)
      }
    } else {
      normalPoints.push(entry)
    }
  }

  const cssVar = (name) => {
    if (typeof document !== 'undefined') {
      return getComputedStyle(document.documentElement).getPropertyValue(name).trim()
    }
    return ''
  }

  const textMuted = cssVar('--text-muted') || '#8E97A3'
  const textSecondary = cssVar('--text-secondary') || '#B6BDC7'
  const borderSubtle = cssVar('--border-subtle') || '#262D36'
  const bgSurface = cssVar('--bg-surface') || '#12161B'
  const colorWarning = cssVar('--color-warning') || '#F9A825'
  const colorDanger = cssVar('--color-danger') || '#E53935'
  const colorSuccess = cssVar('--color-success') || '#43A047'

  return {
    backgroundColor: 'transparent',
    grid: {
      left: 60,
      right: 24,
      top: 32,
      bottom: 40,
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: bgSurface,
      borderColor: borderSubtle,
      textStyle: { color: textSecondary, fontSize: 12 },
      formatter(params) {
        const d = props.dataPoints.find(
          p => p.sequence_index === params.value[0]
        )
        if (!d) return ''
        let html = `<strong>Point ${d.sequence_index}</strong><br/>`
        html += `Ct: ${d.ct_value.toFixed(2)}<br/>`
        html += `Z-Score: ${d.z_score?.toFixed(2) ?? 'N/A'}<br/>`
        if (d.control_level) html += `Level: ${d.control_level}<br/>`
        if (d.violations && d.violations.length > 0) {
          html += `Rules: ${d.violations.join(', ')}`
        }
        return html
      },
    },
    xAxis: {
      type: 'value',
      name: 'Run #',
      nameTextStyle: { color: textMuted, fontSize: 11 },
      axisLine: { lineStyle: { color: borderSubtle } },
      axisTick: { lineStyle: { color: borderSubtle } },
      axisLabel: { color: textMuted, fontSize: 11 },
      splitLine: { show: false },
      min: (value) => Math.max(1, value.min - 1),
      max: (value) => value.max + 1,
    },
    yAxis: {
      type: 'value',
      name: 'Ct Value',
      nameTextStyle: { color: textMuted, fontSize: 11 },
      axisLine: { lineStyle: { color: borderSubtle } },
      axisTick: { lineStyle: { color: borderSubtle } },
      axisLabel: { color: textMuted, fontSize: 11 },
      splitLine: { lineStyle: { color: borderSubtle, type: 'dashed', opacity: 0.4 } },
      min: m - 4 * s,
      max: m + 4 * s,
    },
    series: [
      {
        name: 'Normal',
        type: 'scatter',
        data: normalPoints,
        symbolSize: 8,
        itemStyle: { color: textSecondary },
        z: 3,
      },
      {
        name: 'Warning',
        type: 'scatter',
        data: warningPoints,
        symbolSize: 10,
        itemStyle: { color: colorWarning },
        z: 4,
      },
      {
        name: 'Reject',
        type: 'scatter',
        data: rejectPoints,
        symbolSize: 10,
        symbol: 'diamond',
        itemStyle: { color: colorDanger },
        z: 5,
      },
      {
        name: 'Reference',
        type: 'line',
        data: [],
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { type: 'solid', width: 1 },
          label: {
            position: 'start',
            fontSize: 10,
            color: textMuted,
          },
          data: [
            { yAxis: m, label: { formatter: 'Mean' }, lineStyle: { color: colorSuccess, opacity: 0.6 } },
            { yAxis: m + s, label: { formatter: '+1SD' }, lineStyle: { color: textMuted, opacity: 0.4 } },
            { yAxis: m - s, label: { formatter: '-1SD' }, lineStyle: { color: textMuted, opacity: 0.4 } },
            { yAxis: m + 2 * s, label: { formatter: '+2SD' }, lineStyle: { color: colorWarning, opacity: 0.5 } },
            { yAxis: m - 2 * s, label: { formatter: '-2SD' }, lineStyle: { color: colorWarning, opacity: 0.5 } },
            { yAxis: m + 3 * s, label: { formatter: '+3SD' }, lineStyle: { color: colorDanger, opacity: 0.5 } },
            { yAxis: m - 3 * s, label: { formatter: '-3SD' }, lineStyle: { color: colorDanger, opacity: 0.5 } },
          ],
        },
        markArea: {
          silent: true,
          data: [
            [
              { yAxis: m - s, itemStyle: { color: 'rgba(67, 160, 71, 0.04)' } },
              { yAxis: m + s },
            ],
            [
              { yAxis: m - 2 * s, itemStyle: { color: 'rgba(249, 168, 37, 0.03)' } },
              { yAxis: m - s },
            ],
            [
              { yAxis: m + s, itemStyle: { color: 'rgba(249, 168, 37, 0.03)' } },
              { yAxis: m + 2 * s },
            ],
            [
              { yAxis: m - 3 * s, itemStyle: { color: 'rgba(229, 57, 53, 0.03)' } },
              { yAxis: m - 2 * s },
            ],
            [
              { yAxis: m + 2 * s, itemStyle: { color: 'rgba(229, 57, 53, 0.03)' } },
              { yAxis: m + 3 * s },
            ],
          ],
        },
      },
    ],
  }
})
</script>

<template>
  <div class="lj-chart">
    <VChart
      ref="chartRef"
      :option="option"
      :autoresize="true"
      class="lj-chart__canvas"
    />
  </div>
</template>

<style scoped>
.lj-chart {
  width: 100%;
  min-height: 340px;
}

.lj-chart__canvas {
  width: 100%;
  height: 340px;
}
</style>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

const props = defineProps({
  levels: {
    type: Array,
    required: true,
    default: () => [],
  },
  regression: {
    type: Object,
    default: () => ({ slope: 1, intercept: 0, r_squared: 0 }),
  },
})

const chartRef = ref(null)
let echarts = null
let chartInstance = null

async function renderChart() {
  if (!chartRef.value || !props.levels.length) return

  if (!echarts) {
    echarts = await import('echarts/core')
    const { ScatterChart, LineChart } = await import('echarts/charts')
    const {
      GridComponent,
      TooltipComponent,
      LegendComponent,
      GraphicComponent,
    } = await import('echarts/components')
    const { CanvasRenderer } = await import('echarts/renderers')
    echarts.use([
      ScatterChart,
      LineChart,
      GridComponent,
      TooltipComponent,
      LegendComponent,
      GraphicComponent,
      CanvasRenderer,
    ])
  }

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const scatterData = props.levels.map((l) => [l.expected, l.measured])

  // Compute regression line endpoints
  const xValues = props.levels.map((l) => l.expected)
  const xMin = Math.min(...xValues)
  const xMax = Math.max(...xValues)
  const { slope, intercept, r_squared } = props.regression
  const regressionData = [
    [xMin, slope * xMin + intercept],
    [xMax, slope * xMax + intercept],
  ]

  const option = {
    backgroundColor: 'transparent',
    grid: {
      left: 56,
      right: 24,
      top: 40,
      bottom: 48,
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: '#171C22',
      borderColor: '#262D36',
      textStyle: { color: '#F3F4F6', fontSize: 12 },
      formatter: (params) => {
        if (params.seriesType === 'scatter') {
          return `Expected: ${params.value[0]}<br/>Measured: ${params.value[1]}`
        }
        return ''
      },
    },
    xAxis: {
      type: 'value',
      name: 'Expected',
      nameTextStyle: { color: '#8E97A3', fontSize: 12 },
      axisLine: { lineStyle: { color: '#343D48' } },
      axisTick: { lineStyle: { color: '#343D48' } },
      axisLabel: { color: '#8E97A3', fontSize: 11 },
      splitLine: { lineStyle: { color: '#262D36' } },
    },
    yAxis: {
      type: 'value',
      name: 'Measured',
      nameTextStyle: { color: '#8E97A3', fontSize: 12 },
      axisLine: { lineStyle: { color: '#343D48' } },
      axisTick: { lineStyle: { color: '#343D48' } },
      axisLabel: { color: '#8E97A3', fontSize: 11 },
      splitLine: { lineStyle: { color: '#262D36' } },
    },
    series: [
      {
        name: 'Measurements',
        type: 'scatter',
        data: scatterData,
        symbolSize: 8,
        itemStyle: { color: '#B6BDC7' },
      },
      {
        name: 'Regression',
        type: 'line',
        data: regressionData,
        smooth: false,
        showSymbol: false,
        lineStyle: { color: '#43A047', width: 2 },
        itemStyle: { color: '#43A047' },
      },
    ],
    graphic: [
      {
        type: 'text',
        right: 24,
        top: 12,
        style: {
          text: [
            `R\u00B2 = ${r_squared.toFixed(4)}`,
            `Slope = ${slope.toFixed(4)}`,
            `Intercept = ${intercept.toFixed(4)}`,
          ].join('  |  '),
          fill: '#8E97A3',
          fontSize: 11,
          fontFamily: "'SF Mono', 'Cascadia Code', 'Fira Code', monospace",
        },
      },
    ],
  }

  chartInstance.setOption(option)
}

function handleResize() {
  chartInstance?.resize()
}

onMounted(() => {
  if (props.levels.length) {
    nextTick(renderChart)
  }
  window.addEventListener('resize', handleResize)
})

watch(
  () => [props.levels, props.regression],
  () => nextTick(renderChart),
  { deep: true }
)

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
  chartInstance = null
})
</script>

<template>
  <div class="linearity-chart">
    <div class="linearity-chart__header">
      <span class="linearity-chart__title">Linearity Regression</span>
    </div>
    <div ref="chartRef" class="linearity-chart__plot"></div>
  </div>
</template>

<style scoped>
.linearity-chart {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.linearity-chart__header {
  margin-bottom: 12px;
}

.linearity-chart__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.linearity-chart__plot {
  width: 100%;
  height: 360px;
}
</style>

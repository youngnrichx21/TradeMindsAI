document.addEventListener("DOMContentLoaded", () => {
  window.activeChart   = null;
  window.activeSeries  = null;
  window.preTrend      = [];
  window.trendSegment  = [];
  window.playbackIndex = 0;
  window.lastCandle    = null;

  function destroyChart() {
    if (window.activeChart) {
      window.activeChart.remove();
      window.activeChart = null;
      document.getElementById("chart").innerHTML = "";
    }
  }

  function initChart(data) {
    const c = document.getElementById("chart");
    window.activeChart  = LightweightCharts.createChart(c, {
      width:900,
      height:500,
      timeScale: {
        fixLeftEdge: true,
      },
    });
    window.activeSeries = window.activeChart.addCandlestickSeries();
    window.activeSeries.setData(data);
    if (data.length) window.lastCandle = data[data.length-1];
  }

  window.loadPuzzle = (pre, trend) => {
    destroyChart();
    window.preTrend      = pre;
    window.trendSegment  = trend;
    window.playbackIndex = 0;
    initChart(pre);
  };

  window.updateChart = () => {
    const full = window.preTrend.concat(window.trendSegment.slice(0, window.playbackIndex));
    window.activeSeries.setData(full);
    if (full.length) window.lastCandle = full[full.length-1];
  };
});

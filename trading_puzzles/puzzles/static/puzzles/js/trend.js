document.addEventListener("DOMContentLoaded", () => {
  const trendSel = $("#trend-select"),
        coinSel  = $("#coin-select"),
        spinner  = document.getElementById("chart-spinner");
  let interval = null;

  async function fetchPuzzle(symbol, trend) {
    const url  = `/puzzles/api/get_trend_puzzle/?symbol=${symbol}&trend=${trend}`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return resp.json();
  }

  async function loadChart(symbol, trend) {
    spinner.style.display = "block";
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
    try {
      const data = await fetchPuzzle(symbol, trend);
      window.loadPuzzle(data.pre_trend, data.trend);
    } catch(err) {
      console.error("Chart load error:", err);
    } finally {
      spinner.style.display = "none";
    }
  }

  function playback(ms) {
    if (interval) {
      clearInterval(interval);
    }
    interval = setInterval(() => {
      if (window.playbackIndex < window.trendSegment.length) {
        window.playbackIndex++;
        window.updateChart();
      } else {
        clearInterval(interval);
        interval = null;
        window.evaluateTrades(window.lastCandle.close);
      }
    }, ms);
  }

  $("#next-puzzle-btn").click(() => loadChart(coinSel.val(), trendSel.val()));
  coinSel.change(() => {
    resetPortfolio();
    loadChart(coinSel.val(), trendSel.val());
  });
  trendSel.change(() => loadChart(coinSel.val(), trendSel.val()));
  $("#play-btn").click(() => playback(500));
  $("#fast-btn").click(() => playback(100));

  // initial load
  loadChart(coinSel.val(), trendSel.val());
});

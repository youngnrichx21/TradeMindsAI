document.addEventListener("DOMContentLoaded", () => {
  const trendSel = $("#trend-select"),
        coinSel  = $("#coin-select"),
        playPauseBtn = $("#play-pause-btn"),
        speedSel = $("#speed-select"),
        spinner  = document.getElementById("chart-spinner");
  let interval = null,
      isPlaying = false;

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
    isPlaying = false;
    playPauseBtn.text("Play");
    try {
      const data = await fetchPuzzle(symbol, trend);
      window.loadPuzzle(data.pre_trend, data.trend);
    } catch(err) {
      console.error("Chart load error:", err);
    } finally {
      spinner.style.display = "none";
    }
  }

  function playback() {
    if (interval) clearInterval(interval);

    const speed = parseFloat(speedSel.val()) || 1;
    const ms = 100 / speed;

    interval = setInterval(() => {
      if (window.playbackIndex < window.trendSegment.length) {
        window.playbackIndex++;
        window.updateChart();

        if (window.playbackIndex >= window.trendSegment.length) {
          window.evaluateTrades(window.lastCandle.close);
        }
      }
    }, ms);
  }

  function togglePlayback() {
    isPlaying = !isPlaying;
    if (isPlaying) {
      playback();
      playPauseBtn.text("Pause");
    } else {
      clearInterval(interval);
      interval = null;
      playPauseBtn.text("Play");
    }
  }

  $("#next-puzzle-btn").click(() => loadChart(coinSel.val(), trendSel.val()));
  coinSel.change(() => {
    resetPortfolio();
    loadChart(coinSel.val(), trendSel.val());
  });
  trendSel.change(() => loadChart(coinSel.val(), trendSel.val()));
  playPauseBtn.click(togglePlayback);
  speedSel.change(() => {
    if (isPlaying) playback(); // Restart playback with new speed
  });

  // initial load
  loadChart(coinSel.val(), trendSel.val());
});

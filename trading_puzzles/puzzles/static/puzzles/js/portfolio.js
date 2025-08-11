let portfolio = { balance: 1000000, open: [], closed: [], nextId: 1 };

function updateBalance() {
  $("#balance").text(portfolio.balance.toFixed(2));
}

function resetPortfolio() {
  portfolio = { balance:1000000, open:[], closed:[], nextId:1 };
  $("#open-table tbody, #closed-table tbody").empty();
  updateBalance();
  $("#trade-msg").text("Portfolio reset");
}

function showMsg(msg) {
  $("#trade-msg").text(msg);
  setTimeout(() => $("#trade-msg").text(""), 3000);
}

$("#trade-submit").click(() => {
  const type = $("#trade-type").val(),
        qty  = parseFloat($("#trade-qty").val()),
        sl   = parseFloat($("#trade-sl").val()) || null,
        tp   = parseFloat($("#trade-tp").val()) || null,
        entry = window.lastCandle?.close || 0;
  if (!entry || qty <= 0) return showMsg("Invalid trade details.");
  if (type==="buy" && entry*qty > portfolio.balance) return showMsg("Insufficient balance.");

  portfolio.balance += type==="sell" ? entry*qty : -entry*qty;
  updateBalance();

  const t = { id:portfolio.nextId++, type, qty, entry, sl, tp };
  portfolio.open.push(t);

  $("#open-table tbody").append(`
    <tr data-id="${t.id}">
      <td>${t.id}</td><td>${t.type}</td><td>${t.qty}</td>
      <td>${t.entry.toFixed(2)}</td><td>${t.sl||"-"}</td><td>${t.tp||"-"}</td>
      <td class="pnl">0.00</td>
    </tr>
  `);
  showMsg(`Trade ${t.id} placed @${t.entry.toFixed(2)}`);
});

window.evaluateTrades = finalPrice => {
  portfolio.open.forEach(t => {
    const pnl = ((t.type==="buy"
      ? finalPrice - t.entry
      : t.entry - finalPrice) * t.qty
    );
    const success = t.tp!=null && (
      t.type==="buy"  ? finalPrice>=t.tp
                      : finalPrice<=t.tp
    );
    $("#open-table tr[data-id="+t.id+"]").remove();
    $("#closed-table tbody").append(`
      <tr>
        <td>${t.id}</td><td>${t.type}</td><td>${t.qty}</td>
        <td>${t.entry.toFixed(2)}</td><td>${finalPrice.toFixed(2)}</td>
        <td>${success?"Won":"Failed"}</td><td>${pnl.toFixed(2)}</td>
      </tr>
    `);
    portfolio.balance += pnl;
    showMsg(success ? `✅ Trade ${t.id} won` : `❌ Trade ${t.id} failed`);
  });
  portfolio.open = [];
  updateBalance();
};

updateBalance();

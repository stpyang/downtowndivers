var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
  };

  function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
      return entityMap[s];
    });
  }

function addRow(blender, bill_to, escaped_tank_code, tank_factor, gas, psi_start, psi_end) {
  var gas_cost = Number(gas_info[gas].cost)
  var gas_name = gas_info[gas].name
  var psi_start = psi_start.toFixed(0)
  var psi_end = psi_end.toFixed(0)
  var psi = psi_end - psi_start
  var price = tank_factor * psi / 100.0 * (gas_cost + equipment_cost)

  var newrow = $("<tr>", {id: "fill"}).append(
    $("<td>").text(blender),
    $("<td>").text(bill_to),
    $("<td>").text(escaped_tank_code),
    $("<td>").text(gas_name),
    $("<td>").text(psi_start),
    $("<td>").text(psi_end),
    $("<td class='total_price'>").text(price.toFixed(2)),
    $("<td>").append(
      $("<button>", {id: "remove-fill-button", class: "btn btn-danger"})
        .html("<i class='glyphicons glyphicons-bin'></i>&nbsp;Delete")
      )
    )
  $("#tbody").append(newrow)
}

function addFill() {
  $("#tank-danger-message").addClass("hidden")
  $("#tank-danger-list").empty()

  var blender = $("#id_blender option:selected").val()
  var bill_to = $("#id_bill_to option:selected").val()
  var code = $("#id_tank option:selected").html() // tank_code or doubles_code
  var gas = $("#id_gas option:selected").val()
  var psi_start = $("#id_psi_start").val()
  var psi_end = $("#id_psi_end").val()

  code = escapeHtml(code)
  psi_start = Number(psi_start)
  psi_end = Number(psi_end)

  // TODO(stpyang): how do I move this validation to python or html5?
  if (psi_start < 0 || psi_end > 4000 || psi_start >= psi_end) {
    return false
  }

  tank_info[code].forEach(function(tank) {
    var tank_code = tank["tank_code"]
    var tank_factor = tank["tank_factor"]

    tank_code = escapeHtml(tank_code)

    addRow(blender, bill_to, tank_code, tank_factor, gas, psi_start, psi_end)

    if (!tank["is_current_hydro"]) {
      $("#tank-danger-list").append(
        $("<li>").html("<p>Tank `" + tank_code + "` does not have current hydro data!</p>")
      )
      $("#tank-danger-message").removeClass("hidden")
    }
    if (!tank["is_current_vip"]) {
      $("#tank-danger-list").append(
        $("<li>").html("<p>Tank `" + tank_code + "` does not have current vip data!</p>")
      )
      $("#tank-danger-message").removeClass("hidden")
    }
  })

  var i = $("#tbody tr").size()
  if (i == 0) {
    $("#thead").empty()
  } else if (i == 1) {
    if ($("#thead").is(":empty")) {
      $("#thead").append(
        $("<tr>", {id: "fill"}).append(
          $("<td>").text("Blender"),
          $("<td>").text("Bill To"),
          $("<td>").text("Tank"),
          $("<td>").text("Gas"),
          $("<td>").text("Psi Start"),
          $("<td>").text("Psi End"),
          $("<td>").text("Price")
        )
      )
    }
  }

  if (!($("#tank-danger-message").hasClass("hidden"))) {
    $("#myModal").modal("toggle")
  }
}

function updateFillForm(is_blend) {
  var num_rows = $("#tbody tr").size()

  var form = $("#log-fills-form")
  form.find("[class=hidden]").closest("input").remove()
  form.append($("<input>", { name: "num_rows", class: "hidden" }).attr("value", num_rows))

  $("#tbody").find("tr").each(function(i, val) {
    var $tds = $(this).find("td")
    form.append($("<input>", { name: "blender_" + i, class: "hidden"}).attr("value", $tds.eq(0).text()))
    form.append($("<input>", { name: "bill_to_" + i, class: "hidden"}).attr("value", $tds.eq(1).text()))
    form.append($("<input>", { name: "tank_code_" + i, class: "hidden"}).attr("value", $tds.eq(2).text()))
    form.append($("<input>", { name: "gas_name_" + i, class: "hidden"}).attr("value", $tds.eq(3).text()))
    form.append($("<input>", { name: "psi_start_" + i, class: "hidden"}).attr("value", $tds.eq(4).text()))
    form.append($("<input>", { name: "psi_end_" + i, class: "hidden"}).attr("value", $tds.eq(5).text()))
    form.append($("<input>", { name: "total_price_" + i, class: "hidden"}).attr("value", $tds.eq(6).text()))
    form.append($("<input>", { name: "is_blend_" + i, class: "hidden"}).attr("value", is_blend))
  })
}

function updateFillButton() {
  var i = $("#tbody tr").size()
  var array = $("tbody").find("[class=total_price]").map(function(i, x) {
      return Number(x.innerHTML)
    }).toArray()
  var total_price = 0
  if (array.length) {
    total_price = array.reduce(function(x, y) {
      return x + y
    })
  }
  if (i == 0) {
    $("#log-fills-button").addClass("hidden")
    $("#log-fills-button-text").empty()
  } else if (i == 1) {
    $("#log-fills-button").removeClass("hidden")
    $("#log-fills-button-text").text("Log Fill ($" + total_price.toFixed(2) + ")")
  } else if (i > 1) {
    $("#log-fills-button").removeClass("hidden")
    $("#log-fills-button-text").text("Log Fills ($" + total_price.toFixed(2) + ")")
  }
}

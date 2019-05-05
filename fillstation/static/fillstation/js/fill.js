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

function addRowGas(blender, bill_to, doubles_code, tank_code, tank_factor, gas, psi_start, psi_end) {
  var gas_cost = Number(gas_info[gas].cost)
  var gas_name = gas_info[gas].name
  var psi_start = psi_start.toFixed(0)
  var psi_end = psi_end.toFixed(0)
  var psi = psi_end - psi_start
  var price = tank_factor * psi / 100.0 * (gas_cost)

  var newrow = $("<tr>", {id: "fill"}).append(
    $("<td>").text(blender),
    $("<td>").text(bill_to),
    $("<td>").text(doubles_code),
    $("<td>").text(tank_code),
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

function addRowEquipmentSurcharge(blender, bill_to, doubles_code, price) {
  var newrow = $("<tr>", {id: "fill"}).append(
    $("<td>").text(blender),
    $("<td>").text(bill_to),
    $("<td>").text(doubles_code),
    $("<td>").text(""), // tank_code
    $("<td>").text("Equipment surcharge"),
    $("<td>").text(""), // psi_start
    $("<td>").text(""), // psi_end
    $("<td class='total_price'>").text(price.toFixed(2)),
    $("<td>").text("")
  )
  $("#tbody").append(newrow)
}

function addFill() {
  $("#tank-danger-message").addClass("hidden")
  $("#tank-danger-list").empty()

  var blender = $("#id_blender option:selected").val()
  var bill_to = $("#id_bill_to option:selected").val()
  var doubles_code = $("#id_tank option:selected").html() // tank_code or doubles_code
  var gas = $("#id_gas option:selected").val()
  var psi_start = $("#id_psi_start").val()
  var psi_end = $("#id_psi_end").val()

  doubles_code = escapeHtml(doubles_code)
  psi_start = Number(psi_start)
  psi_end = Number(psi_end)

  // TODO(stpyang): how do I move this validation to python or html5?
  if (psi_start < 0 || psi_end > 4000 || psi_start >= psi_end) {
    return false
  }

  tank_info[doubles_code].forEach(function(tank) {
    var tank_code = tank["tank_code"]
    var tank_factor = tank["tank_factor"]

    tank_code = escapeHtml(tank_code)

    addRowGas(blender, bill_to, doubles_code, tank_code, tank_factor, gas, psi_start, psi_end)

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
          $("<td>").text("Doubles Code"),
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

  var doubles_codes = new Set()

  var index = 0
  $("#tbody").find("tr").each(function(i, val) {
    var $tds = $(this).find("td")

    var blender = $tds.eq(0).text()
    var bill_to = $tds.eq(1).text()
    var doubles_code = $tds.eq(2).text()
    var tank_code = $tds.eq(3).text()
    var gas_name = $tds.eq(4).text()
    var psi_start = $tds.eq(5).text()
    var psi_end = $tds.eq(6).text()
    var total_price = $tds.eq(7).text()

    if (gas_name == "Equipment surcharge") {
      $(this).closest("tr").remove()
    } else {
      doubles_codes.add([blender, bill_to, doubles_code].join(" "))

      form.append($("<input>", { name: "blender_" + index, class: "hidden"}).attr("value", blender))
      form.append($("<input>", { name: "bill_to_" + index, class: "hidden"}).attr("value", bill_to))
      form.append($("<input>", { name: "tank_code_" + index, class: "hidden"}).attr("value", tank_code))
      form.append($("<input>", { name: "gas_name_" + index, class: "hidden"}).attr("value", gas_name))
      form.append($("<input>", { name: "psi_start_" + index, class: "hidden"}).attr("value", psi_start))
      form.append($("<input>", { name: "psi_end_" + index, class: "hidden"}).attr("value", psi_end))
      form.append($("<input>", { name: "total_price_" + index, class: "hidden"}).attr("value", total_price))
      form.append($("<input>", { name: "is_blend_" + index, class: "hidden"}).attr("value", is_blend))

      index++
    }
  })

  doubles_codes.forEach(function(key) {
    var blender = key.split(" ")[0]
    var bill_to = key.split(" ")[1]
    var doubles_code = key.split(" ")[2]

    form.append($("<input>", { name: "blender_" + index, class: "hidden"}).attr("value", blender))
    form.append($("<input>", { name: "bill_to_" + index, class: "hidden"}).attr("value", bill_to))
    form.append($("<input>", { name: "doubles_code" + index, class: "hidden"}).attr("value", doubles_code))
    form.append($("<input>", { name: "is_equipment_surcharge_" + index, class: "hidden"}).attr("value", true))

    addRowEquipmentSurcharge(blender, bill_to, doubles_code, equipment_cost_fixed)
  })

  form.append($("<input>", { name: "num_rows", class: "hidden" }).attr("value", index))
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

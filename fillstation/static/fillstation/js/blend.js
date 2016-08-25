function debug(A) {
  for(var i = 0; i < A.length; ++i) {
    temp = Array()
    for (var j = 0; j < A[i].length; ++j) {
      temp.push(A[i][j])
    }
    console.log(temp.map(function(x) { return x.toFixed(20) }))
  }
  console.log("")
}

/*
  The array must be a rectangular matrix
*/
function gaussianEliminate(array) {
  // Clone the input array
  var A = array.map(function(row) {
    return row.slice()
  })

  var num_rows = A.length
  var num_columns = A[0].length

  var j = 0
  for (var i = 0; i < num_rows && j < num_columns; i++) {
    // Search for maximum in column j
    var max_element = Math.abs(A[i][j])
    var max_row = i

    for(var k = i + 1; k < num_rows; k++) {
      if (Math.abs(A[k][i]) > max_element) {
        max_element = A[k][i]
        max_row = k
      }
    }

    // Swap maximum row with current row
    if (max_row != i) {
      var tmp = A[max_row].slice(0)
      A[max_row] = A[i]
      A[i] = tmp
    }

    // Normalize
    if (max_element != 0) {
      A[i] = A[i].map(function (x) {return x / A[i][j] })
    }

    // Make all rows above and below this one 0 in current column
    if (max_element != 0) {
      for (var k = 0; k < num_rows; k++) {
        if (k != i) {
          var c = -A[k][j]
          for(var l = i; l < num_columns; l++) {
            A[k][l] += c * A[i][l]
            // HACK(stpyang): If we are close enough to zero, make it zero
            if (Math.abs(A[k][l]) < 0.00000001) {
              A[k][l] = 0
            }
          }
        }
      }
    }

    j++
  }
  return A
}

/*
  Class to check to see if a solution is valid if:
   the first n-1 elements are between 0 and self.cubic_feet_end
   the last element is between 0 and self.cubic_feet_start
 */
function Validator(cubic_feet_start, cubic_feet_end, epsilon) {
  this.cubic_feet_start = cubic_feet_start;
  this.cubic_feet_end = cubic_feet_end;
  this.epsilon = epsilon

  // TODO(stpyang): fix epsilon (?)
  // TODO(stpyang): use slices
  // TODO(stpyang): use lodash in_range
  this.isValid = function(w) {
    var i
    for (var i = 0; i < w.length - 1; i++) {
      if (w[i] < 0 - (this.cubic_feet_end * epsilon) || Number(w[i].toFixed(8)) > Number(this.cubic_feet_end.toFixed(8))) {
        return false
      }
    }
    if (w[i] < 0 - (this.cubic_feet_end * epsilon) || Number(w[i].toFixed(8)) > Number(this.cubic_feet_start.toFixed(8))) {
      return false
    }
    return true
  }
}

function maybeAddSolution(solutions, w, v, i, target, validator) {
  var w_hat = w.slice(0)
  if (w_hat[i] != target && v[i] != 0) {
    var c = (target - w_hat[i]) / v[i]
    for(var j = 0; j < w_hat.length; j++) {
      w_hat[j] += c * v[j]
    }
  }
  if (validator.isValid(w_hat)) {
    solutions.push(w_hat)
  }
}

/*
  For matrices in row echelon form.
  This ignores the last element
*/
function zeroRow(row) {
  return row.every( function(element, index) {
    return (element == 0.0 || index == (row.length - 1))
  })
}

/*
  Assumes the input is a matrix in row echelon form
*/
function noSolution(row_echelon_array) {
  return row_echelon_array.some( function(row) {
    return (zeroRow(row) && row.slice(-1) != 0)
  })
}

/*
  Assumes the input is a matrix in row echelon form
  This ignores the last column
*/
function kernelDimension(row_echelon_array) {
  var result = 0
  row_echelon_array.forEach( function(row) {
    result += zeroRow(row)
  })
  return result;
}

/*
  Assumes the input is a matrix in row echelon form
  This ignores the last column
*/
function rank(row_echelon_array) {
  var result = 0
  row_echelon_array.forEach( function(row) {
    result += !zeroRow(row)
  })
  return result;
}

// Try to find a solution to a system of blend equstions
// return null if not possible
function findValidSolution(array, num_gas_inputs, validator) {
  var row_echelon_array = gaussianEliminate(array)

  // debug(array)
  // debug(row_echelon_array)

  // case no solutions
  if (noSolution(row_echelon_array)) {
    throw "No solution"
  }

  var v = row_echelon_array.map(function(row) { return row.slice(-2)[0] } )
  var w = row_echelon_array.map(function(row) { return row.slice(-1)[0] } )

  // case one solution
  if (rank(row_echelon_array) == num_gas_inputs + 1) {
    // the coefficients of w will be the well-defined solution to our blend equations
    // e.g. w [ 25, 50, 30] ==> fill 25, 50, 30 cubic feet respectively
    // of gas_source[0], gas_source[1], gas_start
    // we just need to check if it is valid
    if (!validator.isValid(w)) {
      throw "Unique solution is not valid"
    } else {
      return w
    }
  } else if (rank(row_echelon_array) == num_gas_inputs) {
    // we have a one-dimensional space of solutions
    // w + \lb
    // we need to check edge cases and find the one which maximizes the last
    // entry of v, i.e. minimizes the gas we need to drain

    v.push(-1)
    w.push(0)
    var solutions = []
    for(var i = 0; i < num_gas_inputs; ++i) {
      maybeAddSolution(solutions, w, v, i, 0, validator)
      maybeAddSolution(solutions, w, v, i, validator.cubic_feet_end, validator)
    }
    maybeAddSolution(solutions, w, v, w.length - 1, 0, validator)
    maybeAddSolution(solutions, w, v, w.length - 1, validator.cubic_feet_start, validator)

    if (solutions.length == 0) {
      throw "Multiple solutions are not valid"
    }

    // find the solution with the larges w[2], (drain the tank as little as possible)
    var w
    for (var i = 0; i < solutions.length; i++) {
      if (i == 0 || solutions[i].slice(-1) > w.slice(-1)) {
        w = solutions[i]
      }
    }

    return w
  } else {
    throw("I don't know!")
  }
}

function addBlend() {
  $("#tank-danger-message").addClass("hidden")
  $("#tank-danger-list").empty()

  $("#gas-sources-warning-message").addClass("hidden")

  $("#gas-solution-warning-message").addClass("hidden")
  $("#gas-solution-warning-message-content").empty()

  $("#meh-close-enough-warning-message").addClass("hidden")

  $("#drain-tank-info-message").addClass("hidden")
  $("#drain-tank-info-message-content").empty()

  var blender = $("#id_blender option:selected").val()
  var bill_to = $("#id_bill_to option:selected").val()
  var code = $("#id_tank option:selected").html()
  var gas_start = $("#id_gas_start").val()
  var oxygen_start = $("#id_oxygen_start").val()
  var helium_start = $("#id_helium_start").val()
  var psi_start = $("#id_psi_start").val()
  var gas_end = $("#id_gas_end").val()
  var helium_end = $("#id_helium_end").val()
  var oxygen_end = $("#id_oxygen_end").val()
  var psi_end = $("#id_psi_end").val()
  var gas_inputs = $("#id_gas_inputs").find("input[type=checkbox]:checked")

  code = escapeHtml(code)
  psi_start = Number(psi_start)
  oxygen_start = Number(oxygen_start)
  helium_start = Number(helium_start)
  psi_end = Number(psi_end)
  oxygen_end = Number(oxygen_end)
  helium_end = Number(helium_end)

  // TODO(stpyang): how do I move this validation to python or html5?
  if (Number(psi_start) > Number(psi_end) || (oxygen_start + helium_start) > 100 || (oxygen_end + helium_end) > 100) {
    return false
  }

  // HACK(stpyang): This is to make it work when mixing 18/45
  var helium_input = $("#id_helium").prop("checked")

  if (gas_inputs.length == 2 && helium_input) {
    $("#id_air").prop("checked", true)
    $("#id_air").parent('[class*="icheckbox"]').addClass("checked")
    gas_inputs = $("#id_gas_inputs").find("input[type=checkbox]:checked")
  }

  if (gas_inputs.length > 3) {
    $("#gas-sources-warning-message").removeClass("hidden")
    $("#myModal").modal("toggle")
    return false
  }

  tank_info[code].forEach(function(tank) {
    var tank_code = tank["tank_code"]
    var tank_factor = tank["tank_factor"]
    var cubic_feet_start = psi_start * tank_factor / 100
    var cubic_feet_end = psi_end * tank_factor / 100
    var validator = new Validator(cubic_feet_start, cubic_feet_end, 0.05) // allow up to 5% error

    tank_code = escapeHtml(tank_code)

    // get a vector representing the components of our start and end mix
    // u_start = oxygen, helium, nitrogen PER CUBIC FOOT
    // u_end = oxgen, helium, nitrogen TOTAL CUBIC FEET
    var u_start = new Array(0, 0, 0)
    if (cubic_feet_start != 0) {
      u_start = new Array(
        oxygen_start * psi_start * tank_factor / cubic_feet_start / 10000,
        helium_start * psi_start * tank_factor / cubic_feet_start / 10000,
        (100 - oxygen_start - helium_start) * psi_start * tank_factor / cubic_feet_start / 10000
      )
    }

    var u_end = new Array(
      oxygen_end * psi_end * tank_factor / 10000,
      helium_end * psi_end * tank_factor / 10000,
      (100 - oxygen_end - helium_end) * psi_end * tank_factor / 10000
    )

    // get vectors representing components of the input gases
    u = gas_inputs.map(function(i, gas) {
      var gas = $("#" + gas.id).attr("name")
      var oxygen_fraction = gas_info[gas].oxygen_percentage / 100
      var helium_fraction = gas_info[gas].helium_percentage / 100
      return [[
        oxygen_fraction,
        helium_fraction,
        1 - oxygen_fraction - helium_fraction
      ]]
    })

    var array = new Array()
    for(var i = 0; i < 3; i++) {
      var row = new Array()
      u.each(function(j, x) { row.push(x[i]) })
      row.push(u_start[i])
      row.push(u_end[i])
      array.push(row)
    }

    var solution = null
    try {
      var solution = findValidSolution(array, gas_inputs.length, validator)
    } catch (err) {
      $("#gas-solution-warning-message").removeClass("hidden")
      $("#gas-solution-warning-message-content").html(err)
      return false
    }

    if (solution.slice(-1)[0] < cubic_feet_start) {
      var psi = Math.max(100 * solution.slice(-1)[0] / tank_factor, 0)
      $("#drain-tank-info-message-content").append("Drain your tank to " + psi.toFixed(0) + " psi first!")
      $("#drain-tank-info-message").removeClass("hidden")
    }

    var psi = Math.max(100 * solution.slice(-1)[0] / tank_factor, 0)
    for (var i = 0; i < solution.length - 1; i++) {
      if (solution[i] > 0) {
        addRow(blender, bill_to, tank_code, tank_factor,
          gas_inputs[i].name, psi, psi += 100 * solution[i] / tank_factor)
      } else if (solution[i] < 0) {
        $("#meh-close-enough-warning-message").removeClass("hidden")
      }
    }
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
    if (psi.toFixed(0) != psi_end.toFixed(0)) {
      $("#meh-close-enough-warning-message").removeClass("hidden")
    }
  })

  if (!($("#tank-danger-message").hasClass("hidden")) ||
    !($("#gas-sources-warning-message").hasClass("hidden")) ||
    !($("#gas-solution-warning-message").hasClass("hidden")) ||
    !($("#meh-close-enough-warning-message").hasClass("hidden")) ||
    !($("#drain-tank-info-message").hasClass("hidden"))) {
    $("#myModal").modal("toggle")
  }

  return true
}

function changeGasInputs(gas, oxygen, helium, input_oxygen, input_helium) {
  gas = gas.val()
  if (gas == "custom") {
    oxygen.val("")
    helium.val("")
    input_oxygen.removeClass("hidden")
    input_helium.removeClass("hidden")
  } else if (gas == "trimix-30-30") {
    oxygen.val("30")
    helium.val("30")
    input_oxygen.addClass("hidden")
    input_helium.addClass("hidden")
  } else if (gas == "trimix-21-35") {
    oxygen.val("21")
    helium.val("35")
    input_oxygen.addClass("hidden")
    input_helium.addClass("hidden")
  } else if (gas == "trimix-18-45") {
    oxygen.val("18")
    helium.val("45")
    input_oxygen.addClass("hidden")
    input_helium.addClass("hidden")
  } else {
    oxygen.val(gas_info[gas].oxygen_percentage)
    helium.val(gas_info[gas].helium_percentage)
    input_oxygen.addClass("hidden")
    input_helium.addClass("hidden")
  }
}
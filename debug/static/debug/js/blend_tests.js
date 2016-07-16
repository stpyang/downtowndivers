QUnit.test("hello test", function(assert) {
  assert.ok( 1 == 1, "Passed!")
})

QUnit.test("test zeroRow", function(assert) {
  assert.ok(zeroRow(Array(1)), "(1)")
  assert.ok(zeroRow(Array(0, 1)), "(0, 1)")
  assert.ok(zeroRow(Array(0, 0, 2)), "(0, 0, 2)")
  assert.notOk(zeroRow(Array(1, 0, 0, 0)), "(1, 0, 0, 0)")
  assert.notOk(zeroRow(Array(0, 1, 0, 0)), "(0, 1, 0, 0)")
  assert.notOk(zeroRow(Array(0, 0, 1, 0)), "(0, 0, 1, 0)")
})

QUnit.test("test noSolution", function(assert) {
  assert.ok(noSolution(Array(
      Array(1, 0, 0),
      Array(0, 0, 1)
    )), "")
  assert.notOk(noSolution(Array(
      Array(1, 0, 0),
      Array(0, 0, 0)
    )), "")
  assert.notOk(noSolution(Array(
      Array(1, 0, 0),
      Array(0, 1, 0)
    )), "")
  assert.notOk(noSolution(Array(
      Array(1, 0, 1),
      Array(0, 1, 0)
    )), "")
  assert.notOk(noSolution(Array(
      Array(1, 0, 0),
      Array(0, 1, 1)
    )), "")
  assert.notOk(noSolution(Array(
      Array(1, 0, 1),
      Array(0, 1, 1)
    )), "")
  assert.ok(noSolution(Array(
      Array(1, 0, 0, 1),
      Array(0, 1, 0, 2),
      Array(0, 0, 0, 1)
    )), "")
  assert.notOk(noSolution(Array(
      Array(1, 0, 1, 1),
      Array(0, 1, 1, 2),
      Array(0, 0, 1, 1)
    )), "")
})

QUnit.test("test gaussianEliminate", function(assert) {
  // Test for rounding errors, since sometimes we are within 10e-8 of a solution
  var array = Array(
    Array(0.32000000000000000666, 0.32000000000000000666, 27.75130737943056047357),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.67999999999999993783, 0.67999999999999993783, 58.97152818128995477309)
  )
  var solution = Array(
    Array(1.00000000000000000000, 1.00000000000000000000, 86.72283556072052590480),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000)
  )

  assert.deepEqual(gaussianEliminate(array), solution, "N32 -> N32 using N32")

  array = Array(
    Array(0.32000000000000000666, 0.28000000000000002665, 24.76800000000000423483),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.67999999999999993783, 0.71999999999999997335, 52.63200000000001210765)
  )

  solution = Array(
    Array(1.00000000000000000000, 0.00000000000000000000, 77.40000000000001989520),
    Array(0.00000000000000000000, 1.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000)
  )

  assert.deepEqual(gaussianEliminate(array), solution, "N28 -> 32 using N32")

  array = Array(
    Array(0.45000000000000001110, 0.50000000000000000000, 0.32000000000000000666, 0.00000000000000000000, 38.70000000000000284217),
    Array(0.17999999999999999334, 0.00000000000000000000, 0.00000000000000000000, 1.00000000000000000000, 0.00000000000000000000),
    Array(0.37000000000000005107, 0.50000000000000000000, 0.67999999999999993783, 0.00000000000000000000, 38.70000000000000284217)
  )
  solution = Array(
    Array(1.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000, 5.55555555555555535818, 0.00000000000000000000),
    Array(0.00000000000000000000, 1.00000000000000000000, 0.00000000000000000000, -5.79012345679012252475, 77.39999999999999147349),
    Array(0.00000000000000000000, 0.00000000000000000000, 1.00000000000000000000, 1.23456790123456694452, 0.00000000000000000000)
  )

  console.log("DEBUG")
  debug(gaussianEliminate(array))
  assert.deepEqual(gaussianEliminate(array), solution, "H -> N50 using Tr18/45,N50,N32")
})

QUnit.test("test kernelDimension", function(assert) {
  // Test for rounding errors, since sometimes we are within 10e-8 of a solution
  var array = Array(
    Array(1.00000000000000000000, 1.00000000000000022204, 86.72283556072052590480),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000)
 )

  assert.deepEqual(kernelDimension(array), 2, "kernelDimension assert 1")

  array = Array(
    Array(0.32000000000000000666, 0.28000000000000002665, 24.76800000000000423483),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.67999999999999993783, 0.71999999999999997335, 52.63200000000001210765)
  )

  assert.deepEqual(kernelDimension(array), 1, "kernelDimenion assert 2")
})

QUnit.test("test rank", function(assert) {
  // Test for rounding errors, since sometimes we are within 10e-8 of a solution
  var array = Array(
    Array(1.00000000000000000000, 1.00000000000000022204, 86.72283556072052590480),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000)
 )

  assert.deepEqual(rank(array), 1, "rank assert 1")

  array = Array(
    Array(0.32000000000000000666, 0.28000000000000002665, 24.76800000000000423483),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.67999999999999993783, 0.71999999999999997335, 52.63200000000001210765)
  )

  assert.deepEqual(rank(array), 2, "rank assert 2")
})

QUnit.test("test findValidSolution", function(assert) {
  var validator = new Validator(7.74, 77.4, 0.0)

  var array = Array(
    Array(0.00000000000000000000, 0.17999999999999999334, 0.50000000000000000000, 0.00000000000000000000, 38.70000000000000284217),
    Array(1.00000000000000000000, 0.45000000000000001110, 0.00000000000000000000, 1.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.37000000000000005107, 0.50000000000000000000, 0.00000000000000000000, 38.70000000000000284217)
  )
  assert.deepEqual(
    findValidSolution(array, 3, validator),
    Array(0.0, 0.0, 77.40000000000000568434, 0.0),
    "H -> N50 using He,Tr18/45,N50"
  )

  array = Array(
    Array(0.45000000000000001110, 0.50000000000000000000, 0.32000000000000000666, 0.00000000000000000000, 38.70000000000000284217),
    Array(0.17999999999999999334, 0.00000000000000000000, 0.00000000000000000000, 1.00000000000000000000, 0.00000000000000000000),
    Array(0.37000000000000005107, 0.50000000000000000000, 0.67999999999999993783, 0.00000000000000000000, 38.70000000000000284217)
  )
  assert.deepEqual(
    findValidSolution(array, 3, validator),
    Array(0.0, 77.39999999999999, 0.0, 0.0),
    "H -> N50 using Tr18/45,N50,N32"
  )

  array = Array(
    Array(0.50000000000000000000, 0.32000000000000000666, 0.00000000000000000000, 38.70000000000000284217),
    Array(0.00000000000000000000, 0.00000000000000000000, 1.00000000000000000000, 0.00000000000000000000),
    Array(0.50000000000000000000, 0.67999999999999993783, 0.00000000000000000000, 38.70000000000000284217)
  )
  assert.deepEqual(
    findValidSolution(array, 3, validator),
    Array(77.4, 0.0, 0.0, 0.0),
    "H -> N50 using N50,N32"
  )

  array = Array(
    Array(0.00000000000000000000, 1.00000000000000000000, 0.20899999999999999134, 1.00000000000000000000, 38.70000000000000284217),
    Array(1.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.79100000000000003642, 0.00000000000000000000, 38.70000000000000284217)
  )
  assert.deepEqual(
    findValidSolution(array, 3, validator),
    Array(0, 20.734589127686476, 48.92541087231353, 7.74),
    "N50 -> N50 using O,He,Air"
  )

  array = Array(
    Array(0.00000000000000000000, 1.00000000000000000000, 0.20899999999999999134, 1.00000000000000000000, 38.70000000000000284217),
    Array(1.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.79100000000000003642, 0.00000000000000000000, 38.70000000000000284217)
  )
  assert.deepEqual(
    findValidSolution(array, 3, validator),
    Array(0, 20.734589127686476, 48.92541087231353, 7.74),
    "H -> N50 using H,O,Air"
  )

  array = Array(
    Array(1.00000000000000000000, 0.20899999999999999134, 0.20899999999999999134, 38.70000000000000284217),
    Array(0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000),
    Array(0.00000000000000000000, 0.79100000000000003642, 0.79100000000000003642, 38.70000000000000284217)
  )
  assert.deepEqual(
    findValidSolution(array, 2, validator),
    Array(28.474589127686478, 41.185410872313525, 0, 7.74),
    "Air -> N50 using O,Air"
  )

  array = Array(
    Array(0.10000000000000000555, 0.32000000000000000666, 0.20899999999999999134, 13.93200000000000216005),
    Array(0.69999999999999995559, 0.00000000000000000000, 0.00000000000000000000, 34.83000000000000540012),
    Array(0.20000000000000006661, 0.67999999999999993783, 0.79100000000000003642, 28.63800000000000522959)
  )
  assert.deepEqual(
    findValidSolution(array, 2, validator),
    Array(49.75714285714287, 28.638996138996152, -0.9961389961390086),
    "Air -> 18/45 using 10/70, 32"
  )
})
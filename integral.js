const LOG = console.log

const monteCarloIntegration = (samples, f, l = 0, u = 1, importanceSampling = false) => {
  const weight = x => 1 // todo

  return [...Array(samples)]
  .map( () => l + (u - l) * Math.random() )
  .reduce( (sum, x) => sum + f(x) / (importanceSampling ? weight(x) : 1), 0) 
    / samples * (u - l)
  }


const stratifiedIntegration = (strats, f, l = 0, u = 1, numPerStrat = 10) => {
  const intervalWindow = u - l

  const calcStrat = stratIndex => 
    [...Array(numPerStrat)]
      .map( (_, i) => l + (stratIndex + Math.random()) / strats * intervalWindow )
      .reduce( (sum, cur) => sum + f(cur), 0 )

  return [...Array(strats)]
    .map( (_, i) => calcStrat(i) )
    .reduce( (sum, x) => {
      const stratArea = intervalWindow / strats
      const stratIntegral = x / numPerStrat
      const stratContrib = stratArea * stratIntegral
      return sum + stratContrib
    }, 0)
}

const f = x => x**2
LOG(`${monteCarloIntegration.name} = ${monteCarloIntegration(1000000, f)}`)
LOG(`${stratifiedIntegration.name} = ${stratifiedIntegration(100, f)}`)
LOG(`${monteCarloIntegration.name}WithImportanceSampling = ${monteCarloIntegration(1000000, f, 0, 1, importanceSampling=true)}`)
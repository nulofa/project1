const tooltip = document.getElementById('tooltip');

fetch('../static/data_new.json')
  .then(res => res.json())
  .then(res => {
  
  createStuff(res.map(r => [
    // convertMinAndSec(r.Time),
    // r.Year,
    // r.Doping,
// r.Name
      parseFloat(r.x),
      parseFloat(r.y),
      r.similar,
      r.Title,
      r.Characteristics,
      r.Accesion_number,
      r.spearman
  ]));
});


// function convertMinAndSec(str) {
//   return new Date(`2010 01 01 00:${str}`);
// }

function createInnerHTMLForTooltip(d) {
  return `
    <p><strong>Accesion number: </strong><br>${d[5]}</p>
    <p><strong>Spearman correclation: </strong><br>${d[6]}</p>
    <p><strong>Title: </strong><br>${d[3]}</p>
    <p><strong>Characteristics: </strong><br>${d[4]}</p>
    
    
  `;
}

function createStuff(data) {
  const width = 900;
  const height = 500;
  const padding = 80;
  
  const circleRadius = 4;
  
  // const yScale = d3.scaleTime()
  //     .domain([d3.min(data, d => d[0]), d3.max(data, d => d[0])])
  //     .range([padding, height - padding]);
  const yScale= d3
        .scaleLinear()
        .domain([d3.min(data, d => d[0])-10, d3.max(data, d => d[0])]) // input
        .range([padding, height - padding]);

  const xScale =d3
        .scaleLinear()
        .domain([d3.min(data, d => d[1]), d3.max(data, d => d[1])]) // input
        .range([padding, width - padding]);
  
  // const xScale = d3.scaleTime()
  //     .domain([
  //       d3.min(data, d => new Date(d[1] - 1)),
  //       d3.max(data, d => new Date(d[1] + 1))
  //     ])
  //     .range([padding, width - padding]);

  console.log(d3.max(data, d => d[1]));
  console.log(d3.max(data, d => d[0]));
  console.log('{{ip }}');
  
  
  const svg = d3.select('#container').append('svg')
          .attr('width', width)
          .attr('height', height);
  
  // create the graph
  svg.selectAll('circle')
    .data(data)
    .enter()
    .append('circle')
    .attr('class', 'dot')
    .attr('data-xvalue', d => d[1])
    .attr('data-yvalue', d => d[0])
    .attr('cx', d => xScale(d[1]))
    .attr('cy', d => yScale(d[0]))
    .attr('fill', d => d[2] === '' ? 'yellowgreen' : 'firebrick')
    .attr('stroke', 'black')
    .attr('r', circleRadius)
    .on('mouseover', (d, i) => {
      tooltip.classList.add('show');
      tooltip.style.left = xScale(d[1]) + 10 + 'px';

      tooltip.style.top = yScale(d[0]) - 10 + 'px';

      // tooltip.setAttribute('data-year', d[1])

      tooltip.innerHTML = createInnerHTMLForTooltip(d);
  }).on('mouseout', () => {
     tooltip.classList.remove('show');
  });
  
  // format the data
  // const timeFormatForMinAndSec = d3.timeFormat("%M:%S");
  // const timeFormatForYear = d3.format("d");
  
  // create axis
  const xAxis = d3.axisBottom(xScale)
    .scale(xScale)
  const yAxis = d3.axisLeft(yScale)
    .scale(yScale)
  
  svg.append('g')
    .attr('id', 'x-axis')
    .attr('transform', `translate(0, ${height - padding})`)
    .call(xAxis);
  
  svg.append('g')
    .attr('id', 'y-axis')
    .attr('transform', `translate(${padding}, 0)`)
    .call(yAxis)
}
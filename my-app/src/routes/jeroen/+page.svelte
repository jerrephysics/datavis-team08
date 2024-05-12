<script lang="js">

import * as d3 from 'd3';
import { onMount } from 'svelte';


let data = [] ;
let file = '';
let grouping = '';

const grouping_title = {"region":"Region",
						"regionalmanager":"Regional Manager",
						"area":"Area",
						"areamanager":"Area Manager",
						"nation": "Nation"};

const load = async () => {
	file = d3.select('input[name="grouping"]:checked').node().value;
	grouping = grouping_title[file];
	console.log(grouping)
	data = await d3.csv(`/jer-data-${file}.csv`,(d) => {return {z: +d.CartPriceInCP, y: +d.Time, x: 1, area: d.Location};})
.then(data => redraw(data));
}



onMount(() => {
		//d3.select('#region').checked = true;
		//load();
		//redraw();
		window.addEventListener('resize',load);
		d3.selectAll('input[name="grouping"]').on('click',load);
	})


//let vis;

const qui_magenta = "#8E4162";
const tea_green = "#D7E8BA";
const moonstone = "#4DA1A9";
const neon_blue = "#4361EE";
const tyrian_purple = "#611C35";
//const colormap = [qui_magenta, tea_green,moonstone,neon_blue,tyrian_purple];

const bg = '#282a36';
const fg = '#f8f8f2';
const cyan = '#8be9fd';
const green = '#50fa7b';
const orange = '#ffb86c';
const pink = '#ff79c6';
const purple = '#bd93f9';
const red = '#ff5555';
const yellow = '#f1fa8c';

const colormap = [cyan,green,orange, pink, purple, red,yellow];

const margin = {top:		20,
				bottom:		20,
				left:		20,
				right:		20};

let width;
let height;


function redraw(data) {
	d3.select('#vis').html(null);
	let min_vals = [Infinity, Infinity, Infinity];
	let max_vals = [-Infinity, -Infinity, -Infinity];

	for (let dat of data){
		min_vals[0] = Math.min(dat.x, min_vals[0]);
		max_vals[0] = Math.max(dat.x, max_vals[0]);
		min_vals[1] = Math.min(dat.y, min_vals[1]);
		max_vals[1] = Math.max(dat.y, max_vals[1]);
		min_vals[2] = Math.min(dat.z, min_vals[2]);
		max_vals[2] = Math.max(dat.z, max_vals[2]);
	}

	let xScale = d3.scaleLinear().domain([0.9*min_vals[0],1.1* max_vals[0]]);
	let yScale = d3.scaleLinear().domain([0.9*min_vals[1], 1.2*max_vals[1]]);
	let zScale = d3.scaleLinear().domain([0.9*min_vals[2],1.1* max_vals[2]]);
	
	width = d3.select('#vis').node().getBoundingClientRect().width - margin.left - margin.right;
	height = d3.select('#vis').node().getBoundingClientRect().height - margin.top - margin.bottom;
	
	const MAX_WIDTH = 20;
	const MIN_WIDTH = 2;
	const MAX_RADIUS = 1.5*MAX_WIDTH;
	const MIN_RADIUS = MAX_WIDTH;
	const MAX_LENGTH = (Math.floor(Math.min(width, height) / 2) - MAX_RADIUS) * 0.8;
	const MIN_LENGTH = 0.2 * MAX_LENGTH;
	
	const center = {x: Math.floor(width / 2), y: Math.floor(height / 2) };
	
	xScale.range([MIN_WIDTH, MAX_WIDTH]);	
	yScale.range([MIN_LENGTH, MAX_LENGTH]);	
	zScale.range([MIN_RADIUS, MAX_RADIUS]);	

const svg = d3.select('#vis')
				.append('svg')
				.attr('width', width + margin.left + margin.right)
				.attr('height', height + margin.top + margin.bottom)
				.style('background',bg)
				.append('g')
				.attr('transform', `translate(${[Math.floor(width / 2), Math.floor(height/ 2)]})`);



svg.append('g').selectAll('rect')
	.data(data)
	.enter()
	.append('rect')
	.attr('width', function (d) {return xScale(d.x);})
	.attr('height', function (d) {return yScale(d.y);})
	.attr('x', function (d) { return -0.5 * xScale(d.x); })
	.attr('y', 0)
	.attr('transform', function (d,i) { return `rotate( ${ 180 + (i / data.length) * 360},0,0)`;})
	.style('fill',function (d,i) { return colormap[i % colormap.length]; });

svg.append('g').selectAll('circle')
	.data(data)
	.enter()
	.append('circle')
	.attr('cx', 0)
	.attr('cy', function(d) { return yScale(d.y);})
	.attr('r', function (d) {return zScale(d.z);})
	.attr('fill-opacity',1)
	.style('fill',function (d,i) { return colormap[i % colormap.length]; })
	.attr('transform', function (d,i) {return `rotate(${180 + i / data.length * 360}, 0, 0)`;});




let polygon_points = []
let angle = Math.PI / 2  + Math.PI /  data.length;

for (let step = 0; step < data.length; step++){
	console.log(angle);
	console.log(Math.cos(angle));
	polygon_points.push(MAX_WIDTH  * Math.cos(angle));
	polygon_points.push(MAX_WIDTH * Math.sin(angle));
	angle += 2*Math.PI / data.length;
}
console.log(polygon_points);

svg.append('g').append('polygon')
	.attr('points',polygon_points)
	.attr('transform','rotate(180,0,0)')
	.style('fill',bg);


svg.append('g').selectAll('text')
	.data(data)
	.enter()
	.append('text')
	.attr('y',0)
	.attr('x',0)
	.style('fill',fg)
	.attr('dominant-baseline', 'middle')
	.attr('text-anchor', 'middle')
	.text(function (d) {return d.area;})
	.attr('transform', function (d,i) {
		let angle = 3*Math.PI/2 + i / data.length * 2 * Math.PI;
		let r= 1.3 * ( yScale(d.y)+zScale(d.z) );
		return `translate(${r * Math.cos(angle)}, ${r * Math.sin(angle)})`;
		})
	


}//redraw

</script>


<h1> Flower plot for data grouped by {grouping}</h1>
<div id="selection">
<label for="selectionlist">Select grouping: </label>
<input type="radio" id="region" name="grouping" value="region">
<label for="region">Region</label>

<input type="radio" id="regionalmanager" name="grouping" value="regionalmanager">
<label for="area">Regional manager</label>

<input type="radio" id="area" name="grouping" value="area">
<label for="area">Area</label>

<input type="radio" id="areamanager" name="grouping" value="areamanager">
<label for="area">Area manager</label>

<input type="radio" id="nation" name="grouping" value="nation">
<label for="area">Nation</label>
</div>
<div id="vis"></div>

<style>

	#selection{
		max-width: fit-content;
		margin-inline: auto;
	}

	#vis {
		position: fixed;
		width: 100%;
		height: 85%;
		flex: auto;
	}

	circle {
		fill: black;
		fill-opacity: 0.5;
	}
	


</style>

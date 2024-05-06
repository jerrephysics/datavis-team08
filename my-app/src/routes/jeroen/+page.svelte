<script lang="ts">

import * as d3 from 'd3';
import { onMount } from 'svelte';

//let vis;

const qui_magenta = "#8E4162";
const tea_green = "#D7E8BA";
const moonstone = "#4DA1A9";
const neon_blue = "#4361EE";
const tyrian_purple = "#611C35";
const colormap = [qui_magenta, tea_green,moonstone,neon_blue,tyrian_purple];


const margin = {top:		0,
				bottom:		0,
				left:		0,
				right:		0};

let width;
let height;

let data = [];
for (let i = 0; i<5; ++i){
	data.push({x: Math.random(), y: Math.random() ,z: Math.random(), area: "Area " + i});
}

let i = data.length

data.push({x:1, y:1, z:1, area: "Area " + (i +1)})
data.push({x:0, y:0, z:0, area: "Area " + (i +2)})
data.push({x:1, y:1, z:0, area: "Area " + (i +3)})
data.push({x:0, y:0, z:1, area: "Area " + (i +4)})


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

onMount(() => {
		redraw();
		window.addEventListener('resize',redraw);
	})

function redraw() {
	d3.select('#vis').html(null);
	
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
	polygon_points.push( MAX_WIDTH  * Math.cos(angle));
	polygon_points.push( MAX_WIDTH * Math.sin(angle));
	angle += 2*Math.PI / data.length;
}
console.log(polygon_points);

svg.append('g').append('polygon')
	.attr('points',polygon_points)
	.attr('transform','rotate(180,0,0)')
	.style('fill','black');


svg.append('g').selectAll('text')
	.data(data)
	.enter()
	.append('text')
	.attr('y',0)
	.attr('x',0)
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


<h1> Jeroen ({width}, {height})</h1>
<div id="vis"></div>

<style>


	#vis {
		position: fixed;
		width: 100%;
		height: 85%;
		background-color: whitesmoke;
		flex: auto;
	}

	circle {
		fill: black;
		fill-opacity: 0.5;
	}


</style>

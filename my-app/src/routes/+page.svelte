<script lang='js'>
import * as d3 from 'd3';
import { onMount } from 'svelte';

const month_name = ["January","February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

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

$: data = [];
$: years = [];
$:  months = [];
$: width = 120;
$: height = 120;
$: y_select= 2019;
$: m_select = 1;
$: managers = [];
let y = 2023;
let m = 12;

function rewrite (){
	y_select = d3.select('#years').node().value;
	m_select = d3.select('#months').node().value;	
	managers = data[y_select][m_select];
	console.log('rewrite')
}

onMount ( async () => {
data = await d3.json('/top3.json');
years = Object.keys(data);
months = Object.keys(data[years[0]])

d3.selectAll('select[name="years"]').on('change',rewrite);
d3.selectAll('select[name="months"]').on('change',rewrite);
window.addEventListener('resize',redraw);
redraw();


function redraw () {
	d3.select('#vis').html(null);
	width = Math.round(d3.select('#vis').node().getBoundingClientRect().width);
	height = Math.round(d3.select('#vis').node().getBoundingClientRect().height);
	y = years[years.length - 1];
	m = months[months.length - 1];

	console.log(y,m)
const svg = d3.select('#vis');//.append('svg').attr('width',width).attr('height', height);


//svg.attr('width',width).attr('height', height);

console.log([width, height])


svg.append('rect').attr('width',width/3).attr('height',2*height/4).style('fill',cyan).attr("transform",`translate(0,${2*height/4})`);
svg.append('rect').attr('width', width/3).attr('height', 3*height/4).style('fill',cyan).attr("transform",`translate(${width/3}, ${height/4})`)
svg.append('rect').attr('width', width/3).attr('height', 1*height/4).style('fill',cyan).attr("transform",`translate(${2*width/3}, ${3*height/4})`)

svg.append('text').attr('x', width/6).attr('y', 3*height/8).text(data[y][m][0]).style('fill',fg).attr('dominant-baseline','lower').attr('text-anchor','middle')
svg.append('text').attr('x', 3*width/6).attr('y', height/8).text(data[y][m][1]).style('fill',fg).attr('dominant-baseline','lower').attr('text-anchor','middle')
svg.append('text').attr('x', 5*width/6).attr('y', 5*height/8).text(data[y][m][2]).style('fill',fg).attr('dominant-baseline','lower').attr('text-anchor','middle')


}//redraw

});
</script>

<h1>Home</h1>

<h2>Top regional managers of last month</h2>

<svg id='vis'></svg>

<h2>Search top regional managers</h2>
<label for='years'> Year: </label>
<select name='years' id='years' on:change={rewrite}>
{#each years as y }
<option value={y}>{y}</option>
{/each}
</select>
<label for="months"> Month: </label>
<select name='months' id='months'>
{#each months as m}
<option value={m}>{m}</option>
{/each}
</select>
<ol>
{#each managers as m}
<li> {m}
{/each}
</ol>

<style>
	#vis{
		width:100%;
		height:200px;
	}
	body {
		height:100%;
}
</style>

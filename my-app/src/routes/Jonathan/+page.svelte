<script lang="ts">
    import { scaleLinear } from 'd3-scale';
    import * as d3 from 'd3';
    import { extent } from 'd3-array';
    import { writable } from 'svelte/store';
    //import TheMap from '../../../image.jpg';
    import { draw } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount } from 'svelte';
    import { getContext } from 'svelte';
  
    export let data = [];
    export let selected_datapoint = undefined;
    const yTicks = Array.from({ length: 41 }, (_, i) => i * 10);
	const xTicks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];
	const padding = { top: 20, right: 15, bottom: 20, left: 25 };

    let visible = true;
    let temp = false;
    let showtemp = [false,false,false,false];
    let selectedItems = [];
    let availableOptions = ["North","East","South","West","Underdark"];
    let showNorth = false;
    let showEast = false;
    let showSouth = false;
    let showWest = false;
    let showUnderdark = false;
    let showCircles = writable([showNorth,showEast,showSouth,showWest,showUnderdark]);

    let all_cities = data.deadregions.map(entry => entry.Territory);
    let all_north_cities = data.deadregions.filter(entry => entry.Area == "North").map(entry => entry.Territory);
    let all_east_cities = data.deadregions.filter(entry => entry.Area == "East").map(entry => entry.Territory);
    let all_south_cities = data.deadregions.filter(entry => entry.Area == "South").map(entry => entry.Territory);
    let all_west_cities = data.deadregions.filter(entry => entry.Area == "West").map(entry => entry.Territory);
    let all_underdark_cities = data.deadregions.filter(entry => entry.Area == "Underdark").map(entry => entry.Territory);
    let all_order_dates = data.deadorders.map(entry => entry.OrderDate).map(entry => new Date(entry));
    let all_delivery_dates = data.deadorders.map(entry => entry.DeliveryDate).map(entry => new Date(entry));
    let all_north_order_dates = data.deadorders.filter(entry => all_north_cities.includes(entry.Territory)).map(entry => entry.OrderDate).map(entry => new Date(entry));
    let all_east_order_dates = data.deadorders.filter(entry => all_east_cities.includes(entry.Territory)).map(entry => entry.OrderDate).map(entry => new Date(entry));
    let all_city_order_dates = [];
    let all_city_delivery_dates = [];
  
    const svgWidth = 1000;
    const svgHeight = 668.7;
    const scaleX = scaleLinear().domain([-100,4600]).range([0,svgWidth]);
    const scaleY = scaleLinear().domain([0,3300]).range([svgHeight,0]);
    const scaleColour = scaleLinear().domain([0,671]).range(["red","green"]);
    const scaleRadius = scaleLinear().domain([100,2632]).range([4,10]);
    const getAverage = (array) => array.reduce((sum, currentValue) => sum + currentValue, 0) / array.length;
    const MAX_SELECTED_ITEMS = 5; 
	const MAX_AVAILABLE_OPTIONS = 5;

    let mouse_x, mouse_y;
    const setMousePosition = function(event) {
    mouse_x = event.clientX;
    mouse_y = event.clientY;
    }
    let color = "";

    function chooseColour(value) {
        if (all_north_cities.includes(value)) {
            color = "blue";
        } else if (all_east_cities.includes(value)) {
            color = "green";
        } else if (all_south_cities.includes(value)) {
            color = "orange";
        } else if (all_west_cities.includes(value)) {
            color = "brown";
        } else if (all_underdark_cities.includes(value)) {
            color = "black";
        } else {
            color = "default"; // If value doesn't belong to any list, you can set a default color
        }
        return color;
    }

    let chosenItems = [];

    const updateSelectedItems = (value, index) => {
        // Remove any items from `chosenItems` that are no longer selected.
        chosenItems = chosenItems.filter(x => selectedItems.includes(x))
    
        // Make sure that the new items do not include any already selected items.
        let newItems = selectedItems.filter(x => !chosenItems.includes(x))

        // Merge the previously chosen items, with the newly selected items. 
        chosenItems = [...chosenItems, ...newItems].slice(-MAX_SELECTED_ITEMS);

        // And now update the group of selected items to only include the once that are chose.
        selectedItems = selectedItems.filter(x => chosenItems.includes(x))

        toggleCircles(value, index);
	}

    function toggleCircles(value, index) {
        if (value == "North"){
            showNorth = !showNorth;
        } else if (value == "East"){
            showEast = !showEast; 
        } else if (value == "South"){
            showSouth = !showSouth; 
        } else if (value == "West"){
            showWest = !showWest; 
        } else {
            showUnderdark = !showUnderdark; 
        }
        showCircles.update(circles => {
            let newCircles = [...circles];
            newCircles[index] = !newCircles[index];
            return newCircles;
        });
    }

    function update_all_city_delivery_dates(selected_datapoint){
        all_city_delivery_dates = data.deadorders.filter(entry => entry.Territory ==  selected_datapoint.popup.title).map(entry => entry.DeliveryDate).map(entry => new Date(entry));
        return all_city_delivery_dates;
    }

    function update_all_city_order_dates(selected_datapoint){
        all_city_order_dates = data.deadorders.filter(entry => entry.Territory ==  selected_datapoint.popup.title).map(entry => entry.OrderDate).map(entry => new Date(entry));
        return all_city_order_dates;
    }

    function subtractArrays(arr1, arr2) {
        return arr1.map((value, index) => value - arr2[index]);
    }

    let path = '';
	let linecolor = 'red';
	let loaded = false;

    function formatArrayToString(array) {
        let formattedString = '';
        array.forEach((value, index) => {
            if (index === 0) {
                formattedString += `M${index + 1}:${value}`; // Move to the first point
            } else {
                formattedString += ` L${index + 1}:${value}`; // Draw a line to subsequent points
            }
        });
        return formattedString;
    }

    function formatArrayToPathData(array, scaleXFunc , scaleYFunc) {
        let pathData = '';
        array.forEach((value, index) => {
            const x = scaleXFunc(index + 1); // Scale x-coordinate if needed
            const y = scaleYFunc(value); // Scale y-coordinate if needed
            if (index === 0) {
                pathData += `M${x},${y}`; // Move to the first point
            } else {
                pathData += ` L${x},${y}`; // Draw a line to subsequent points
            }
        });
        return pathData;
    }

    function createScalingFunctions(dataArray) {
        // Define the input domain (the range of values in your data array)
        const xDomain = [1, dataArray.length]; // Assuming 1-based indexing for the x-axis
        const yDomain = [Math.min(...dataArray), Math.max(...dataArray)]; // Assuming y-axis range from min to max values
        
        // Define the output range (the dimensions of your SVG)
        const xRange = [200,svgWidth-200];
        const yRange = [svgHeight-200, 0]; // In SVG, y-coordinates increase from top to bottom
        
        // Create scaling functions for x and y coordinates
        const scaleXFunc = d3.scaleLinear().domain(xDomain).range(xRange);
        const scaleYFunc = d3.scaleLinear().domain(yDomain).range(yRange);

        return { scaleXFunc, scaleYFunc };
    }

    function generateHistogramData(dataArray) {
        var histogram = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

        for (var i = 0; i < dataArray.length; i++) {
            var value = dataArray[i];

            if (value >= 0 && value < 1) {
                histogram[0]++;
            } else if (value >= 1 && value < 2) {
                histogram[1]++;
            } else if (value >= 2 && value < 3) {
                histogram[2]++;
            } else if (value >= 3 && value < 4) {
                histogram[3]++;
            } else if (value >= 4 && value < 5) {
                histogram[4]++;
            } else if (value >= 5 && value < 6) {
                histogram[5]++;
            } else if (value >= 6 && value <= 7) {
                histogram[6]++;
            } else if (value >= 7 && value <= 8) {
                histogram[7]++;
            } else if (value >= 8 && value <= 9) {
                histogram[8]++;
            } else if (value >= 9 && value <= 10) {
                histogram[9]++;
            } else if (value >= 10 && value <= 11) {
                histogram[10]++;
            } else if (value >= 11 && value <= 12) {
                histogram[11]++;
            } else if (value >= 12 && value <= 13) {
                histogram[12]++;
            } else if (value >= 13 && value <= 14) {
                histogram[13]++;
            } else if (value >= 14 && value <= 15) {
                histogram[14]++;
            } else if (value >= 15 && value <= 16) {
                histogram[15]++;
            } else if (value >= 16 && value <= 17) {
                histogram[16]++;
            } else if (value >= 17 && value <= 18) {
                histogram[17]++;
            }
        }

        return histogram;
    }

	onMount(() => {
		loaded = true;
	});
</script>
  
<style>
    circle {
        fill-opacity: 0.5;
    }
    circle.selected {
        fill: red;
        fill-opacity: 1;
    }
    circle:has(input[type="checkbox"]:checked){
        fill-opacity: 0;
    }
    #tooltip {
    position: fixed;
    background-color: white;
    padding: 3px;
    border: solid 1px;
    }
    svg.tooltip {
        margin: 0px;
        padding: 0px;
    }
    label {
        user-select: none;
    }
	label:has(input[type="checkbox"]:checked){
		color:green
	}
    svg{
        background-color: whitesmoke;
        fill: transparent;
    }

    .Line {
		transition: all 0.3s ease-out;
        visibility: visible;
        display: unset;
        fill: none;
        stroke: red;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .chart,
	h2,
	p {
		width: 100%;
		max-width: 500px;
		margin-left: 200px;
		margin-right: 200px;
	}

	.tick {
		font-size: 0.725em;
		font-weight: 200;
	}

	.tick line {
		stroke: #ffcc02;
		stroke-dasharray: 3;
	}

	.tick text {
		fill: #ffcc02;
		text-anchor: start;
	}

	.tick.tick-0 line {
		stroke-dasharray: 0;
	}

	.x-axis .tick text {
		text-anchor: middle;
	}

	.path-line {
		fill: none;
		stroke: rgb(100, 38, 0);
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 2;
	}

	.path-area {
		fill: rgba(0, 100, 100, 0.2);
	}
</style>


<h1> Map of the Forgotten realms</h1>
<svg width={svgWidth} height={svgHeight}>
    {#if selected_datapoint != undefined}
        {#each [subtractArrays(data.deadorders.filter(entry => entry.Territory ==  selected_datapoint.popup.title).map(entry => entry.DeliveryDate).map(entry => new Date(entry)),data.deadorders.filter(entry => entry.Territory ==  selected_datapoint.popup.title).map(entry => entry.OrderDate).map(entry => new Date(entry))).map(entry => entry/(1000*3600*24))] as path}
            {#each [createScalingFunctions(generateHistogramData(path))] as { scaleXFunc, scaleYFunc }}
                <g class="axis y-axis" transform="translate(0, {padding.top})">
                    <text x={-75} y={100} text-anchor="middle" fill="#ffcc02" transform="rotate(-90)">Frequency (number of orders)</text>
                    {#each yTicks as tick}
                        <g class="tick tick-{tick}" transform="translate(0, {scaleYFunc(tick) - padding.bottom})">
                            <line x2="100%" />
                            <text y="-4">{tick} {tick === 8 ? ' million sq km' : ''}</text>
                        </g>
                    {/each}
                </g>
                <g class="axis x-axis">
                    <text x={750} y={500} text-anchor="middle" fill="#ffcc02" transform="rotate(0)">Delivery time = Deliverydate - Orderdate (days)</text>
                    {#each xTicks as tick}
                        <g class="tick tick-{tick}" transform="translate({scaleXFunc(tick)},{svgHeight})">
                            <line y1="-{svgHeight}" y2="-{padding.bottom}" x1="0" x2="0" />
                            <text y="-2">{svgWidth > 380 ? tick : formatMobile(tick)}</text>
                        </g>
                    {/each}
                </g>
                <path
                    in:draw={{
                        duration: 2000,
                        easing: quintOut
                    }}
                    class={`Line`}
                    d={formatArrayToPathData(generateHistogramData(path), scaleXFunc, scaleYFunc)}
                    fill="none"
                    stroke={linecolor}
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                /> 
            {/each}
        {/each}
    {/if}
    {#if visible}
        <image
            x="0"
            y="0"
            width={svgWidth}
            height={svgHeight} 
            href = "http://localhost:5173/image.jpg"/>
    {/if}
    {#each data.regions as datapoint}
        {#each datapoint.markers as city}
            {#if all_cities.includes(city.popup.title)}
                {#if all_north_cities.includes(city.popup.title) && showNorth}
                    <circle cx={scaleX(city.position[0]-92.16)}
                    cy={scaleY(city.position[1]+97)}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event); temp = visible; visible = false; showtemp[0] = showEast; showtemp[1] = showSouth; showtemp[2] = showWest; showtemp[3] = showUnderdark; showEast = false; showSouth = false; showWest = false; showUnderdark = false}}
                    on:mouseout={function() {selected_datapoint = undefined; visible = temp; showEast = showtemp[0]; showSouth = showtemp[1]; showWest = showtemp[2]; showUnderdark = showtemp[3]}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_east_cities.includes(city.popup.title) && showEast}
                    <circle cx={scaleX(city.position[0]-92.16)}
                    cy={scaleY(city.position[1]+97)}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event); temp = visible; visible = false; showtemp[0] = showNorth; showtemp[1] = showSouth; showtemp[2] = showWest; showtemp[3] = showUnderdark; showNorth = false; showSouth = false; showWest = false; showUnderdark = false}}
                    on:mouseout={function() {selected_datapoint = undefined; visible = temp; showNorth = showtemp[0]; showSouth = showtemp[1]; showWest = showtemp[2]; showUnderdark = showtemp[3]}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_south_cities.includes(city.popup.title) && showSouth}
                    <circle cx={scaleX(city.position[0]-92.16)}
                    cy={scaleY(city.position[1]+97)}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event); temp = visible; visible = false; showtemp[0] = showNorth; showtemp[1] = showEast; showtemp[2] = showWest; showtemp[3] = showUnderdark; showNorth = false; showEast = false; showWest = false; showUnderdark = false}}
                    on:mouseout={function() {selected_datapoint = undefined; visible = temp; showNorth = showtemp[0]; showEast = showtemp[1]; showWest = showtemp[2]; showUnderdark = showtemp[3]}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_west_cities.includes(city.popup.title) && showWest}
                    <circle cx={scaleX(city.position[0]-92.16)}
                    cy={scaleY(city.position[1]+97)}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event); temp = visible; visible = false; showtemp[0] = showNorth; showtemp[1] = showEast; showtemp[2] = showSouth; showtemp[3] = showUnderdark; showNorth = false; showEast = false; showSouth = false; showUnderdark = false}}
                    on:mouseout={function() {selected_datapoint = undefined; visible = temp; showNorth = showtemp[0]; showEast = showtemp[1]; showSouth = showtemp[2]; showUnderdark = showtemp[3]}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_underdark_cities.includes(city.popup.title) && showUnderdark}
                    <circle cx={scaleX(city.position[0]-92.16)}
                    cy={scaleY(city.position[1]+97)}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event); temp = visible; visible = false; showtemp[0] = showNorth; showtemp[1] = showEast; showtemp[2] = showSouth; showtemp[3] = showWest; showNorth = false; showEast = false; showSouth = false; showWest = false}}
                    on:mouseout={function() {selected_datapoint = undefined; visible = temp; showNorth = showtemp[0]; showEast = showtemp[1]; showSouth = showtemp[2]; showWest = showtemp[3]}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
            {/if}
    {/each}
{/each}
</svg>

<div class="checkboxes">
{#each availableOptions as value, index}
<label>
	<input
        type="checkbox"
        name="items"
        value={value}	 
        bind:group={selectedItems}
        on:change={() => updateSelectedItems(value, index)}
		/>
	<span>{value} Area</span>
</label>
{/each}
</div>
<button on:click={() => visible = !visible}>Remove/Show map</button>

{#if selected_datapoint != undefined}
    <div id="tooltip" style="left: {mouse_x + 10}px; top: {mouse_y - 10}px">
    Territory: {selected_datapoint.popup.title}, orders: {data.deadorders.filter(entry => entry.Territory == selected_datapoint.popup.title).length}, 
    average delivery time: {getAverage(subtractArrays(update_all_city_delivery_dates(selected_datapoint),update_all_city_order_dates(selected_datapoint)))/(1000*3600*24)} days
    </div>
{/if}
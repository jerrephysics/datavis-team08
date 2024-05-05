<script>
    import { scaleLinear } from 'd3-scale';
    import { extent } from 'd3-array';
    import { writable } from 'svelte/store';
  
    export let data = [];
    export let selected_datapoint = undefined;
    let value = undefined;
    let index = 1;
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
    let all_order_dates = data.deadorders.map(entry => entry.OrderDate);
    let all_north_order_dates = data.deadorders.map(entry => entry.OrderDate);
    let all_delivery_dates = data.deadorders.map(entry => entry.DeliveryDate);
    //console.log(all_order_dates);
  
    const scaleX = scaleLinear().domain([-100,4600]).range([0,1200])
    const scaleY = scaleLinear().domain([0,3300]).range([600,0])
    const scaleColour = scaleLinear().domain([0,671]).range(["red","green"])
    const scaleRadius = scaleLinear().domain([100,2632]).range([4,10])
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
</style>
  
<svg width="1200" height="600">
    {#each data.regions as datapoint}
        {#each datapoint.markers as city}
            {#if all_cities.includes(city.popup.title)}
                {#if all_north_cities.includes(city.popup.title) && showNorth}
                    <circle cx={scaleX(city.position[0])}
                    cy={scaleY(city.position[1])}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event)}}
                    on:mouseout={function() {selected_datapoint = undefined}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_east_cities.includes(city.popup.title) && showEast}
                    <circle cx={scaleX(city.position[0])}
                    cy={scaleY(city.position[1])}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event)}}
                    on:mouseout={function() {selected_datapoint = undefined}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_south_cities.includes(city.popup.title) && showSouth}
                    <circle cx={scaleX(city.position[0])}
                    cy={scaleY(city.position[1])}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event)}}
                    on:mouseout={function() {selected_datapoint = undefined}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_west_cities.includes(city.popup.title) && showWest}
                    <circle cx={scaleX(city.position[0])}
                    cy={scaleY(city.position[1])}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event)}}
                    on:mouseout={function() {selected_datapoint = undefined}}
                    style={"fill:" + chooseColour(city.popup.title)}>
                        <title>{city.popup.title}</title>
                    </circle>
                {/if}
                {#if all_underdark_cities.includes(city.popup.title) && showUnderdark}
                    <circle cx={scaleX(city.position[0])}
                    cy={scaleY(city.position[1])}
                    r= {scaleRadius(data.deadorders.filter(entry => entry.Territory == city.popup.title).length)}
                    class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                    on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event)}}
                    on:mouseout={function() {selected_datapoint = undefined}}
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

{#if selected_datapoint != undefined}
<div id="tooltip" style="left: {mouse_x + 10}px; top: {mouse_y - 10}px">
Territory: {selected_datapoint.popup.title}, orders: {data.deadorders.filter(entry => entry.Territory == selected_datapoint.popup.title).length}
</div>
{/if}
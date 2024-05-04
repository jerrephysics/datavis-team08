<script>
    import { scaleLinear } from 'd3-scale';
    import { extent } from 'd3-array';
  
    export let data = [];
    export let selected_datapoint = undefined;
    let all_cities = data.deadregions.map(entry => entry.Territory);
    //let all_order_dates = data.deadorders.map(entry => entry.OrderDate);
    //let all_delivery_dates = data.deadorders.map(entry => entry.DeliveryDate);
  
    const scaleX = scaleLinear().domain([200,3300]).range([0,1200])
    const scaleY = scaleLinear().domain([0,2700]).range([0,600])
    const scaleColour = scaleLinear().domain([0,671]).range(["red","green"])

    let mouse_x, mouse_y;
    const setMousePosition = function(event) {
    mouse_x = event.clientX;
    mouse_y = event.clientY;
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
</style>
  
<svg width="1200" height="600">
    {#each data.regions as datapoint}
        {#each datapoint.markers as city}
            {#if all_cities.includes(city.popup.title)}
                <circle cx={scaleX(city.position[0])}
                cy={scaleY(city.position[1])}
                r=3
                class:selected="{selected_datapoint && city.id == selected_datapoint.id}"
                on:mouseover={function(event) {selected_datapoint = city; setMousePosition(event)}}
                on:mouseout={function() {selected_datapoint = undefined}}
                style={"fill:"+ scaleColour(Math.sqrt((scaleX(city.position[0]) - 600)^2 + (scaleY(city.position[1]) - 300)^2))}>
                    <title>{city.popup.title}</title>
                </circle>
            {/if}
    {/each}
{/each}
</svg>

<u1>
    {#each data.regions as datapoint}
        {#each datapoint.markers as city}

            {#if all_cities.includes(city.popup.title)}
                <li>{city.popup.title}, with coordinates: {city.position} and id: {city.id}</li>
            {/if}
        {/each}
    {/each}
</u1>

{#if selected_datapoint != undefined}
<div id="tooltip" style="left: {mouse_x + 10}px; top: {mouse_y - 10}px">
<svg class="tooltip" width=20 height=20>
  <g transform="translate(10,10)">
  <data.regions datapoint={selected_datapoint} />
  </g>
</svg><br/>
Territory: {selected_datapoint.popup.title}, coordinates: ({selected_datapoint.position})
</div>
{/if}
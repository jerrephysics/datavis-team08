<script>
    export let data = [];

    const rescale = function(x, domain_min, domain_max, range_min, range_max) {
        return ((range_max - range_min)*(x-domain_min))/(domain_max-domain_min) + range_min
    }
</script>
  
<style>
circle {
    fill: steelblue;
    fill-opacity: 0.5;
}
</style>
  
<svg width="800" height="400">
    {#each data.flights as datapoint}
        <circle cx={rescale(datapoint.from_long, -180, 180, 0, 800)}
                cy={rescale(datapoint.from_lat, -90, 90, 400, 0)}
                r=3 />
    {/each}
</svg>
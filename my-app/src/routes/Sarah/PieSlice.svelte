<script>
    export let cx = 0;
    export let cy = 0;
    export let r = 50;
    export let start_degree = 0;
    export let stop_degree = 0;
    
    const colors = [
    'Navy', 'RoyalBlue', 'Teal', 'SpringGreen', 'Yellow', 'Pink',
    'Tomato', 'Red', 'GoldenRod', 'SaddleBrown', 'ForestGreen', 'DarkSlateGrey'
  ]; 
    
  
    const degree2radians = function(degree) {
      return Math.PI*(degree)/180
    }
  
    const x = function(cx, radius, theta) {
      return Number(cx) + radius*Math.cos(theta)
    }
  
    const y = function(cy, radius, theta) {
      return Number(cy) + radius*Math.sin(theta)
    }
  
    const pieslice = function(cx, cy, r, start_degree, stop_degree) {
      let start_theta = degree2radians(start_degree)
      let stop_theta = degree2radians(stop_degree)
      let start_x = x(cx,r,start_theta)
      let start_y = y(cy,r,start_theta)
      let stop_x = x(cy,r,stop_theta)
      let stop_y = y(cx,r,stop_theta)
      return "M " + cx + " " + cy + " " +
             "L " + start_x + " " + start_y + " " +
             "A " + r + " " + r + " 0 0 1 " + stop_x + " " + stop_y + " " +
             "Z"
    }
  </script>
  
  <style>
    path {
      stroke: black;
    }
  </style>
  
  {#each Array.from({ length: 12 }).keys() as index}
  {#if index < colors.length}
    <path d={pieslice(cx, cy, r, start_degree + (index * (360 / 12)), start_degree + ((index + 1) * (360 / 12)), colors[index])} style="fill:{colors[index]};" />
  {/if}
{/each}
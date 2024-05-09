<script>
    import PieSlice from './PieSlice.svelte';
    export let data = []
  
    let slices = []
    let running_sum = 0
    $: {
      data.pie.forEach(function(d) {
        let new_running_sum = running_sum + d;
        slices.push([running_sum, new_running_sum])
        running_sum = new_running_sum;
      })
    }
  </script>
  
  <style>
    svg {
      background-color: whitesmoke;
    }
  </style>
  <h1>Total Price of Orders in CP per Month</h1>
  <svg width=500 height=500>
    {#each slices as slice}
      <PieSlice cx=250 cy=250
                r=150
                start_degree={slice[0]} stop_degree={slice[1]} />
    {/each}
  </svg>
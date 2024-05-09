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
  <svg width=800 height=500>
    {#each slices as slice}
      <PieSlice cx=250 cy=250
                r=150
                start_degree={slice[0]} stop_degree={slice[1]} />
    {/each}
    <circle cx={500} cy={100} r="10" style = "fill:Navy"/>
    <text x={520} y={105}  fill="black">
      January
    </text>
    <circle cx={500} cy={130} r="10" style = "fill:RoyalBlue"/>
    <text x={520} y={135}  fill="black">
      February
    </text>
    <circle cx={500} cy={160} r="10" style = "fill:Teal"/>
    <text x={520} y={165}  fill="black">
      March
    </text>
    <circle cx={500} cy={190} r="10" style = "fill:SpringGreen"/>
    <text x={520} y={195}  fill="black">
      April
    </text>
    <circle cx={500} cy={220} r="10" style = "fill:Yellow"/>
    <text x={520} y={225}  fill="black">
      May
    </text>
    <circle cx={500} cy={250} r="10" style = "fill:Pink"/>
    <text x={520} y={255}  fill="black">
      June
    </text>
    <circle cx={500} cy={280} r="10" style = "fill:Tomato"/>
    <text x={520} y={285}  fill="black">
      July
    </text>
    <circle cx={500} cy={310} r="10" style = "fill:Red"/>
    <text x={520} y={315}  fill="black">
      August
    </text>
    <circle cx={500} cy={340} r="10" style = "fill:GoldenRod"/>
    <text x={520} y={345}  fill="black">
      September
    </text>
    <circle cx={500} cy={370} r="10" style = "fill:SaddleBrown"/>
    <text x={520} y={375}  fill="black">
      October
    </text>
    <circle cx={500} cy={400} r="10" style = "fill:ForestGreen"/>
    <text x={520} y={405}  fill="black">
      November
    </text>
    <circle cx={500} cy={430} r="10" style = "fill:DarkSlateGrey"/>
    <text x={520} y={435}  fill="black">
      December
    </text>



  </svg>
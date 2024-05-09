<script lang="ts">
    import PieSlice from './PieSlice.svelte';
    import PieSlice2 from './PieSlice2.svelte'
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

    let slices2 = []
    let running_sum2 = 0
    
  
      data.pie2.forEach(function(d) {
        let new_running_sum2 = running_sum2 + d;
        slices.push([running_sum2, new_running_sum2])
        running_sum2 = new_running_sum2;
      })

  </script>
  
  <style>
    svg {
      background-color: whitesmoke;
    }
  </style>
  <h1>Total Price of Orders in CP per Month</h1>
  <svg width=900 height=440>
    {#each slices as slice}
      <PieSlice cx=280 cy=280
                r=150
                start_degree={slice[0]} stop_degree={slice[1]} />
      <text cx={200}>2000</text>
    {/each}
    <circle cx={550} cy={100} r="6" style = "fill:Navy"/>
    <text x={570} y={105}  fill="black">
      January
    </text>
    <text x={340} y={265}  fill="grey" style="font-size: 12px;" transform="rotate(-10, 340, 265)">
      202187579 CP
    </text>
    <circle cx={550} cy={130} r="6" style = "fill:RoyalBlue"/>
    <text x={570} y={135}  fill="black">
      February
    </text>
    <text x={340} y={300}  fill="grey" style="font-size: 12px;" transform="rotate(15, 340, 300)">
      185629798 CP
    </text>
    <circle cx={550} cy={160} r="6" style = "fill:Teal"/>
    <text x={570} y={165}  fill="black">
      March
    </text>
    <text x={320} y={320}  fill="grey" style="font-size: 12px;" transform="rotate(45, 320, 320)">
      202775019 CP
    </text>
    <circle cx={550} cy={190} r="6" style = "fill:SpringGreen"/>
    <text x={570} y={195}  fill="black">
      April
    </text>
    <text x={290} y={337}  fill="grey" style="font-size: 12px;" transform="rotate(74, 290, 337)">
      196118588 CP
    </text>
    <circle cx={550} cy={220} r="6" style = "fill:Yellow"/>
    <text x={570} y={225}  fill="black">
      May
    </text>
    <text x={260} y={337}  fill="grey" style="font-size: 12px;" transform="rotate(105, 260, 337)">
      200957818 CP
    </text>
    <circle cx={550} cy={250} r="6" style = "fill:Pink"/>
    <text x={570} y={255}  fill="black">
      June
    </text>
    <text x={230} y={322}  fill="grey" style="font-size: 12px;" transform="rotate(128, 230, 322)">
      196001409 CP
    </text>
    <circle cx={550} cy={280} r="6" style = "fill:Tomato"/>
    <text x={570} y={285}  fill="black">
      July
    </text>
    <text x={150} y={320}  fill="grey" style="font-size: 12px;" transform="rotate(-15, 150, 320)">
      202412737 CP
    </text>
    <circle cx={550} cy={310} r="6" style = "fill:Red"/>
    <text x={570} y={315}  fill="black">
      August
    </text>
    <text x={147} y={260}  fill="grey" style="font-size: 12px;" transform="rotate(9, 147, 260)">
      204066468 CP
    </text>
    <circle cx={550} cy={340} r="6" style = "fill:GoldenRod"/>
    <text x={570} y={345}  fill="black">
      September
    </text>
    <text x={173} y={190}  fill="grey" style="font-size: 12px;" transform="rotate(40, 173, 190)">
      199097111 CP
    </text>
    <circle cx={550} cy={370} r="6" style = "fill:SaddleBrown"/>
    <text x={570} y={375}  fill="black">
      October
    </text>
    <text x={235} y={155}  fill="grey" style="font-size: 12px;" transform="rotate(70, 235, 155)">
      2060651901 CP
    </text>
    <circle cx={550} cy={400} r="6" style = "fill:ForestGreen"/>
    <text x={570} y={405}  fill="black">
      November
    </text>
    <text x={305} y={145}  fill="grey" style="font-size: 12px;" transform="rotate(100, 305, 145)">
      196109905 CP
    </text>
    <circle cx={550} cy={430} r="6" style = "fill:DarkSlateGrey"/>
    <text x={570} y={435}  fill="black">
      December
    </text>
    <text x={324} y={240}  fill="grey" style="font-size: 12px;" transform="rotate(-47, 324, 240)">
      204087666 CP
    </text>
  </svg>

  <svg width=900 height=500>
    {#each slices2 as slice2}
      <PieSlice2 cx=300 cy=300
                r=80
                start_degree={slice2[0]} stop_degree={slice2[1]} />
    {/each}
    {#each data.pie2 as p}
    <ul>
      {p}
    </ul>
    {/each}
    <image xlink:href="./violin.png" x="200" y="-100" width="550" height="700" />
  </svg>
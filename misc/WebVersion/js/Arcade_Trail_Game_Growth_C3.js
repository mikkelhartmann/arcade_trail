window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#Arcade_Trail_Game_Growth',
        data: {
          x: 'Month',
          columns: [
            ['Month','May','Jun','Jul','Aug','Sep','Oct','Nov'],
            ['ArcadeTrail', 116,258,433,635,839,1331,2066]
          ],
          type: 'bar',
          colors: {
            ArcadeTrail: '#c61aff'
          }
        },
        size: {
          width: 600,
          height: 400
        },
        padding: {
          top: 0,
          right: 100,
          bottom: 112,
          left: 80
        },
        axis: {
          x: {
            type: 'categorized',
            tick: {
              rotate: -45,
              fit: true,
              multiline: false
            },
            label: {
              text: '', 
              position: 'outer-center'
            }
          },
          y: {
            label: {
              text: 'Number of games in Arcade Trail', 
              position: 'outer-middle'
            }
          }
        },
        legend: {
          hide: true
        },
    });
});
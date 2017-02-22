window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#User_Comparison_Genre_Distribution',
        data: {
          x : 'x',
          columns: [
            ['x', 'Action','Adventure','Fighting','Hidden Objects','Indie','MMO','Platformer','Puzzle,','RPG','Racing','Sandbox','Shooter','Simulation','Sports','Strategy','Survival'],
            ['Michael', 77,36,1,1,98,1,1,1,1,23,2,1,2,34,2,90,1],
            ['Mikkel',  10,7,1,1,1,11,3,1,1,7,1,1,1,3,1,11,1]
          ],
          type: 'bar',
          colors: {
            Michael: '#c61aff',
            Mikkel: '#29a329'
          }
        },
        size: {
          width: 600,
          height: 400
        },
        axis: {
          x: {
            type: 'categorized', 
            tick: {
              rotate: -45,
              fit: true,
              multiline: false
            }
          },
          y: {
            label: {
              text: 'Number of games in genre', 
              position: 'outer-middle'
            }
          }
        },
        legend: {
          position: 'right'
        },
        padding: {
          top: 0,
          right: 100,
          bottom: 200,
          left: 80
        }
    });
});
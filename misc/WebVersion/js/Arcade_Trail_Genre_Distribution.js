window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#Arcade_Trail_Genre_Distribution',
        data: {
          x : 'x',
          columns: [
            ['x', 'Action','Adventure','Fighting','Hidden Objects','Indie','MMO','Platformer','Puzzle,','RPG','Racing','Sandbox','Shooter','Simulation','Sports','Strategy','Survival'],
            ['ArcadeTrail', 1001,688,2,3,1190,53,11,9,372,66,2,17,265,66,435,90,1]
          ],
          type: 'bar',
          colors: {
            ArcadeTrail: '#c61aff',
            Mikkel: '#29a329'
          }
        },
        size: {
          width: 750,
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
          hide: true
        },
        padding: {
          top: 0,
          right: 100,
          bottom: 200,
          left: 100
        }
    });
});
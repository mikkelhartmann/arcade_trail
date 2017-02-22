window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#User_Comparison_Release_Date_Distribution',
        data: {
          x: 'Year',
          columns: [
            ['Year',2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015],
            ['Michael', 2,5,12,9,22,10,26,38,39,12,12],
            ['Mikkel', 0,0,0,0,0,1,1,1,5,7,7]
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
        padding: {
          top: 0,
          right: 100,
          bottom: 112,
          left: 60
        },
        axis: {
          x: {
            tick: {
              values: [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015],
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
              text: 'Number of games released', 
              position: 'outer-middle'
            }
          }
        },
        legend: {
          position: 'right'
        }
    });
});
window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#Arcade_Trail_Release_Date_Distribution',
        data: {
          x: 'Year',
          columns: [
            ['Year',1996,1997,1998,1999,2000,2001,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016],
            ['ArcadeTrail', 2,2,2,2,4,3,2,6,5,11,50,48,74,66,77,109,160,135,1255,11]
          ],
          type: 'bar',
          colors: {
            ArcadeTrail: '#c61aff'
          }
        },
        size: {
          width: 750,
          height: 400
        },
        padding: {
          top: 0,
          right: 100,
          bottom: 112,
          left: 100
        },
        axis: {
          x: {
            tick: {
              values: [1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016],
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
          hide: true
        },
    });
});
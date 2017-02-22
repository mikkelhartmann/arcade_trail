window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#Arcade_Trail_Missing_Genre',
        data: {
          columns: [
            ['Have', 2436],
            ['Missing', 58]
          ],
          type: 'donut',
          colors: {
            Have: '#c61aff',
            Missing: '#29a329'
          },
        },
        size: {
          width: 350,
          height: 350
        },
        legend: {
          position: 'right'
        },
        donut: {
          title: "Release Dates",
          label: {
            format: function (value) { return value; }
          }
        },
        padding: {
          bottom: 110
        }

    });
});
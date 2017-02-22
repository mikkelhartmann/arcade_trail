window.addEventListener('load', function(){
    var chart = c3.generate({
        bindto: '#User_Comparison_Library_Cost',
        data: {
          columns: [
            ['Michael', 1613],
            ['Mikkel', 322]
          ],
          type: 'donut',
          colors: {
            Michael: '#c61aff',
            Mikkel: '#29a329'
          },
          labels: {format: {Michael: d3.format('aaaa')}}
        },
        size: {
          width: 350,
          height: 350
        },
        axis: {
          x: {label: ''},
          y: {label: {text: 'Cost of entire library', position: 'outer-middle'}}
        },
        legend: {
          position: 'right'
        },
        donut: {
          title: "Cost of libraries",
          label: {
            format: function (value) { return value; }
          }
        }

    });
});
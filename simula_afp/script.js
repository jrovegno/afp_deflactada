var cargarExcel = function(url, callback) {
  var oReq = new XMLHttpRequest();
  oReq.open("GET", url, true);
  oReq.responseType = "arraybuffer";

  oReq.onload = function(e) {
    var arraybuffer = oReq.response;

    /* convert data to binary string */
    var data = new Uint8Array(arraybuffer);
    var arr = new Array();
    for(var i = 0; i != data.length; ++i) arr[i] = String.fromCharCode(data[i]);
    var bstr = arr.join("");

    /* Call XLSX */
    var workbook = XLSX.read(bstr, {type:"binary"});

    callback(workbook);
  }

  oReq.send();
}

var graficar = function(series, id) {
  var graph = new Rickshaw.Graph({
    element: document.querySelector(id + ' .chart'),
    renderer: 'multi',
    width: 900,
    height: 320,
    dotSize: 5,
    series: series
  });

  var slider = new Rickshaw.Graph.RangeSlider.Preview({
    graph: graph,
    element: document.querySelector(id + ' .slider')
  });

  graph.render();

  var detail = new Rickshaw.Graph.HoverDetail({
  	graph: graph,
    formatter: function(series, x, y) {
      var fecha = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>';
      var monto = y.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,').replace('.00', '');
      var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
      var content = swatch + series.name + ": $" + monto + '<br>' + fecha;
      return content;
    }
  });

  var legend = new Rickshaw.Graph.Legend({
  	graph: graph,
  	element: document.querySelector(id + ' .legend')
  });

  var time = new Rickshaw.Fixtures.Time.Local();

  var xAxis = new Rickshaw.Graph.Axis.Time({
      graph: graph,
      timeUnit: time.unit('year')
  });
  xAxis.render();

  var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
      graph: graph,
      legend: legend,
      disabledColor: function() { return 'rgba(0, 0, 0, 0.2)' }
  });
}

var obtener_series = function(data) {
  var filas = XLSX.utils.sheet_to_row_object_array(data.Sheets.DATOS);
  filas = $.grep(filas, function(item) {
    return item.Mes != '';
  });
  var fecha = null;
  var plata_a_numero = function(valor) {
    var r = parseInt(valor.split(' ').join('').replace('$', '').split(',').join(''));
    return isNaN(r) ? 0 : r;
  }
  var resultado = $.map(filas, function(item) {
    if (fecha == null) {
      fecha = new Date(item.Año, item.Mes, 1, 0, 0, 0, 0);
    } else {
      fecha.setMonth(fecha.getMonth() + 1);
    }
    return {
      fecha: fecha.getTime() / 1000,
      fondo: plata_a_numero(item.FONDO),
      rentabilidad: plata_a_numero(item.RENTABILIDAD),
      aporte: plata_a_numero(item.APORTE),
      comision: plata_a_numero(item.COMISION)
    };
  });

  var palette = new Rickshaw.Color.Palette();

  var series = [
    {
      name: 'APORTE',
      data: $.map(resultado, function(item) { return {x: item.fecha, y: item.aporte }}),
      color: palette.color(),
      renderer: 'stack'
    }, {
      name: 'RENTABILIDAD',
      data: $.map(resultado, function(item) { return {x: item.fecha, y: item.rentabilidad }}),
      color: palette.color(),
      renderer: 'stack'
    }, {
      name: 'COMISION',
      data: $.map(resultado, function(item) { return {x: item.fecha, y: item.comision }}),
      color: palette.color(),
      renderer: 'line'
    }, {
      name: 'FONDO',
      data: $.map(resultado, function(item) { return {x: item.fecha, y: item.fondo }}),
      color: palette.color(),
      renderer: 'line'
    }
  ];
  
  return series;
}

cargarExcel('simula_afp_cuprum_C.xlsx', function(data) {
  var series = obtener_series(data);
  graficar(series, '#cuprum_pesos');
});

cargarExcel('simula_afp_habitat_C.xlsx', function(data) {
  var series = obtener_series(data);
  graficar(series, '#habitat_pesos');
});



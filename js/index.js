$('#run').on('click', function(e) {
  e.preventDefault();
  
  toogleValue = $('#ui-or-bv')[0].checked;

  if(toogleValue) {
    run("unbounded_integers");
  } else {
    run("bit_vectors");
  }
});

function run(theory) {

  $('#output-div').slideUp('fast');

  var code = $('#code').val();
  var data = { code : code, theory : theory };

  $.ajax({
    url : 'http://localhost:8000/api/v1/igen',
    type : "POST",
    data : JSON.stringify(data),
    contentType : "application/json",
    dataType : "json",
    complete : function(data) {
      var json = data.responseText;
      console.log(json);
      var replies = JSON.parse(json);
      console.log(replies);

      var output = ''

      for(var i = 0; i < replies.vcs.length; i++) {
        var reply = JSON.parse(replies.vcs[i]);
        var vc = reply.vc;
        var sat_or_unsat = reply.sat_or_unsat;
        var model_or_unsat_core = reply.model_or_unsat_core

        output += vc + '\n'
        output += sat_or_unsat.toUpperCase() + '\n'
      }

      $('#output-div').show('slow');
      $('#output').val(output);
    }
  });
}

$('.title').on('click', function(e) {
  var code =
    'pre x > 100 end;\n\n' + 
    'while x < 1000 do\n' + 
    '    inv 100 < x and x <= 1000 end;\n' + 
    '    x := x + 1\n' + 
    'end;\n\n' + 
    'pos x = 1000 end\n';
  
  $('#code').val(code);
});


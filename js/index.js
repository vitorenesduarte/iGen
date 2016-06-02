$('#run').on('click', function(e) {
  e.preventDefault();
  run();
});

function run() {
  $('#output-div').slideUp('slow');

  var code = $('#code').val();
  var data = { code : code };

  $.ajax({
    url : 'http://localhost:8000/api/v1/igen',
    type : "POST",
    data : JSON.stringify(data),
    contentType : "application/json",
    dataType : "json",
    complete : function(data) {
      var json = data.responseText;
      var reply = JSON.parse(json);

      var vcs = reply.vcs;
      var result = reply.result;

      var output = ''
      for(var i = 0; i < vcs.length; i++)
        output += vcs[i] + '\n'
      output += '\n' + result

      $('#output').val(output);
      $('#output-div').slideDown('slow');
    }
  });
}

$('#back-to-top').on('click', function(e) {
  e.preventDefault();
  $('html,body').animate({
    scrollTop: 0
  }, 700);
});

$('.do-nothing').on('click', function(e) {
  e.preventDefault();
});

$('.title').on('click', function(e) {
  var code =
    'pre x > 100 end;\n' + 
    'while x < 1000 do\n' + 
    '    inv 100 < x and x <= 1000 end;\n' + 
    '    x := x + 1\n' + 
    'end;\n' + 
    'pos x > 1000 end\n';
  
  $('#code').val(code);
});


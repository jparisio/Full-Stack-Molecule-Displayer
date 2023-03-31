/* javascript to accompany jquery.html */

$(document).ready( 
	/* this defines a function that gets called after the document is in memory */
	function()
	{
  
	  /* add a click handler for our button */
	  $("#button").click(
		function()
		{
	  /* ajax post */
	  $.post("/form_handler.html",
		/* pass a JavaScript dictionary */
		{
		  name: $("#name").val(),
		  code: $("#code").val(),
		  number: $("#number").val(),
		  c1: $("#c1").val(),
		  c2: $("#c2").val(),
		  c3: $("#c3").val(),	
		  radius: $("#radius").val(),
		//   extra_info: "some stuff here"
		},
		function( data, status )
		{
		  alert( "Data: " + data + "\nStatus: " + status );
		}
	  );
		}
	  );


	  $("#delete").click(
		function()
		{
	  /* ajax post */
	  $.post("/deleteElement.html",
		/* pass a JavaScript dictionary */
		{
		  eNumber: $("#eNo").val(),
		//   extra_info: "some stuff here"
		},
		function( data, status )
		{
		  alert( "Data: " + data + "\nStatus: " + status );
		}
	  );
		}
	  );


	  $("#upload").click(
		function()
		{
	  /* ajax post */
	  $.post("/sdf_upload.html",
		/* pass a JavaScript dictionary */
		{
		  molName: $("#molName").val(),
		  file: $('#sdf_file').prop('files')
		//   extra_info: "some stuff here"
		},
		function( data, status )
		{
		  alert( "Data: " + data + "\nStatus: " + status );
		}
	  );
		}
	  );




	}
  );
  
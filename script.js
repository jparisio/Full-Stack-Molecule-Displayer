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
			// console.log("enter")
			const file =  $("#files")[0].files[0];
			const molName = $("#molName").val();
			const formData = new FormData();

			formData.append("file",file);
			formData.append("molName", molName);

			$.ajax({
				url : "/sdf_upload.html",
				type : "POST",
				data : formData,
				processData: false,
				contentType: false,
				success: function(data) {
					alert('FILE UPLOADED')
				}
			}
		  );
		}
	  );



	  $("#molList").click(
		function()
		{
	  /* ajax post */
	  $.post("/moleculesList.html",
		/* pass a JavaScript dictionary */
		{
		  molList: $("#molList").val(),
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
  
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
					alert(data)
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
		//   alert( "Data: " + data + "\nStatus: " + status );
		//   $("#label").text(data);
		  const arr = data.split(" ");
		  for(let i = 0; i < arr.length - 1; i++){
			var txt = $("<p></p>").text(arr[i] + " " + arr[i + 1] + " " + arr[i + 2]); 
			i++;
			i++;  
  		  	$("#addHere").append(txt);
			txt.attr('id', 'mol' + String(i));
		  }
		//   var title =   $("<h3 id = 'selectTitle'>Type in Molecule you would like to select</h3>");
		//   var selector =  $("<input id = 'selector'></input>");
		//   var selectbutton = $("<button id = 'selectButton'></button>").text("Enter"); 
		//   $("#addHere").append(title);
		//   $("#addHere").append(selector);
		//   $("#addHere").append(selectbutton);
		}
	  );
		}
	  );



	  $("#selectButton").click(
		function()
		{
		/* ajax post */
		$.post("/display_sdf.html",
			/* pass a JavaScript dictionary */
			{
			mol: $("#selector").val(),
			//   extra_info: "some stuff here"
			},
			function( data, status )
			{
			if(data == "Molecule doesnt exist"){
				alert(data);
			} else {
			alert(status + ", scroll to see molecule")
			// var txt = $("<div></div>").svg(data);   // Create with jQuery
  		  	$("#svgGoesHere").append(data);
			// $("#svgGoesHere").text(data);
			// $("#svgGoesHere").hide();
			var txt = $("<button></button>").text("rotate");
			var txt2 = $("<label></label>").text("		insert rotation angle into either x (field 1), y (field 2), or z (field 3), other two fields must be zero");
			var input1 = $("<input></input>");   
			var input2 = $("<input></input>");  
			var input3 = $("<input></input>");    // Create with jQuery
			$("#rotate").prepend(txt2);
  		  	$("#rotate").prepend(txt);
			$("#rotateFields").append(input1);
			$("#rotateFields").append(input2);
			$("#rotateFields").append(input3);
			input1.attr("id", "r1");
			input2.attr("id", "r2");
			input3.attr("id", "r3");
			}

			}
		  );
		}
	  );




	  $("#rotate").click(
		function()
		{
	  /* ajax post */
	  $.post("/rotate.html",
		/* pass a JavaScript dictionary */
		{
		  svg_image: $("#selector").val(),
		  r1: $("#r1").val(),
		  r2: $("#r2").val(),
		  r3: $("#r3").val(),
		//   extra_info: "some stuff here"
		},
		function( data, status )
		{
			if(data == "incorrect values input"){
				alert(data)
			} else{
		  	alert("rotated");
		  	$("#svgGoesHere").remove();
			var txt = $("<label></label>");   // Create with jQuery
  		  	$("#svgGoesHere2").after(txt);
			txt.attr("id","svgGoesHere");
		  	$("#svgGoesHere").append(data);
			}
		}
		
	  );
		}
	  );



	//   $("#upload_html").click(
	// 	function()
	// 	{
	// 	/* ajax post */
	// 	$.ajax({
	// 		type: 'POST',
	// 		url: form.attr('action'),
	// 		data: form.serialize(), // serializes form elements
	// 		success: function(response) {
	// 		  // re-writes the entire document
	// 		  var newDoc = document.open("text/html", "replace");
	// 		  newDoc.write(response);
	// 		  newDoc.close();
	// 		}
	// 	  });
	// 	}
	//   );





	}
  );
  